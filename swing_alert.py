#!/usr/bin/env python3
"""Commodity swing alerts for Brent, WTI and Henry Hub natgas.

Signals (adapted from TTM-squeeze / volatility-breakout ideas, e.g. hackingthemarkets/ttm-squeeze):
  SETUP  - Bollinger Bands contract inside Keltner Channels ("squeeze"): volatility is coiled,
           a large move tends to follow. Heads-up alert, no trade yet.
  ENTRY  - squeeze releases + momentum direction + trend filter + volume confirmation.
           Sends entry, stop (1.5 ATR), targets (2R / 4R ATR) and trailing stop rule.
  EXIT   - stop, target, chandelier trailing stop, or momentum flip on an open signal.
  EVENT  - warns before scheduled volatility (EIA crude Wed 10:30 ET, EIA gas storage Thu 10:30 ET,
           plus any dates in EXTRA_EVENTS, e.g. OPEC+ meetings).

Usage:
  python swing_alert.py scan       # check now, send alerts (run every 15-60 min)
  python swing_alert.py backtest   # test the rules on history
  python swing_alert.py selftest   # offline test with synthetic data
Notifications: set NTFY_TOPIC (free phone push via ntfy.sh app) and/or TELEGRAM_TOKEN + TELEGRAM_CHAT_ID,
and/or DISCORD_WEBHOOK.  Set ALPACA_KEY + ALPACA_SECRET for real-time data (else Yahoo, ~10 min delayed).
Optional EIA_API_KEY adds weekly inventory surprise context.
"""
import json, os, sys, datetime as dt
from zoneinfo import ZoneInfo
import numpy as np, pandas as pd, requests

for _k, _v in list(os.environ.items()):  # tolerate secrets pasted with stray spaces/newlines
    if _v != _v.strip(): os.environ[_k] = _v.strip()

MARKETS = {"BRENT": "BZ=F", "WTI": "CL=F", "NATGAS": "NG=F"}
INTERVAL, PERIOD = os.getenv("INTERVAL", "1h"), os.getenv("PERIOD", "60d")
P = dict(bb_len=20, bb_k=2.0, kc_k=1.5, atr_len=14, ema_trend=50, vol_mult=1.2,
         stop_atr=1.5, t1_atr=2.0, t2_atr=4.0, trail_atr=3.0, min_squeeze_bars=6)
EXTRA_EVENTS = [e for e in os.getenv("EXTRA_EVENTS", "").split(",") if e]  # "2026-11-30 OPEC+ meeting"
STATE_FILE = os.getenv("STATE_FILE", "state.json")
ET = ZoneInfo("America/New_York")


# ---------------- indicators ----------------
def indicators(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    c, h, l = d.Close, d.High, d.Low
    n = P["bb_len"]
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    d["atr"] = tr.ewm(alpha=1 / P["atr_len"], adjust=False).mean()
    mid, sd = c.rolling(n).mean(), c.rolling(n).std()
    kc_rng = tr.rolling(n).mean() * P["kc_k"]
    d["sq"] = ((mid - P["bb_k"] * sd) > (mid - kc_rng)) & ((mid + P["bb_k"] * sd) < (mid + kc_rng))
    d["sq_bars"] = d.sq.groupby((~d.sq).cumsum()).cumsum()
    # TTM-style momentum: linreg of price minus midpoint of Donchian/SMA
    base = c - ((h.rolling(n).max() + l.rolling(n).min()) / 2 + mid) / 2
    x = np.arange(n)
    d["mom"] = base.rolling(n).apply(lambda y: np.polyfit(x, y, 1)[0] * (n - 1) + np.polyfit(x, y, 1)[1], raw=True)
    d["ema"] = c.ewm(span=P["ema_trend"], adjust=False).mean()
    d["bbw_pct"] = ((4 * sd / mid).rolling(250, min_periods=50).rank(pct=True))  # width percentile
    vol = d.get("Volume", pd.Series(0, index=d.index)).fillna(0)
    d["vol_ok"] = (vol == 0) | (vol > vol.rolling(n).mean() * P["vol_mult"])
    d["rsi"] = rsi(c)
    return d


def rsi(c, n=14):
    delta = c.diff()
    up = delta.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-delta.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def signal_at(d: pd.DataFrame, i: int):
    """Return (kind, side) for bar i: ('ENTRY','LONG'/'SHORT') | ('SETUP',None) | (None,None)."""
    r, prev = d.iloc[i], d.iloc[i - 1]
    if prev.sq and not r.sq and prev.sq_bars >= P["min_squeeze_bars"] and r.vol_ok:
        if r.mom > 0 and r.mom > prev.mom and r.Close > r.ema and r.rsi < 75:
            return "ENTRY", "LONG"
        if r.mom < 0 and r.mom < prev.mom and r.Close < r.ema and r.rsi > 25:
            return "ENTRY", "SHORT"
    if r.sq and r.sq_bars == P["min_squeeze_bars"]:
        return "SETUP", None
    return None, None


def plan(side, price, atr):
    s = 1 if side == "LONG" else -1
    return dict(side=side, entry=price, stop=price - s * P["stop_atr"] * atr,
                t1=price + s * P["t1_atr"] * atr, t2=price + s * P["t2_atr"] * atr,
                best=price, atr=atr, t1_hit=False)


def manage(pos, r):
    """Update open position with bar r. Returns exit reason or None."""
    s = 1 if pos["side"] == "LONG" else -1
    hi, lo = (r.High, r.Low) if s == 1 else (-r.Low, -r.High)
    pos["best"] = max(pos["best"] * s, hi) * s
    trail = pos["best"] - s * P["trail_atr"] * r.atr
    if pos["t1_hit"]:
        pos["stop"] = max(pos["stop"] * s, pos["entry"] * s, trail * s) * s  # breakeven + trail after T1
    if lo <= pos["stop"] * s:
        return "STOP/TRAIL", pos["stop"]
    if hi >= pos["t2"] * s:
        return "TARGET 2", pos["t2"]
    if not pos["t1_hit"] and hi >= pos["t1"] * s:
        pos["t1_hit"] = True
        return "T1_PARTIAL", pos["t1"]
    if s * r.mom < 0 and pos["t1_hit"]:
        return "MOMENTUM FLIP", r.Close
    return None, None


# ---------------- data ----------------
ALPACA_MAP = {"BZ=F": "BNO", "CL=F": "USO", "NG=F": "UNG"}  # ETFs tracking front-month futures


def fetch_alpaca(sym, period, interval):
    """Real-time bars (free IEX feed) from Alpaca for the ETF proxy of each future."""
    tf = {"1h": "1Hour", "15m": "15Min", "5m": "5Min", "1d": "1Day"}[interval]
    days = int(period[:-1]) * (365 if period.endswith("y") else 1)
    start = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    hdr = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET"]}
    rows, tok = [], None
    while True:
        q = {"timeframe": tf, "start": start, "limit": 10000, "feed": os.getenv("ALPACA_FEED", "iex"),
             "adjustment": "all", **({"page_token": tok} if tok else {})}
        j = requests.get(f"https://data.alpaca.markets/v2/stocks/{ALPACA_MAP[sym]}/bars",
                         headers=hdr, params=q, timeout=20)
        j.raise_for_status(); j = j.json()
        rows += j.get("bars") or []
        if not (tok := j.get("next_page_token")):
            break
    if not rows:
        raise RuntimeError(f"no Alpaca data for {ALPACA_MAP[sym]}")
    df = pd.DataFrame(rows).rename(columns={"t": "Date", "o": "Open", "h": "High", "l": "Low", "c": "Close", "v": "Volume"})
    return df.set_index(pd.to_datetime(df.Date))[["Open", "High", "Low", "Close", "Volume"]]


def fetch(sym, period=PERIOD, interval=INTERVAL):
    if os.getenv("ALPACA_KEY") and os.getenv("DATA_SOURCE", "alpaca") == "alpaca":
        try:
            return fetch_alpaca(sym, period, interval)
        except Exception as e:
            print(f"Alpaca failed ({e.__class__.__name__}: {str(e)[:60]}), falling back to Yahoo")
    import yfinance as yf
    df = yf.Ticker(sym).history(period=period, interval=interval, auto_adjust=False)
    if df.empty:
        raise RuntimeError(f"no data for {sym}")
    return df[["Open", "High", "Low", "Close", "Volume"]].dropna()


def eia_context():
    """Latest weekly crude & gas storage change from EIA (official source). Needs free EIA_API_KEY."""
    key = os.getenv("EIA_API_KEY")
    if not key:
        return ""
    out = []
    for name, route, sid in [("US crude stocks", "petroleum/stoc/wstk", "WCESTUS1"),
                             ("US gas storage", "natural-gas/stor/wkly", "NW2_EPG0_SWO_R48_BCF")]:
        try:
            j = requests.get(f"https://api.eia.gov/v2/{route}/data/", timeout=15, params={
                "api_key": key, "frequency": "weekly", "data[0]": "value", "facets[series][]": sid,
                "sort[0][column]": "period", "sort[0][direction]": "desc", "length": 2}).json()
            v = j["response"]["data"]
            out.append(f"{name}: {float(v[0]['value']) - float(v[1]['value']):+,.0f} wk/wk ({v[0]['period']})")
        except Exception as e:
            out.append(f"{name}: n/a ({e.__class__.__name__})")
    return "\n".join(out)


def upcoming_events(now=None, hours=3):
    now = now or dt.datetime.now(ET)
    ev = []
    for days in range(0, 2):
        day = (now + dt.timedelta(days=days)).date()
        t = dt.datetime.combine(day, dt.time(10, 30), ET)
        if day.weekday() == 2: ev.append((t, "EIA crude inventory report (WTI/Brent)"))
        if day.weekday() == 3: ev.append((t, "EIA natgas storage report (NATGAS)"))
    for e in EXTRA_EVENTS:
        d, _, name = e.partition(" ")
        ev.append((dt.datetime.fromisoformat(d).replace(hour=9, tzinfo=ET), name or "event"))
    return [f"{name} at {t:%a %H:%M ET}" for t, name in ev if dt.timedelta(0) <= t - now <= dt.timedelta(hours=hours)]


# ---------------- notify ----------------
def notify(title, body, priority="default"):
    print(f"\n=== {title}\n{body}")
    if t := os.getenv("NTFY_TOPIC"):
        pr = {"min": 1, "low": 2, "default": 3, "high": 4, "urgent": 5}[priority]
        try:  # JSON publish supports emoji in titles
            requests.post("https://ntfy.sh/", timeout=15, json={"topic": t, "title": title, "message": body,
                          "priority": pr, "tags": ["oil_drum"]}).raise_for_status()
        except Exception as e:
            print("ntfy failed:", e, getattr(getattr(e, "response", None), "text", "")[:200])
    if (tok := os.getenv("TELEGRAM_TOKEN")) and (cid := os.getenv("TELEGRAM_CHAT_ID")):
        requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", timeout=15,
                      json={"chat_id": cid, "text": f"{title}\n{body}"})
    if w := os.getenv("DISCORD_WEBHOOK"):
        requests.post(w, json={"content": f"**{title}**\n{body}"}, timeout=15)


# ---------------- scan ----------------
def load_state():
    try:
        return json.load(open(STATE_FILE))
    except Exception:
        return {"positions": {}, "sent": []}


def scan():
    st = load_state()
    sent = set(st["sent"][-300:])
    ctx = eia_context()
    for e in upcoming_events():
        key = f"EV|{e}|{dt.date.today()}"
        if key not in sent:
            notify("⚠️ Volatility event soon", e + "\nExpect fast moves; widen stops or stay flat.", "high")
            sent.add(key)
    for name, sym in MARKETS.items():
        try:
            d = indicators(fetch(sym))
        except Exception as e:
            print(f"{name}: {e}"); continue
        i, r = len(d) - 2, d.iloc[-2]          # use last CLOSED bar (avoid repainting)
        print(f"{name}: {d.index[i]} close {r.Close:.3f} squeeze={bool(r.sq)}({int(r.sq_bars)}) mom={r.mom:+.3f} rsi={r.rsi:.0f}")
        bar = str(d.index[i])
        pos = st["positions"].get(name)
        if pos:
            reason, px = manage(pos, r)
            if reason:
                pnl = (px - pos["entry"]) / pos["entry"] * 100 * (1 if pos["side"] == "LONG" else -1)
                notify(f"🔔 {name} {'TAKE PARTIAL' if reason == 'T1_PARTIAL' else 'EXIT'} {pos['side']}",
                       f"{reason} @ {px:.3f}  ({pnl:+.2f}% from {pos['entry']:.3f})\n"
                       + ("Take ~half off, stop moved to breakeven, trail rest." if reason == "T1_PARTIAL" else ""),
                       "high")
                if reason != "T1_PARTIAL":
                    st["positions"].pop(name)
            continue
        kind, side = signal_at(d, i)
        key = f"{kind}|{name}|{bar}"
        if not kind or key in sent:
            continue
        sent.add(key)
        if kind == "SETUP":
            notify(f"👀 {name} squeeze building", f"Volatility compressed {int(r.sq_bars)} bars "
                   f"(BB width pct {r.bbw_pct:.0%}). Big move likely soon. Price {r.Close:.3f}, ATR {r.atr:.3f}.\n{ctx}")
        else:
            p = plan(side, r.Close, r.atr)
            st["positions"][name] = p
            risk = abs(p["entry"] - p["stop"]) / p["entry"] * 100
            notify(f"🚀 {name} ENTRY {side}",
                   f"Entry ~{p['entry']:.3f} ({sym})\nStop {p['stop']:.3f} (-{risk:.2f}%)\n"
                   f"T1 {p['t1']:.3f} (take half)  T2 {p['t2']:.3f}\nTrail {P['trail_atr']}xATR after T1.\n"
                   f"RSI {r.rsi:.0f}, momentum {r.mom:+.3f}\n{ctx}", "urgent")
    st["sent"] = list(sent)[-300:]
    json.dump(st, open(STATE_FILE, "w"), indent=1, default=float)


# ---------------- backtest ----------------
def backtest(d, fee_pct=0.03):
    d = indicators(d)
    trades, pos = [], None
    for i in range(60, len(d)):
        r = d.iloc[i]
        if pos:
            reason, px = manage(pos, r)
            if reason == "T1_PARTIAL":
                pos["half"] = (px - pos["entry"]) / pos["entry"] * (1 if pos["side"] == "LONG" else -1)
            elif reason:
                ret = (px - pos["entry"]) / pos["entry"] * (1 if pos["side"] == "LONG" else -1)
                ret = (ret + pos["half"]) / 2 if "half" in pos else ret
                trades.append(ret * 100 - 2 * fee_pct); pos = None
            continue
        kind, side = signal_at(d, i)
        if kind == "ENTRY":
            pos = plan(side, r.Close, r.atr)
    t = pd.Series(trades, dtype=float)
    if t.empty:
        return {"trades": 0}
    gp, gl = t[t > 0].sum(), -t[t < 0].sum()
    eq = t.cumsum()
    return {"trades": len(t), "win_rate": f"{(t > 0).mean():.0%}", "avg_%": round(float(t.mean()), 2),
            "total_%": round(float(t.sum()), 1), "profit_factor": round(float(gp / gl), 2) if gl else float("inf"),
            "max_dd_%": round(float((eq - eq.cummax()).min()), 1)}


def run_backtest():
    for name, sym in MARKETS.items():
        for interval, period in ([("1h", "1500d"), ("1d", "8y")] if os.getenv("ALPACA_KEY") else [("1h", "730d"), ("1d", "15y")]):
            try:
                print(name, interval, backtest(fetch(sym, period, interval)))
            except Exception as e:
                print(name, interval, "error:", e)


def selftest():
    rng = np.random.default_rng(1)
    n = 2000
    vol = np.where((np.arange(n) // 120) % 2, 0.004, 0.015)  # alternate calm / volatile regimes
    c = 75 * np.exp(np.cumsum(rng.normal(0, vol)))
    df = pd.DataFrame({"Open": c, "High": c * (1 + vol), "Low": c * (1 - vol), "Close": c,
                       "Volume": rng.integers(1000, 5000, n)}, index=pd.date_range("2024", periods=n, freq="h"))
    print("synthetic:", backtest(df))
    print("events (Wed 08:00 ET):", upcoming_events(dt.datetime(2026, 11, 4, 8, 0, tzinfo=ET)))


def doctor():
    """Describe secret formats without revealing them."""
    import re
    for k in ["ALPACA_KEY", "ALPACA_SECRET", "NTFY_TOPIC"]:
        v = os.getenv(k, "")
        print(f"{k}: len={len(v)} starts_with={v[:2]!r} url={v.startswith('http')} spaces={' ' in v}")
    t = os.getenv("NTFY_TOPIC", "")
    print("NTFY_TOPIC valid:", bool(re.fullmatch(r"[-_A-Za-z0-9]{1,64}", t)))
    try:
        fetch_alpaca("CL=F", "5d", "1h"); print("Alpaca: OK")
    except Exception as e:
        print("Alpaca:", str(e)[:80])


if __name__ == "__main__":
    {"scan": scan, "backtest": run_backtest, "selftest": selftest,
     "doctor": doctor, "testnotify": lambda: notify("✅ Swing alerts connected", "Test message. Data: " + ("Alpaca real-time" if os.getenv("ALPACA_KEY") else "Yahoo delayed"))}.get(
        (sys.argv[1:] or ["scan"])[0], lambda: print(__doc__))()
