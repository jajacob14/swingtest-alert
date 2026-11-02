#!/usr/bin/env python3
"""Commodity swing alerts: Brent (BNO / BZ=F), WTI (USO / CL=F), NatGas (UNG / NG=F).

Commands:
  scan      check latest closed bars, send ENTRY / EXIT / SETUP / EVENT alerts   (cron: every 15 min)
  brief     market snapshot for all three to your phone                          (cron: weekday mornings)
  optimize  grid-search 1m/5m/15m (1h fallback) per market, walk-forward validate, write params.json (daily)
  live      minute-by-minute: spike/dip, day high/low, instant stop/target, 15m strategy, pulse report
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
BARS = {"1m": ("1Min", 1), "5m": ("5Min", 5), "15m": ("15Min", 15), "1h": ("1Hour", 60), "1d": ("1Day", 1440)}
INTRADAY = ("1m", "5m")  # flat by the close, never held overnight
HOLD = {"1m": 60, "5m": 48, "15m": 32, "1h": 40, "1d": 20}  # max bars in a trade (time stop)
DEFAULT = dict(interval="1h", strategy="squeeze", min_sq=6, trend=1, stop=1.5, tgt=3.0, trail=2.5, hold=40)
EXTRA_EVENTS = [e for e in os.getenv("EXTRA_EVENTS", "").split(",") if e]  # "2026-11-30 OPEC+ meeting"
ALPACA = bool(os.getenv("ALPACA_KEY"))
COLOR = {"BRENT": ("🟢", "green_circle", 0x43A047), "WTI": ("🟠", "orange_circle", 0xFB8C00),
         "NATGAS": ("🔵", "large_blue_circle", 0x1E88E5)}


# ---------------- data ----------------
def fetch(mkt, interval, days):
    fut, etf = MARKETS[mkt]
    if ALPACA:
        try:
            return fetch_alpaca(etf, interval, days)
        except Exception as e:
            print(f"Alpaca failed ({str(e)[:70]}), falling back to Yahoo")
    import yfinance as yf
    days = min(days, {"1m": 7, "5m": 59, "15m": 59, "1h": 729}.get(interval, 9000))
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
    if p.get("interval") in INTRADAY:  # no new intraday entries in the last 15 min of the session
        late = pd.Series(d.index.tz_convert(ET).time >= dt.time(15, 45), index=d.index); L, S = L & ~late, S & ~late
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


def eod_mask(index, iv):
    if iv not in INTRADAY: return np.zeros(len(index), bool)
    day = np.asarray(index.tz_convert(ET).date)
    return np.r_[day[1:] != day[:-1], True]


def simulate(d, p, L, S, a=0, b=None):
    c, h, l, atr = (d[k].to_numpy(float) for k in ("Close", "High", "Low", "atr"))
    eod = eod_mask(d.index, p.get("interval"))
    b = len(c) if b is None else b
    sig = np.flatnonzero((L | S)[:b]); out = []; i = max(a, 60)
    while True:
        k = np.searchsorted(sig, i)
        if k >= len(sig): break
        i = sig[k]
        pos = open_pos(1 if L[i] else -1, c[i], atr[i], p)
        for j in range(i + 1, b):
            r, px = step(pos, h[j], l[j], c[j], atr[j], p)
            if not r and eod[j]: r, px = "EOD", c[j]
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


def opt_market(mkt):
    best = None
    for iv, days in (("1m", 60), ("5m", 250), ("15m", 700), ("1h", 1500)):
        if best and iv == "1h": break  # 1h only as fallback when no fast setup validates
        try:
            d = indicators(fetch(mkt, iv, days))
        except Exception as e:
            print(mkt, iv, "data error:", e); continue
        cut = int(len(d) * 0.7); cands = []
        for e in ENTRIES:
            L, S = signals(d, {**e, "interval": iv})
            for x in EXITS:
                p = {**e, **x, "interval": iv, "hold": HOLD[iv]}
                tr = stats(simulate(d, p, L, S, 0, cut))
                if tr["n"] >= 30 and tr["pf"] > 1.1: cands.append((tr["t"], p, tr, L, S))
        for _, p, tr, L, S in sorted(cands, key=lambda z: -z[0])[:5]:  # top in-sample, confirm out-of-sample
            te = stats(simulate(d, p, L, S, cut))
            if te["n"] >= 15 and te["pf"] >= 1.15 and (best is None or te["t"] > best["test"]["t"]):
                days_test = max(1, (d.index[-1] - d.index[cut]).days * 5 / 7)
                best = {**p, "train": tr, "test": te, "trades_per_day": round(te["n"] / days_test, 1),
                        "bars": len(d), "src": "alpaca" if ALPACA else "yahoo"}
                break
        print(f"{mkt} {iv}: {len(d)} bars, {len(cands)} candidates, best so far: {best and best['interval']}", flush=True)
    return mkt, ({**best, "status": "active"} if best else {**DEFAULT, "status": "watch"})


def optimize():
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(3) as ex:
        res = dict(ex.map(opt_market, MARKETS))
    for m, p in res.items(): print(m, json.dumps(p))
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
def notify(title, body, priority="default", mkt=None):
    dot, tag, hexc = COLOR.get(mkt, ("⚪", "white_circle", 0x9E9E9E))
    title = f"{dot} {title}" if mkt else title
    print(f"\n=== {title}\n{body}")
    if t := os.getenv("NTFY_TOPIC"):
        try:
            requests.post("https://ntfy.sh/", timeout=15, json={"topic": t, "title": title, "message": body, "tags": [tag],
                          "priority": {"low": 2, "default": 3, "high": 4, "urgent": 5}[priority]}).raise_for_status()
        except Exception as e: print("ntfy failed:", e)
    if (tok := os.getenv("TELEGRAM_TOKEN")) and (cid := os.getenv("TELEGRAM_CHAT_ID")):
        requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", json={"chat_id": cid, "text": f"{title}\n{body}"}, timeout=15)
    if w := os.getenv("DISCORD_WEBHOOK"):
        requests.post(w, json={"embeds": [{"title": title, "description": body, "color": hexc}]}, timeout=15)


# ---------------- live ----------------
def load_state():
    try: return json.load(open(STATE_FILE))
    except Exception: return {}


def fmt_stats(p):
    s = p.get("test")
    return f"Backtest (unseen data): {s['n']} trades, {s['win']:.0%} win, PF {s['pf']}" if s else "Not validated: watch-only"


def size_txt(px, stop):
    acct = float(os.getenv("ACCOUNT_SIZE") or 10000); risk = float(os.getenv("RISK_PCT") or 1)
    sh = int(min(acct * risk / 100 / abs(px - stop), acct / px))  # 1% risk, never more than the account
    return f"Size: {sh} shares (${sh * px:,.0f}) risks {risk:g}% of ${acct:,.0f}"


# ---------------- Kalshi (all prices shown in Kalshi terms) ----------------
KALSHI = "https://api.elections.kalshi.com/trade-api/v2"
KSERIES = {"BRENT": ["KXBRENTD"], "WTI": ["KXWTIH", "KXWTI"], "NATGAS": ["KXNATGASD"]}
NAME = {"BRENT": "BRENT", "WTI": "WTI", "NATGAS": "NAT GAS"}
REASON = {"STOP": "hit your stop: cut the loss", "TARGET": "hit the target 🎯", "TIME": "idea timed out",
          "END OF DAY": "market closing soon"}
_KC = {}


def money(mkt, x): return f"${x:.3f}" if mkt == "NATGAS" else f"${x:.2f}"


def implied(rows):
    """Price where Kalshi YES is ~50¢ = the market's live price estimate."""
    pts = [(r["k"], (r["yb"] + r["ya"]) / 2) for r in rows if r["ya"] > 0]
    for (k1, p1), (k2, p2) in zip(pts, pts[1:]):
        if p1 >= 0.5 >= p2 and p1 != p2: return k1 + (p1 - 0.5) / (p1 - p2) * (k2 - k1)


def kalshi_book(mkt, min_left=8):
    """Soonest-closing open Kalshi event for this market (≥8 min left) with strikes + implied price. Cached 60s."""
    key = f"{mkt}|{min_left}"
    if (c := _KC.get(key)) and time.time() - c["t"] < 60: return c
    now, evs = pd.Timestamp.now(tz="UTC"), {}
    for ser in KSERIES[mkt]:
        try:
            ms = requests.get(f"{KALSHI}/markets", params={"series_ticker": ser, "status": "open", "limit": 300},
                              timeout=15).json().get("markets", [])
        except Exception: continue
        for m in ms:
            if m.get("strike_type") != "greater" or m.get("floor_strike") is None: continue
            close = pd.Timestamp(m["close_time"])
            if close - now < pd.Timedelta(minutes=min_left): continue
            f = lambda k: float(m.get(k) or 0)
            evs.setdefault((close, m["event_ticker"]), []).append(
                dict(k=float(m["floor_strike"]), yb=f("yes_bid_dollars"), ya=f("yes_ask_dollars"), na=f("no_ask_dollars")))
    for (close, ev), rows in sorted(evs.items()):
        rows.sort(key=lambda r: r["k"])
        if px := implied(rows):
            _KC[key] = dict(event=ev, close=close, rows=rows, px=px, t=time.time()); return _KC[key]


def kconv(mkt, etf_now):
    """Function that turns a fund (ETF) price level into the matching Kalshi price."""
    b = kalshi_book(mkt) if os.getenv("KALSHI", "1") == "1" else None
    r = b["px"] / etf_now if b else 1.0
    return lambda x: money(mkt, x * r)


def kalshi_pick(mkt, up, min_left=8):
    b = kalshi_book(mkt, min_left) or kalshi_book(mkt)
    if not b: return "(no open Kalshi contract right now)"
    when = b["close"].tz_convert(ET).strftime("%-I:%M %p")
    if up: r, side, cost = next(((r, "YES", r["ya"]) for r in b["rows"] if r["k"] > b["px"] and 0 < r["ya"] < 1), (None,) * 3)
    else: r, side, cost = next(((r, "NO", r["na"]) for r in reversed(b["rows"]) if r["k"] < b["px"] and 0 < r["na"] < 1), (None,) * 3)
    if not r: return "(no good Kalshi strike right now)"
    return f'👉 BUY {side} · "Above {money(mkt, r["k"])}" · {when}\n    cost {cost * 100:.0f}¢ → pays $1 if right'


def hold_txt(p):
    m = p["hold"] * BARS[p["interval"]][1]
    return f"{m} min" if m < 90 else f"{m / 60:.0f} hrs"


def process(mkt, d, p, st, sent):
    """Run strategy on closed bars d (with indicators): manage open trade or alert a fresh entry."""
    iv = p["interval"]; st.setdefault("pos", {}); st.setdefault("last", {})
    last = st["last"].get(mkt)
    idx = [i for i in range(len(d)) if str(d.index[i]) > last][-8:] if last else [len(d) - 1]
    L, S = signals(d, p); eod = eod_mask(d.index, iv); lv = kconv(mkt, d.Close.iloc[-1])
    for i in idx:
        r = d.iloc[i]; bar = str(d.index[i])
        if pos := st["pos"].get(mkt):
            why, px = step(pos, r.High, r.Low, r.Close, r.atr, p)
            if not why and iv in INTRADAY and (eod[i] and i < len(d) - 1 or d.index[i].tz_convert(ET).time() >= dt.time(15, 55)):
                why, px = "END OF DAY", r.Close
            if why:
                exit_alert(mkt, pos, px, why, lv); del st["pos"][mkt]
            continue
        if p["status"] == "active" and (L[i] or S[i]) and i == len(d) - 1:
            side = 1 if L[i] else -1; pos = open_pos(side, r.Close, r.atr, p); pos["interval"] = iv; st["pos"][mkt] = pos
            t = p.get("test") or {}
            notify(f"{NAME[mkt]}  {'⬆️ BET UP' if side > 0 else '⬇️ BET DOWN'}",
                   f"Now: {lv(r.Close)}\n{kalshi_pick(mkt, side > 0, min(p['hold'] * BARS[iv][1], 180))}\n"
                   f"🎯 Profit zone: {lv(pos['tgt'])}\n🛑 Sell the bet if it hits {lv(pos['stop'])}\n"
                   f"⏱ Good for about {hold_txt(p)}"
                   + (f"\n📊 Past results: wins {t['win']:.0%}, winners bigger than losers" if t else ""), "urgent", mkt)
        elif iv not in INTRADAY and r.sq and r.sq_bars == 6 and (k := f"SQ|{mkt}|{bar}") not in sent:
            sent.add(k); notify(f"{NAME[mkt]}  👀 BIG MOVE BREWING",
                                f"Now: {lv(r.Close)}\nPrice is unusually quiet; a sharp move often follows.\n"
                                f"Don't bet yet. Wait for BET UP / BET DOWN.", "low", mkt)
    st["last"][mkt] = str(d.index[-1])


def exit_alert(mkt, pos, px, why, lv):
    pnl = s_pnl(pos, px); good = pnl > 0
    notify(f"{NAME[mkt]}  {'✅' if good else '🛑'} SELL YOUR {'UP' if pos['side'] > 0 else 'DOWN'} BET NOW",
           f"Now: {lv(px)}\nWhy: {REASON.get(why, why.lower())}\nMove since entry: {pnl:+.2f}% {'👍' if good else '👎'}",
           "urgent", mkt)


def scan(only=None):
    st = load_state(); sent = set(st.get("sent", [])); params = load_params()
    for e in events():
        if (k := f"EV|{e}|{dt.date.today()}") not in sent:
            sent.add(k); notify("📅 BIG REPORT TODAY", e + "\nExpect sudden jumps around that time.", "high")
    for mkt in only or MARKETS:
        p = {**DEFAULT, **params.get(mkt, {})}; iv = p["interval"]
        try:
            d = indicators(closed(fetch(mkt, iv, {"1m": 5, "5m": 10, "15m": 12}.get(iv, 45)), iv))
        except Exception as e:
            print(mkt, "error:", e); continue
        process(mkt, d, p, st, sent)
        print(f"{mkt} {p['status']} {p['strategy']}/{iv}: {d.index[-1]} {d.Close.iloc[-1]:.2f} sq={bool(d.sq.iloc[-1])} "
              f"mom={d.mom.iloc[-1]:+.3f} rsi={d.rsi.iloc[-1]:.0f} pos={'yes' if mkt in st['pos'] else 'no'}")
    st["sent"] = sorted(sent)[-300:]
    json.dump(st, open(STATE_FILE, "w"), indent=1, default=float)


def brief():
    params, st, lines = load_params(), load_state(), []
    for mkt in MARKETS:
        try:
            d = indicators(fetch(mkt, "1h", 45)); dd = fetch(mkt, "1d", 60)
        except Exception:
            lines.append(f"{COLOR[mkt][0]} {NAME[mkt]}: no data"); continue
        r, c = d.iloc[-1], dd.Close; lv = kconv(mkt, r.Close)
        prev = c.iloc[-2] if dd.index[-1].date() >= d.index[-1].date() else c.iloc[-1]
        chg = (r.Close / prev - 1) * 100
        rng = (dd.High - dd.Low).tail(14).mean() / c.iloc[-1] * 100
        trend = "UP ↗️" if r.Close > r.ema and r.mom > 0 else "DOWN ↘️" if r.Close < r.ema and r.mom < 0 else "SIDEWAYS ➡️"
        pos = (st.get("pos") or {}).get(mkt)
        lines.append(f"{COLOR[mkt][0]} {NAME[mkt]}  {lv(r.Close)}  {'▲' if chg >= 0 else '▼'}{abs(chg):.1f}%\n"
                     f"    Trend: {trend}\n    Usual daily swing: ±{rng:.1f}%"
                     + ("\n    ⚡ Quiet → big move likely" if r.sq else "")
                     + (f"\n    You have an open {'UP' if pos['side'] > 0 else 'DOWN'} bet" if pos else ""))
    ev = events(hours=14)
    notify(f"📋 Market check · {dt.datetime.now(ET):%-I:%M %p}", "\n\n".join(lines + ([f"📅 Today: " + "; ".join(ev)] if ev else [])))


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


# ---------------- live (minute-by-minute) ----------------
MINMOVE = {"BRENT": 0.35, "WTI": 0.35, "NATGAS": 0.7}  # min % move in 5 min to count as a spike/dip
LIVE_OPEN, LIVE_CLOSE = dt.time(9, 25), dt.time(16, 5)


def fetch_1m(since):
    hdr = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET"]}
    out, tok = {}, None
    while True:
        q = {"symbols": ",".join(v[1] for v in MARKETS.values()), "timeframe": "1Min", "limit": 10000,
             "start": since.strftime("%Y-%m-%dT%H:%M:%SZ"), "feed": os.getenv("ALPACA_FEED", "iex"),
             **({"page_token": tok} if tok else {})}
        r = requests.get("https://data.alpaca.markets/v2/stocks/bars", headers=hdr, params=q, timeout=20)
        r.raise_for_status(); j = r.json()
        for sym, rows in (j.get("bars") or {}).items(): out.setdefault(sym, []).extend(rows)
        if not (tok := j.get("next_page_token")): break
    res = {}
    for sym, rows in out.items():
        df = pd.DataFrame(rows).rename(columns=dict(t="Date", o="Open", h="High", l="Low", c="Close", v="Volume"))
        res[sym] = df.set_index(pd.to_datetime(df.Date))[["Open", "High", "Low", "Close", "Volume"]]
    return res


def persist(msg="bot: live state"):
    if os.getenv("GIT_PERSIST"):
        import subprocess as sp
        sp.run(f'git add state.json && (git diff --cached --quiet || (git commit -qm "{msg}" && git pull -q --rebase origin main && git push -q))',
               shell=True)


def resample(m, n):
    if n == 1: return m
    b = m.resample(f"{n}min", label="left", closed="left").agg(
        {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}).dropna()
    return b[b.index + pd.Timedelta(minutes=n) <= pd.Timestamp.now(tz="UTC")]


def fast_checks(mkt, m, st, cool):
    """1-minute detectors: spikes/dips, trend flips, pre-move, day high/low, live stop/target hits."""
    now = time.time()
    def fire(kind, title, body, pr="high", mins=15):
        if now - cool.get((mkt, kind), 0) > mins * 60:
            cool[(mkt, kind)] = now; notify(f"{NAME[mkt]}  {title}", body, pr, mkt)
    c = m.Close; px = c.iloc[-1]
    if len(c) < 60: return
    lv = kconv(mkt, px)
    sig = np.log(c).diff().tail(780).std()
    r5 = np.log(px / c.iloc[-6]); z = r5 / (sig * np.sqrt(5) + 1e-12)
    if abs(z) >= 2.5 and abs(r5) * 100 >= MINMOVE[mkt]:
        up, wild = r5 > 0, abs(z) > 4.5
        fire("spike", f"{'⚡ JUMPED' if up else '🩸 DROPPED'} {abs(r5) * 100:.1f}% in 5 min",
             f"Now: {lv(px)}\n" + (f"Very stretched; it often snaps back. Don't chase.\nBounce idea:\n{kalshi_pick(mkt, not up)}"
                                    if wild else f"Strong push; it may keep going.\nRide it:\n{kalshi_pick(mkt, up)}"), "urgent", 10)
    b5 = resample(m, 5)
    if len(b5) > 60:
        d5 = indicators(b5); r, pr = d5.iloc[-1], d5.iloc[-2]; vr3 = m.Volume.tail(3).mean() / (m.Volume.tail(390).mean() + 1e-9)
        e9, e21 = b5.Close.ewm(span=9, adjust=False).mean(), b5.Close.ewm(span=21, adjust=False).mean()
        x_now, x_prev = np.sign(e9.iloc[-1] - e21.iloc[-1]), np.sign(e9.iloc[-2] - e21.iloc[-2])
        if x_now != x_prev and x_now * r.mom > 0:
            up = x_now > 0
            fire("trend", f"{'↗️ TURNING UP' if up else '↘️ TURNING DOWN'}",
                 f"Now: {lv(px)}\nShort-term trend just flipped {'up' if up else 'down'}.\nPossible bet:\n{kalshi_pick(mkt, up)}", "high", 20)
        bias = "UP" if r.mom > 0 and r.mom > pr.mom else "DOWN" if r.mom < 0 and r.mom < pr.mom else None
        if r.sq and r.sq_bars >= 6 and vr3 > 1.5 and bias:
            fire("premove", f"🎯 MOVE COMING · leaning {bias}",
                 f"Now: {lv(px)}\nPrice coiled tight and buyers/sellers are waking up.\nGet ready:\n{kalshi_pick(mkt, bias == 'UP')}", "high", 30)
    et = m.index.tz_convert(ET); today = m[et.date == et[-1].date()]
    if len(today) > 30:
        prev = today.iloc[:-1]
        if px > prev.High.max(): fire("hod", "📈 NEW HIGH for today", f"Now: {lv(px)}  (old high {lv(prev.High.max())})", "default", 30)
        if px < prev.Low.min(): fire("lod", "📉 NEW LOW for today", f"Now: {lv(px)}  (old low {lv(prev.Low.min())})", "default", 30)
    if pos := st.get("pos", {}).get(mkt):
        s, hi, lo = pos["side"], m.High.iloc[-1], m.Low.iloc[-1]
        hit = ("STOP", pos["stop"]) if (lo <= pos["stop"] if s > 0 else hi >= pos["stop"]) else \
              ("TARGET", pos["tgt"]) if (hi >= pos["tgt"] if s > 0 else lo <= pos["tgt"]) else None
        if hit:
            exit_alert(mkt, pos, hit[1], hit[0], lv); del st["pos"][mkt]; return True
        if abs(px - pos["stop"]) < 0.25 * abs(pos["entry"] - pos["stop"]):
            fire("nearstop", "⚠️ CLOSE TO YOUR STOP", f"Now: {lv(px)}\nStop: {lv(pos['stop'])}\nBe ready to sell the bet.", "high", 30)


def pulse(data, st):
    lines = []
    for mkt, (_, etf) in MARKETS.items():
        if (m := data.get(etf)) is None or len(m) < 20: continue
        c = m.Close; et = m.index.tz_convert(ET); y = m[et.date < et[-1].date()]; lv = kconv(mkt, c.iloc[-1])
        day = (c.iloc[-1] / y.Close.iloc[-1] - 1) * 100 if len(y) else 0
        m15 = (c.iloc[-1] / c.iloc[-16] - 1) * 100
        arrow = "↗️" if m15 > 0.1 else "↘️" if m15 < -0.1 else "➡️"
        pos = st.get("pos", {}).get(mkt)
        lines.append(f"{COLOR[mkt][0]} {NAME[mkt]:<8}{lv(c.iloc[-1]):>9}  {arrow} {'▲' if day >= 0 else '▼'}{abs(day):.1f}%"
                     + (f"\n     your {'UP' if pos['side'] > 0 else 'DOWN'} bet: {s_pnl(pos, c.iloc[-1]):+.1f}%" if pos else ""))
    if lines: notify(f"📡 Check-in · {dt.datetime.now(ET):%-I:%M %p}", "\n".join(lines) + "\n(arrow = last 15 min)", "low")


def s_pnl(pos, px): return pos["side"] * (px - pos["entry"]) / pos["entry"] * 100


def live():
    """Poll 1-minute bars; instant spike/dip/stop alerts; run strategy at each 15m bar close; pulse report."""
    if not ALPACA: sys.exit("live mode needs ALPACA_KEY / ALPACA_SECRET")
    t0, maxmin, pulse_min = time.time(), float(os.getenv("LIVE_MAX_MIN") or 1e9), int(os.getenv("PULSE_MIN") or 5)
    cool, data, last_scan, last_pulse, params = {}, {}, None, None, load_params()
    print(f"live mode: max {maxmin} min, pulse every {pulse_min} min")
    while (time.time() - t0) / 60 < maxmin:
        now = dt.datetime.now(ET)
        if now.weekday() >= 5 or not (LIVE_OPEN <= now.time() <= LIVE_CLOSE):
            if os.getenv("LIVE_MAX_MIN") and now.time() > LIVE_CLOSE: print("market closed, exiting"); break
            time.sleep(60); continue
        try:
            since = min((d.index[-1] for d in data.values()), default=None)
            since = (since - pd.Timedelta(minutes=3)) if since is not None else pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=7)
            for sym, df in fetch_1m(since).items():
                data[sym] = pd.concat([data.get(sym), df]).pipe(lambda x: x[~x.index.duplicated(keep="last")]).tail(6000)
            st = load_state(); changed = False
            for e in events(hours=0.25):
                if (k := f"EV15|{e}|{now.date()}") not in st.setdefault("sent", []):
                    st["sent"].append(k); notify("⏰ REPORT IN 15 MIN", e + "\nPrices can jump hard. Avoid new bets until after.", "urgent")
            for mkt, (_, etf) in MARKETS.items():
                if etf in data:
                    m = data[etf]; m = m[m.index + pd.Timedelta(minutes=1) <= pd.Timestamp.now(tz="UTC")]  # closed 1m bars
                    changed |= bool(fast_checks(mkt, m, st, cool))
            sent = set(st.get("sent", []))
            for mkt, (_, etf) in MARKETS.items():  # strategy on every closed bar, built from live 1-min data
                p = {**DEFAULT, **params.get(mkt, {})}; n = BARS[p["interval"]][1]
                if n <= 15 and etf in data:
                    m = data[etf]; b = resample(m[m.index + pd.Timedelta(minutes=1) <= pd.Timestamp.now(tz="UTC")], n)
                    if len(b) > 60 and str(b.index[-1]) != st.get("last", {}).get(mkt):
                        had = mkt in st.get("pos", {}); process(mkt, indicators(b), p, st, sent)
                        changed |= had != (mkt in st.get("pos", {}))
            st["sent"] = sorted(sent)[-300:]
            json.dump(st, open(STATE_FILE, "w"), indent=1, default=float)
            if changed: persist("bot: live trade")
            if now.minute < 3 and now.hour != last_scan and now.second >= 20:  # hourly: refresh params + 1h strategies
                last_scan = now.hour
                if os.getenv("GIT_PERSIST"): os.system("git pull -q --rebase origin main"); params = load_params()
                hourly = [k for k in MARKETS if BARS[{**DEFAULT, **params.get(k, {})}["interval"]][1] > 15]
                if hourly: scan(hourly); persist()
            if pulse_min and (last_pulse is None or (now - last_pulse).total_seconds() >= pulse_min * 60):
                last_pulse = now; pulse(data, load_state())
        except Exception as e:
            print("live error:", e)
        time.sleep(max(5, 62 - dt.datetime.now().second))  # wake ~2s after each new minute
    persist()


def kalshi_discover():
    ser = requests.get(f"{KALSHI}/series", timeout=30).json().get("series", [])
    for x in ser:
        t = (x.get("title") or "").lower()
        if re.search(r"(natural gas|natgas|brent|wti)", t) and x.get("frequency") in ("daily", "weekly", "hourly"):
            ms = requests.get(f"{KALSHI}/markets", params={"series_ticker": x["ticker"], "status": "open", "limit": 200}, timeout=30).json().get("markets", [])
            print("SERIES", x["ticker"], "|", x.get("title"), "|", x.get("frequency"), "| open markets:", len(ms))
            if ms:
                m = ms[0]; print("   KEYS", sorted(k for k in m if "price" in k or "bid" in k or "ask" in k or "time" in k or "strike" in k))
                print("   SAMPLE", {k: m.get(k) for k in ("ticker", "event_ticker", "yes_sub_title", "floor_strike", "cap_strike", "strike_type",
                      "yes_bid_dollars", "yes_ask_dollars", "last_price_dollars", "close_time", "volume")})
                print("   RULES", (m.get("rules_primary") or "")[:300])
                print("   EVENTS", sorted({z["event_ticker"] for z in ms})[:6])


def kcheck():
    for mkt in MARKETS:
        for ml in (8, 180):
            b = kalshi_book(mkt, ml)
            if b: print("KCHK", mkt, ml, b["event"], b["close"], "implied", round(b["px"], 3),
                        [(r["k"], r["yb"], r["ya"]) for r in b["rows"] if abs(r["k"] - b["px"]) < b["px"] * 0.01][:6])
        dd = fetch(mkt, "1d", 10); print("KCHK", mkt, "ETF daily closes", [(str(i.date()), round(v, 2)) for i, v in dd.Close.tail(4).items()])


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
                testnotify=lambda: [notify(f"{m} test alert", f"Color check for {m} ({MARKETS[m][1]}). Data: "
                                       + ("Alpaca real-time" if ALPACA else "Yahoo delayed"), "high", m) for m in MARKETS],
                live=live, kalshi=kalshi_discover, kcheck=kcheck, loop=lambda: [(scan(), time.sleep(int(os.getenv("LOOP_SEC", 120)))) for _ in iter(int, 1)])
    cmds.get((sys.argv[1:] or ["scan"])[0], lambda: print(__doc__))()
