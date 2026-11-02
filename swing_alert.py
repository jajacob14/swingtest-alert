#!/usr/bin/env python3
"""Commodity swing alerts: Brent (BNO / BZ=F), WTI (USO / CL=F), NatGas (UNG / NG=F).

Commands:
  scan      check latest closed bars, send ENTRY / EXIT / SETUP / EVENT alerts   (cron: every 15 min)
  brief     market snapshot for all three to your phone                          (cron: weekday mornings)
  optimize  grid-search strategies per market on ~2-4y data, walk-forward validate, write params.json (weekly)
  doctor    check secrets + ntfy delivery;  testnotify  send a test push;  selftest  offline test;  loop  run scan forever
Data: Alpaca real-time (ALPACA_KEY/ALPACA_SECRET, ETF proxies) else Yahoo futures (~10 min delayed).
Push: NTFY_TOPIC, TELEGRAM_TOKEN+TELEGRAM_CHAT_ID, DISCORD_WEBHOOK.  Context: EIA_API_KEY, EXTRA_EVENTS.
"""
import json, os, re, sys, time, itertools, datetime as dt
from zoneinfo import ZoneInfo
import numpy as np, pandas as pd, requests
from numpy.lib.stride_tricks import sliding_window_view as swv

for _k, _v in list(os.environ.items()):  # tolerate secrets pasted with stray spaces/newlines
    if _v != _v.strip(): os.environ[_k] = _v.strip()

MARKETS = {"BRENT": ("BZ=F", "BNO"), "WTI": ("CL=F", "USO"), "NATGAS": ("NG=F", "UNG")}
ET = ZoneInfo("America/New_York")
STATE_FILE, PARAMS_FILE = os.getenv("STATE_FILE", "state.json"), "params.json"
FEE = 0.03  # % per side: spread + slippage
BARS = {"15m": ("15Min", 15), "1h": ("1Hour", 60), "1d": ("1Day", 1440)}
HOLD = {"15m": 32, "1h": 40, "1d": 20}  # max bars in a trade (time stop)
DEFAULT = dict(interval="1h", strategy="squeeze", min_sq=6, trend=1, stop=1.5, tgt=3.0, trail=2.5, hold=40)
EXTRA_EVENTS = [e for e in os.getenv("EXTRA_EVENTS", "").split(",") if e]  # "2026-11-30 OPEC+ meeting"
ALPACA = bool(os.getenv("ALPACA_KEY"))


# ---------------- data ----------------
def fetch(mkt, interval, days):
    fut, etf = MARKETS[mkt]
    if ALPACA:
        try:
            return fetch_alpaca(etf, interval, days)
        except Exception as e:
            print(f"Alpaca failed ({str(e)[:70]}), falling back to Yahoo")
    import yfinance as yf
    days = min(days, 59 if interval == "15m" else 729 if interval == "1h" else 9000)
    df = yf.Ticker(fut).history(period=f"{days}d", interval=interval, auto_adjust=False)
    if df.empty: raise RuntimeError(f"no data for {fut}")
    return df[["Open", "High", "Low", "Close", "Volume"]].dropna()


def fetch_alpaca(sym, interval, days):
    start = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    hdr = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET"]}
    rows, tok = [], None
    while True:
        q = {"timeframe": BARS[interval][0], "start": start, "limit": 10000, "adjustment": "all",
             "feed": os.getenv("ALPACA_FEED", "iex"), **({"page_token": tok} if tok else {})}
        r = requests.get(f"https://data.alpaca.markets/v2/stocks/{sym}/bars", headers=hdr, params=q, timeout=30)
        r.raise_for_status(); j = r.json()
        rows += j.get("bars") or []
        if not (tok := j.get("next_page_token")): break
    if not rows: raise RuntimeError(f"no Alpaca data for {sym}")
    df = pd.DataFrame(rows).rename(columns=dict(t="Date", o="Open", h="High", l="Low", c="Close", v="Volume"))
    return df.set_index(pd.to_datetime(df.Date))[["Open", "High", "Low", "Close", "Volume"]]


def closed(df, interval):
    """Drop the still-forming last bar."""
    end = df.index[-1] + pd.Timedelta(minutes=BARS[interval][1])
    return df.iloc[:-1] if end > pd.Timestamp.now(tz=df.index.tz or "UTC") else df


# ---------------- indicators & signals ----------------
def rsi(c, n):
    d = c.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def indicators(df, n=20):
    d = df.copy(); c, h, l = d.Close, d.High, d.Low
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    d["atr"] = tr.ewm(alpha=1 / 14, adjust=False).mean()
    mid, sd = c.rolling(n).mean(), c.rolling(n).std()
    d["sq"] = (2 * sd < 1.5 * tr.rolling(n).mean()).fillna(False)  # Bollinger(2) inside Keltner(1.5)
    d["sq_bars"] = d.sq.groupby((~d.sq).cumsum()).cumsum()
    base = (c - ((h.rolling(n).max() + l.rolling(n).min()) / 2 + mid) / 2).to_numpy()
    x = np.arange(n); xm = x.mean()
    w = 1 / n + (x - xm) * (n - 1 - xm) / ((x - xm) ** 2).sum()  # linreg endpoint weights
    mom = np.full(len(d), np.nan)
    if len(d) >= n: mom[n - 1:] = swv(base, n) @ w
    d["mom"] = mom
    d["ema"] = c.ewm(span=50, adjust=False).mean()
    d["rsi"], d["rsi2"] = rsi(c, 14), rsi(c, 2)
    d["bbz"] = (c - mid) / sd                                   # distance from mean in std devs
    d["volp"] = (d.atr / c).rolling(500, min_periods=100).rank(pct=True)  # volatility regime percentile
    return d


def signals(d, p):
    c, ema, mom = d.Close, d.ema, d.mom
    up, dn = (c > ema, c < ema) if p.get("trend") else (True, True)
    if p["strategy"] == "squeeze":
        rel = (d.sq.shift(fill_value=False) & ~d.sq & (d.sq_bars.shift() >= p["min_sq"]))
        recent = rel.astype(int).rolling(3, min_periods=1).max().astype(bool) & ~d.sq
        L = recent & (mom > 0) & (mom > mom.shift()) & up
        S = recent & (mom < 0) & (mom < mom.shift()) & dn
    elif p["strategy"] == "breakout":
        N = p["lookback"]
        L = (c > d.High.rolling(N).max().shift()) & up
        S = (c < d.Low.rolling(N).min().shift()) & dn
    elif p["strategy"] == "fade":  # buy stretched lows / sell stretched highs, once momentum turns
        L = (d.bbz.shift() < -p["k"]) & (c > c.shift()) & (d.rsi < 35)
        S = (d.bbz.shift() > p["k"]) & (c < c.shift()) & (d.rsi > 65)
    else:  # rsi2 pullback in trend
        L = (c > ema) & (d.rsi2 < p["lo"])
        S = (c < ema) & (d.rsi2 > 100 - p["lo"])
    if p.get("volcap"):  # skip entries in extreme volatility spikes
        ok = ~(d.volp > p["volcap"]); L, S = L & ok, S & ok
    return L.to_numpy(bool), S.to_numpy(bool)


def open_pos(side, px, atr, p):
    return dict(side=side, entry=px, stop=px - side * p["stop"] * atr, tgt=px + side * p["tgt"] * atr, best=px, n=0)


def step(pos, hi, lo, cl, atr, p):
    """Advance an open trade one bar. Returns (reason, exit_price) or (None, None)."""
    s = pos["side"]; pos["n"] += 1
    if (lo <= pos["stop"]) if s > 0 else (hi >= pos["stop"]): return "STOP", pos["stop"]
    if (hi >= pos["tgt"]) if s > 0 else (lo <= pos["tgt"]): return "TARGET", pos["tgt"]
    if pos["n"] >= p["hold"]: return "TIME", cl
    pos["best"] = max(pos["best"], hi) if s > 0 else min(pos["best"], lo)
    if p["trail"]:
        t = pos["best"] - s * p["trail"] * atr
        if s * (t - pos["stop"]) > 0: pos["stop"] = t
    return None, None


def simulate(d, p, L, S, a=0, b=None):
    c, h, l, atr = (d[k].to_numpy(float) for k in ("Close", "High", "Low", "atr"))
    b = len(c) if b is None else b
    sig = np.flatnonzero((L | S)[:b]); out = []; i = max(a, 60)
    while True:
        k = np.searchsorted(sig, i)
        if k >= len(sig): break
        i = sig[k]
        pos = open_pos(1 if L[i] else -1, c[i], atr[i], p)
        for j in range(i + 1, b):
            r, px = step(pos, h[j], l[j], c[j], atr[j], p)
            if r: out.append(pos["side"] * (px - pos["entry"]) / pos["entry"] * 100 - 2 * FEE); break
        else: break
        i = j + 1
    return np.array(out)


def stats(t):
    if len(t) == 0: return dict(n=0, win=0, avg=0, total=0, pf=0, dd=0, t=0)
    gl = -t[t < 0].sum(); eq = t.cumsum()
    return dict(n=len(t), win=round(float((t > 0).mean()), 2), avg=round(float(t.mean()), 3),
                total=round(float(t.sum()), 1), pf=round(float(t[t > 0].sum() / gl), 2) if gl else 9.99,
                dd=round(float((eq - np.maximum.accumulate(eq)).min()), 1),
                t=round(float(t.mean() / (t.std() + 1e-9) * np.sqrt(len(t))), 2))


# ---------------- optimize (walk-forward) ----------------
ENTRIES = ([dict(strategy="squeeze", min_sq=m, trend=t) for m in (4, 8) for t in (0, 1)]
           + [dict(strategy="breakout", lookback=n, trend=t) for n in (10, 20, 40) for t in (0, 1)]
           + [dict(strategy="rsi2", lo=x) for x in (5, 10)]
           + [dict(strategy="fade", k=k) for k in (2.0, 2.5)])
ENTRIES += [{**e, "volcap": 0.95} for e in ENTRIES]
EXITS = [dict(stop=s, tgt=g, trail=r) for s in (1.0, 1.5, 2.5) for g in (1.5, 2.5, 4.0) for r in (0, 2.5)]


def optimize():
    res = {}
    for mkt in MARKETS:
        best = None
        for iv, days in (("15m", 700), ("1h", 1500)):
            try:
                d = indicators(fetch(mkt, iv, days))
            except Exception as e:
                print(mkt, iv, "data error:", e); continue
            cut = int(len(d) * 0.7); cands = []
            for e in ENTRIES:
                L, S = signals(d, e)
                for x in EXITS:
                    p = {**e, **x, "interval": iv, "hold": HOLD[iv]}
                    tr = stats(simulate(d, p, L, S, 0, cut))
                    if tr["n"] >= 30 and tr["pf"] > 1.1: cands.append((tr["t"], p, tr, L, S))
            for _, p, tr, L, S in sorted(cands, key=lambda z: -z[0])[:5]:  # top in-sample, confirm out-of-sample
                te = stats(simulate(d, p, L, S, cut))
                if te["n"] >= 10 and te["pf"] >= 1.15 and (best is None or te["t"] > best["test"]["t"]):
                    best = {**p, "train": tr, "test": te, "bars": len(d), "src": "alpaca" if ALPACA else "yahoo"}
                    break
            print(f"{mkt} {iv}: {len(d)} bars, {len(cands)} in-sample candidates")
        res[mkt] = {**best, "status": "active"} if best else {**DEFAULT, "status": "watch"}
        print(mkt, json.dumps(res[mkt]))
    res["_updated"] = dt.datetime.now(ET).isoformat(timespec="minutes")
    json.dump(res, open(PARAMS_FILE, "w"), indent=1)


def load_params():
    try: return json.load(open(PARAMS_FILE))
    except Exception: return {}


# ---------------- context ----------------
def eia_context():
    if not (key := os.getenv("EIA_API_KEY")): return ""
    out = []
    for name, route, sid in [("Crude stocks", "petroleum/stoc/wstk", "WCESTUS1"),
                             ("Gas storage", "natural-gas/stor/wkly", "NW2_EPG0_SWO_R48_BCF")]:
        try:
            v = requests.get(f"https://api.eia.gov/v2/{route}/data/", timeout=15, params={
                "api_key": key, "frequency": "weekly", "data[0]": "value", "facets[series][]": sid,
                "sort[0][column]": "period", "sort[0][direction]": "desc", "length": 2}).json()["response"]["data"]
            out.append(f"{name}: {float(v[0]['value']) - float(v[1]['value']):+,.0f} w/w ({v[0]['period']})")
        except Exception: pass
    return "\n".join(out)


def events(now=None, hours=3):
    now = now or dt.datetime.now(ET); ev = []
    for k in range(2):
        day = (now + dt.timedelta(days=k)).date(); t = dt.datetime.combine(day, dt.time(10, 30), ET)
        if day.weekday() == 2: ev.append((t, "EIA crude inventories (WTI/Brent)"))
        if day.weekday() == 3: ev.append((t, "EIA natgas storage (NATGAS)"))
    for e in EXTRA_EVENTS:
        d, _, name = e.partition(" "); ev.append((dt.datetime.fromisoformat(d).replace(hour=9, tzinfo=ET), name))
    return [f"{n} at {t:%a %H:%M} ET" for t, n in ev if dt.timedelta(0) <= t - now <= dt.timedelta(hours=hours)]


# ---------------- notify ----------------
def notify(title, body, priority="default"):
    print(f"\n=== {title}\n{body}")
    if t := os.getenv("NTFY_TOPIC"):
        try:
            requests.post("https://ntfy.sh/", timeout=15, json={"topic": t, "title": title, "message": body,
                          "priority": {"low": 2, "default": 3, "high": 4, "urgent": 5}[priority]}).raise_for_status()
        except Exception as e: print("ntfy failed:", e)
    if (tok := os.getenv("TELEGRAM_TOKEN")) and (cid := os.getenv("TELEGRAM_CHAT_ID")):
        requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": cid, "text": f"{title}\n{body}"}, timeout=15)
    if w := os.getenv("DISCORD_WEBHOOK"):
        requests.post(w, json={"content": f"**{title}**\n{body}"}, timeout=15)


# ---------------- live ----------------
def load_state():
    try: return json.load(open(STATE_FILE))
    except Exception: return {}


def fmt_stats(p):
    s = p.get("test")
    return f"Backtest (unseen data): {s['n']} trades, {s['win']:.0%} win, PF {s['pf']}" if s else "Not validated: watch-only"


def size_txt(px, stop):
    acct = float(os.getenv("ACCOUNT_SIZE") or 10000); risk = float(os.getenv("RISK_PCT") or 1)
    sh = int(acct * risk / 100 / abs(px - stop))
    return f"Size: {sh} shares (${sh * px:,.0f}) risks {risk:g}% of ${acct:,.0f}"


def scan():
    st = load_state(); st.setdefault("pos", {}); st.setdefault("last", {}); sent = set(st.get("sent", []))
    params = load_params()
    for e in events():
        if (k := f"EV|{e}|{dt.date.today()}") not in sent:
            sent.add(k); notify("⚠️ Volatility event soon", e + "\nExpect fast moves: tighten risk or stay flat.", "high")
    for mkt in MARKETS:
        p = {**DEFAULT, **params.get(mkt, {})}; iv = p["interval"]; etf = MARKETS[mkt][1 if ALPACA else 0]
        try:
            d = indicators(closed(fetch(mkt, iv, 12 if iv == "15m" else 45), iv))
        except Exception as e:
            print(mkt, "error:", e); continue
        last = st["last"].get(mkt); idx = [i for i in range(len(d)) if str(d.index[i]) > (last or "")][-8:] or []
        if not last: idx = [len(d) - 1]
        L, S = signals(d, p)
        for i in idx:
            r = d.iloc[i]; bar = str(d.index[i])
            if pos := st["pos"].get(mkt):
                why, px = step(pos, r.High, r.Low, r.Close, r.atr, p)
                if why:
                    pnl = pos["side"] * (px - pos["entry"]) / pos["entry"] * 100
                    notify(f"🔔 {mkt} EXIT {'LONG' if pos['side'] > 0 else 'SHORT'} ({why})",
                           f"{etf} close @ ~{px:.2f}  →  {pnl:+.2f}%  (entry {pos['entry']:.2f})", "high")
                    del st["pos"][mkt]
                continue
            if p["status"] == "active" and (L[i] or S[i]) and i == len(d) - 1:
                side = 1 if L[i] else -1; pos = open_pos(side, r.Close, r.atr, p); st["pos"][mkt] = pos
                risk, rew = (abs(pos[k] - r.Close) / r.Close * 100 for k in ("stop", "tgt"))
                notify(f"🚀 {mkt} {'BUY' if side > 0 else 'SELL SHORT'} now",
                       f"{etf} ~{r.Close:.2f}  ({p['strategy']}, {iv} bars)\nStop {pos['stop']:.2f} (-{risk:.2f}%)\n"
                       f"Target {pos['tgt']:.2f} (+{rew:.2f}%)" + (f"\nTrail {p['trail']}×ATR" if p["trail"] else "")
                       + f"\nMax hold {p['hold']} bars\n{size_txt(r.Close, pos['stop'])}\n{fmt_stats(p)}", "urgent")
            elif r.sq and r.sq_bars == 6 and (k := f"SQ|{mkt}|{bar}") not in sent:
                sent.add(k); notify(f"👀 {mkt} coiling", f"{etf} {r.Close:.2f}: volatility squeezed {int(r.sq_bars)} bars. "
                                    f"Breakout likely soon; watch for entry alert.", "low")
        st["last"][mkt] = str(d.index[-1])
        print(f"{mkt} {p['status']} {p['strategy']}/{iv}: {d.index[-1]} {d.Close.iloc[-1]:.2f} sq={bool(d.sq.iloc[-1])} "
              f"mom={d.mom.iloc[-1]:+.3f} rsi={d.rsi.iloc[-1]:.0f} pos={'yes' if mkt in st['pos'] else 'no'}")
    st["sent"] = sorted(sent)[-300:]
    json.dump(st, open(STATE_FILE, "w"), indent=1, default=float)


def brief():
    params, st, lines = load_params(), load_state(), []
    for mkt in MARKETS:
        etf = MARKETS[mkt][1 if ALPACA else 0]; p = {**DEFAULT, **params.get(mkt, {})}
        try:
            d = indicators(fetch(mkt, "1h", 45)); dd = fetch(mkt, "1d", 60)
        except Exception as e:
            lines.append(f"{mkt}: data error"); continue
        r, c = d.iloc[-1], dd.Close
        chg = (r.Close / c.iloc[-2] - 1) * 100 if dd.index[-1].date() >= d.index[-1].date() else (r.Close / c.iloc[-1] - 1) * 100
        tr = (dd.High - dd.Low).tail(14).mean() / c.iloc[-1] * 100
        trend = "UP" if r.Close > r.ema and r.mom > 0 else "DOWN" if r.Close < r.ema and r.mom < 0 else "MIXED"
        pos = (st.get("pos") or {}).get(mkt)
        ptxt = f"OPEN {'LONG' if pos['side'] > 0 else 'SHORT'} @ {pos['entry']:.2f}, stop {pos['stop']:.2f}" if pos else "flat"
        lines.append(f"{mkt} ({etf}) {r.Close:.2f} {chg:+.1f}% | trend {trend} | RSI {r.rsi:.0f}"
                     f"{' | SQUEEZE ' + str(int(r.sq_bars)) + 'h' if r.sq else ''}\n"
                     f"  exp. daily move ±{tr:.1f}% | 5d range {dd.Low.tail(5).min():.2f}–{dd.High.tail(5).max():.2f}\n"
                     f"  {ptxt}"
                     f" | system: {p['status']} ({p['strategy']}/{p['interval']})")
    ev = events(hours=14); ctx = eia_context()
    notify(f"📊 Energy brief {dt.datetime.now(ET):%a %b %d}", "\n".join(lines + (["Today: " + "; ".join(ev)] if ev else []) + ([ctx] if ctx else [])))


def doctor():
    for k in ("ALPACA_KEY", "ALPACA_SECRET", "NTFY_TOPIC"):
        v = os.getenv(k, ""); print(f"{k}: set={bool(v)} len={len(v)} spaces={' ' in v}")
    if t := os.getenv("NTFY_TOPIC"):
        print("NTFY topic valid:", bool(re.fullmatch(r"[-_A-Za-z0-9]{1,64}", t)), "| first/last chars:", t[0], "...", t[-1])
        r = requests.get(f"https://ntfy.sh/{t}/json", params={"poll": 1, "since": "12h"}, timeout=15)
        msgs = [json.loads(x) for x in r.text.splitlines() if x.strip()]
        print(f"ntfy server has {len(msgs)} message(s) on this topic in last 12h:", [m.get("title") for m in msgs][-5:])
    if ALPACA:
        try: fetch_alpaca("USO", "1h", 5); print("Alpaca: OK")
        except Exception as e: print("Alpaca:", str(e)[:80])


def selftest():
    rng = np.random.default_rng(1); n = 3000
    vol = np.where((np.arange(n) // 150) % 2, 0.003, 0.012)
    c = 75 * np.exp(np.cumsum(rng.normal(0, vol)))
    df = pd.DataFrame({"Open": c, "High": c * (1 + vol), "Low": c * (1 - vol), "Close": c, "Volume": 1000},
                      index=pd.date_range("2024", periods=n, freq="h", tz="UTC"))
    d = indicators(df)
    for e in ENTRIES[::3]:
        L, S = signals(d, e); print(e, stats(simulate(d, {**e, **EXITS[4], "hold": 40}, L, S)))
    print(events(dt.datetime(2026, 11, 4, 8, 0, tzinfo=ET)))


if __name__ == "__main__":
    cmds = dict(scan=scan, brief=brief, optimize=optimize, doctor=doctor, selftest=selftest,
                testnotify=lambda: notify("✅ Swing alerts connected", "Test push. Data: " + ("Alpaca real-time" if ALPACA else "Yahoo delayed"), "high"),
                loop=lambda: [(scan(), time.sleep(int(os.getenv("LOOP_SEC", 120)))) for _ in iter(int, 1)])
    cmds.get((sys.argv[1:] or ["scan"])[0], lambda: print(__doc__))()
