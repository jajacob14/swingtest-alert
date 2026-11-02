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
import json, os, re, sys, time, datetime as dt
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
FAST_DEFAULT = dict(strategy="ignite", z=2.5, look=30, vr=1.5, stop=1.5, tgt=8.0, trail=1.5, interval="1m", hold=30)
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
    et = d.index.tz_convert(ET); day = pd.Series(et.date, index=d.index)
    d["tod"] = et.hour * 60 + et.minute; d["dow"] = et.weekday
    vol = d.Volume.where(d.Volume > 0, 1.0); tp = (h + l + c) / 3
    d["vwap"] = (tp * vol).groupby(day).cumsum() / vol.groupby(day).cumsum()   # session VWAP
    d["vwz"] = (c - d.vwap) / d.atr                                             # distance from VWAP in ATRs
    d["ema200"] = c.ewm(span=200, adjust=False).mean()                          # higher-timeframe trend
    d["sma20"] = c.rolling(20).mean()
    first30 = (d.tod >= 570) & (d.tod < 600)                                     # 9:30-10:00 ET opening range
    d["orh"] = h.where(first30).groupby(day).cummax().groupby(day).ffill()
    d["orl"] = l.where(first30).groupby(day).cummin().groupby(day).ffill()
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
    elif p["strategy"] == "ignite":  # spike starting: sharp 3-bar push out of a quiet range on rising volume
        ret = np.log(c).diff(); sig = ret.rolling(390, min_periods=60).std()
        z3 = np.log(c / c.shift(3)) / (sig * np.sqrt(3))
        hh, ll = d.High.rolling(p["look"]).max().shift(3), d.Low.rolling(p["look"]).min().shift(3)
        vr = d.Volume.rolling(3).mean() / (d.Volume.rolling(390, min_periods=60).mean() + 1e-9)
        L = (z3 > p["z"]) & (c > hh) & (vr > p["vr"])
        S = (z3 < -p["z"]) & (c < ll) & (vr > p["vr"])
    elif p["strategy"] == "orb":  # opening-range breakout: first close beyond the 9:30-10:00 range, before 3pm
        win = (d.tod >= 600) & (d.tod <= 900)
        L = win & (c > d.orh) & (c.shift() <= d.orh.shift())
        S = win & (c < d.orl) & (c.shift() >= d.orl.shift())
    elif p["strategy"] == "vwapfade":  # stretched far from VWAP, turning back toward it
        L = (d.vwz.shift() < -p["k"]) & (c > c.shift())
        S = (d.vwz.shift() > p["k"]) & (c < c.shift())
    elif p["strategy"] == "smacross":  # alpacahq/example-scalping style: price crosses its 20-bar average
        L = (c > d.sma20) & (c.shift() <= d.sma20.shift()) & up
        S = (c < d.sma20) & (c.shift() >= d.sma20.shift()) & dn
    elif p["strategy"] == "fade":  # buy stretched lows / sell stretched highs, once momentum turns
        L = (d.bbz.shift() < -p["k"]) & (c > c.shift()) & (d.rsi < 35)
        S = (d.bbz.shift() > p["k"]) & (c < c.shift()) & (d.rsi > 65)
    else:  # rsi2 pullback in trend
        L = (c > ema) & (d.rsi2 < p["lo"])
        S = (c < ema) & (d.rsi2 > 100 - p["lo"])
    if p.get("interval") in INTRADAY:  # no new intraday entries in the last 15 min of the session
        late = pd.Series(d.index.tz_convert(ET).time >= dt.time(15, 45), index=d.index); L, S = L & ~late, S & ~late
    if p.get("vw"):   # trade with VWAP: longs only above it, shorts only below
        L, S = L & (c > d.vwap), S & (c < d.vwap)
    if p.get("htf"):  # align with the higher-timeframe trend (EMA200)
        L, S = L & (c > d.ema200), S & (c < d.ema200)
    if p.get("tod") and p.get("interval") in ("1m", "5m", "15m"):  # skip lunch chop + EIA release minutes
        bad = ((d.tod >= 690) & (d.tod < 810)) | (d.dow.isin([2, 3]) & (d.tod >= 625) & (d.tod < 645))
        L, S = L & ~bad, S & ~bad
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
           + [dict(strategy="fade", k=k) for k in (2.0, 2.5)]
           + [dict(strategy="ignite", z=z, look=lk, vr=v) for z in (2.0, 2.5, 3.0) for lk in (15, 30) for v in (1.0, 1.5)]
           + [dict(strategy="orb"), dict(strategy="smacross", trend=0), dict(strategy="smacross", trend=1)]
           + [dict(strategy="vwapfade", k=k) for k in (1.5, 2.5)])
FILTERS = [dict(vw=a, htf=b, tod=t) for a in (0, 1) for b in (0, 1) for t in (0, 1)]
ENTRIES += [{**e, "volcap": 0.95} for e in ENTRIES]
EXITS = [dict(stop=s, tgt=g, trail=r) for s in (1.0, 1.5, 2.5) for g in (1.5, 2.5, 4.0, 8.0) for r in (0, 1.5, 2.5)]
FAST_HOLD = 30  # fast trades: max 30 one-minute bars


# ---------------- longshot calibration (cheap 15-min contracts that snap back) ----------------
LS_MAX_COST, LS_MIN_EDGE = float(os.getenv("LS_MAX_COST") or 0.35), float(os.getenv("LS_MIN_EDGE") or 0.06)
LS_BUCKETS = (1.0, 2.0, 99)
FAV_MIN_EDGE = float(os.getenv("FAV_MIN_EDGE") or 0.04)


def kfee(p):
    """Kalshi taker fee per contract ($): ceil(0.07 × P × (1−P)) to the cent."""
    from math import ceil
    return ceil(7 * p * (1 - p) - 1e-9) / 100


def _phi(x):
    from math import erf, sqrt
    return 0.5 * (1 + erf(x / sqrt(2)))


def ls_bucket(dist):
    for b in LS_BUCKETS:
        if dist < b: return str(b)


def fetch_fut_1m(mkt, days=29):
    """Yahoo 1-minute FUTURES bars (what Kalshi settles on) for ~30 days, in 7-day chunks."""
    import yfinance as yf
    out, end = [], dt.datetime.now(dt.timezone.utc)
    for k in range(0, days, 7):
        e = end - dt.timedelta(days=k); b = e - dt.timedelta(days=min(7, days - k))
        df = yf.Ticker(MARKETS[mkt][0]).history(start=b, end=e, interval="1m", auto_adjust=False)
        if len(df): out.append(df[["Open", "High", "Low", "Close", "Volume"]])
    d = pd.concat(out).sort_index(); return d[~d.index.duplicated()]


def ctx_features(c, vol, index, o=None):
    """Market context per bar: 4h trend (EMA240 of 1-min), session VWAP, RSI, 5-min order-flow pressure."""
    et = index.tz_convert(ET); day = pd.Series(et.date, index=index)
    v = vol.where(vol > 0, 1.0)
    vwap = (c * v).groupby(day).cumsum() / v.groupby(day).cumsum()
    o = c.shift() if o is None else o
    flow = (np.sign(c - o) * v).rolling(5).sum() / v.rolling(5).sum()  # +1 all buying … −1 all selling
    return np.sign(c - c.ewm(span=240, adjust=False).mean()), vwap, rsi(c, 14), flow


def ctx_key(dist, bdir, trend, px, vwap, turning, flow=0.0):
    """Cell key: stretch | trend backs bounce | bounce toward VWAP | order flow backs bounce | turning or running."""
    tr = "T+" if trend == bdir else "T-"
    vw = "V+" if (px < vwap if bdir > 0 else px > vwap) else "V-"
    fl = "F+" if flow * bdir > 0 else "F-"
    return f"{ls_bucket(dist)}|{tr}|{vw}|{fl}|{'turn' if turning else 'run'}"


def session(ts_et):
    """Trading session by ET clock: US day, evening (post-settle + 6pm reopen), Asia, Europe."""
    m = ts_et.hour * 60 + ts_et.minute
    return "US" if 570 <= m < 960 else "EVE" if 960 <= m < 1200 else "EU" if 180 <= m < 570 else "ASIA"


SESS_TXT = {"US": "US day session", "EVE": "Evening session (after settlement, 6pm reopen)",
            "ASIA": "Asian session (thin trading)", "EU": "European session (London digests overnight news)"}


def event_window(mkt, now_et, mins_ahead=15):
    """Known jumpy windows (research-based). Returns a reason string or ''."""
    end = now_et + dt.timedelta(minutes=mins_ahead); m0, wd = now_et.hour * 60 + now_et.minute, now_et.weekday()
    def hit(a, b): return a <= m0 <= b or a <= end.hour * 60 + end.minute <= b
    if events(now_et, hours=mins_ahead / 60 + 0.05): return "EIA report inside this session"
    if mkt != "NATGAS" and wd == 1 and hit(16 * 60 + 15, 17 * 60): return "API oil inventory report (Tue 4:30 PM): after-hours jumps"
    if hit(18 * 60, 18 * 60 + 30): return "6 PM reopen: thin, gappy trading"
    if mkt == "NATGAS" and (hit(23 * 60 + 15, 23 * 60 + 59) or hit(90, 150) or hit(5 * 60 + 15, 5 * 60 + 59)):
        return "Weather-model update (GFS/European): nat gas jumps on forecast changes"
    return ""


def ls_rows(df, rth=True):
    """Per 15-min window: first 'turning' and first 'running' minute (3-12 min left) where price is ≥0.5σ√T
    from the window start. won = price ended back across the start (the bounce side wins)."""
    et0 = df.index.tz_convert(ET)
    if rth: df = df[(et0.hour * 60 + et0.minute >= 570) & (et0.hour < 16)]
    df = df.resample("1min").last().dropna(how="all")
    c = df.Close; et = df.index.tz_convert(ET); w = df.index.floor("15min")
    full = pd.Series(1, index=df.index).groupby(w).transform("size") >= 8
    start = c.shift(1).groupby(w).transform("first"); end = c.groupby(w).transform("last")
    T = 14 - (et.minute % 15)
    sig = np.log(c).diff().rolling(390, min_periods=60).std()
    z = np.log(c / start) / (sig * np.sqrt(np.maximum(T, 1)))
    trend, vwap, r, flow = ctx_features(c, df.Volume.fillna(0), df.index, df.Open)
    bdir = -np.sign(z)                                       # bounce direction (back toward start)
    turning = ((bdir > 0) & (c > c.shift()) & (r < 45)) | ((bdir < 0) & (c < c.shift()) & (r > 55))
    ok = full & (T >= 3) & (T <= 12) & (z.abs() >= 0.5) & sig.notna()
    x = pd.DataFrame({"w": w, "dist": z.abs(), "won": np.where(bdir > 0, end >= start, end < start),
                      "key": [ctx_key(a, b, t, p, v, u, f) for a, b, t, p, v, u, f in zip(z.abs(), bdir, trend, c, vwap, turning, flow.fillna(0))],
                      "turn": turning,
                      "skey": [f"{session(t)}|{ls_bucket(a)}|{'T+' if tr == b else 'T-'}|{'turn' if u else 'run'}"
                               for t, a, b, tr, u in zip(et, z.abs(), bdir, trend, turning)]})[ok]
    return x.groupby(["w", "turn"]).head(1)


def ihm_stats(mkt):
    """Wen et al. (2021/2023): first half-hour return (incl. overnight) predicts the last half-hour;
    on EIA Wednesdays the third half-hour (10:30-11:00) does. Tested on ~3y of 15-min bars."""
    try:
        d = fetch(mkt, "15m", 1100)
    except Exception as e:
        return {"error": str(e)[:60]}
    et = d.index.tz_convert(ET); d = d.assign(day=et.date, tod=et.hour * 60 + et.minute)
    rows = []
    days = sorted(set(d.day)); prev_close = None
    for day in days:
        g = d[d.day == day].set_index("tod").Close
        if prev_close and all(k in g for k in (585, 615, 645, 915, 945)):  # bar starts 9:45,10:15,10:45,15:15,15:45
            wed = pd.Timestamp(day).weekday() == 2 and mkt != "NATGAS"
            sig = (g[645] / g[615] - 1) if wed else (g[585] / prev_close - 1)   # 3rd half-hour on EIA days
            rows.append((np.sign(sig), np.sign(g[945] / g[915] - 1)))
        if 945 in g: prev_close = g[945]
    if len(rows) < 60: return {"n": len(rows)}
    a = np.array(rows); same = (a[:, 0] == a[:, 1]).astype(float); cut = int(len(same) * 0.7)
    direction = 1 if same[:cut].mean() >= 0.5 else -1          # learned on older 70%: follow or reverse
    hit = same if direction > 0 else 1 - same
    res = dict(n=len(hit), dir="follow" if direction > 0 else "reverse", hit=round(float(hit.mean()), 3),
               hit_recent=round(float(hit[cut:].mean()), 3))
    res["ok"] = bool(res["hit"] >= 0.54 and res["hit_recent"] >= 0.53)
    return res


def calibrate(mkt):
    try:
        rows = ls_rows(fetch_fut_1m(mkt), rth=False); src = "yahoo futures 30d"
    except Exception as e:
        print(mkt, "futures 1m failed:", e); rows = ls_rows(fetch(mkt, "1m", 60)); src = "etf 60d"
    cut = int(len(rows) * 0.7); tr, te = rows.iloc[:cut], rows.iloc[cut:]
    tab = {k: [len(g), round(float(g.won.mean()), 3)] for k, g in tr.groupby("key") if len(g) >= 25}
    stab = {k: [len(g), round(float(g.won.mean()), 3)] for k, g in tr.groupby("skey") if len(g) >= 25}
    res = dict(table=tab, stable=stab, setups=len(rows), src=src)
    nt = te[~te.skey.str.startswith("US")]
    for typ in ("ls", "fav"):  # overnight validation on unseen 30%, session-aware table
        pnl = cost = n = 0
        for _, r in nt.iterrows():
            cell = stab.get(r.skey)
            if not cell or (typ == "ls") != bool(r.turn): continue
            fair_b = _phi(-r.dist); price = (fair_b if typ == "ls" else 1 - fair_b) + 0.02
            p = cell[1] if typ == "ls" else 1 - cell[1]; won = r.won if typ == "ls" else not r.won
            if (price <= LS_MAX_COST if typ == "ls" else price < 0.92) and p - price - kfee(price) >= (LS_MIN_EDGE if typ == "ls" else FAV_MIN_EDGE):
                pnl += won - price - kfee(price); cost += price; n += 1
        res[f"night_{typ}_n"], res[f"night_{typ}_roi"] = n, round(pnl / cost, 3) if cost else 0
        res[f"night_{typ}_ok"] = bool(n >= 15 and cost and pnl / cost > 0.03)
    res["bounce_by_session"] = {sname: round(float(g.won.mean()), 3) for sname, g in
                                rows[rows.turn].groupby(rows[rows.turn].skey.str.split("|").str[0])}
    for typ in ("ls", "fav"):  # test on unseen 30%: buy when history odds beat a fair price (+2¢ spread)
        pnl = cost = n = 0
        for _, r in te.iterrows():
            cell = tab.get(r.key)
            if not cell: continue
            fair_b = _phi(-r.dist)
            if typ == "ls" and r.turn:
                price, p, won = fair_b + 0.02, cell[1], r.won
                if price <= LS_MAX_COST and p - price - kfee(price) >= LS_MIN_EDGE: pnl += won - price - kfee(price); cost += price; n += 1
            if typ == "fav" and not r.turn:
                price, p, won = 1 - fair_b + 0.02, 1 - cell[1], not r.won
                if price < 0.97 and p - price - kfee(price) >= FAV_MIN_EDGE: pnl += won - price - kfee(price); cost += price; n += 1
        res[f"{typ}_test_n"], res[f"{typ}_test_roi"] = n, round(pnl / cost, 3) if cost else 0
        res[f"{typ}_ok"] = bool(n >= 15 and cost and pnl / cost > 0.03)
    res["active"] = True  # calls still require live Kalshi price < history odds; 'ok' flags mark tested edge
    res["ihm"] = ihm_stats(mkt)
    best = sorted(((v[1] - _phi(-float(k.split("|")[0]) * 0.75), k, v) for k, v in tab.items() if k.endswith("turn")), reverse=True)[:3]
    print(mkt, "CAL", json.dumps({k: v for k, v in res.items() if k not in ("table", "stable")}), "| best bounce cells:", best, flush=True)
    return res


def consistency(d, p, L, S, cut):
    """Split the unseen period in 3; count chunks that were profitable."""
    edges = np.linspace(cut, len(d), 4).astype(int)
    return sum(stats(simulate(d, p, L, S, a, b))["pf"] > 1 for a, b in zip(edges[:-1], edges[1:]))


def opt_market(mkt):
    best, fast = None, None
    for iv, days in (("1m", 60), ("5m", 250), ("15m", 700), ("1h", 1500)):
        if best and iv == "1h": break  # 1h only as fallback when no fast setup validates
        try:
            d = indicators(fetch(mkt, iv, days))
        except Exception as e:
            print(mkt, iv, "data error:", e); continue
        cut = int(len(d) * 0.7); cands = []
        for e in ENTRIES:
            if e["strategy"] == "ignite" and iv != "1m": continue
            if e["strategy"] == "orb" and iv not in ("1m", "5m", "15m"): continue
            L, S = signals(d, {**e, "interval": iv})
            for x in EXITS:
                p = {**e, **x, "interval": iv, "hold": FAST_HOLD if iv == "1m" else HOLD[iv]}
                tr = stats(simulate(d, p, L, S, 0, cut))
                if tr["n"] >= 30 and tr["pf"] > 1.05: cands.append((tr["t"], p, tr, L, S))
        for _, p0, *_ in sorted(cands, key=lambda z: -z[0])[:10]:  # stage 2: add VWAP / trend / time filters
            for f in FILTERS[1:]:
                p = {**p0, **f}; L, S = signals(d, p); tr = stats(simulate(d, p, L, S, 0, cut))
                if tr["n"] >= 30 and tr["pf"] > 1.05: cands.append((tr["t"], p, tr, L, S))
        days_test = max(1, (d.index[-1] - d.index[cut]).days * 5 / 7)
        for _, p, tr, L, S in sorted(cands, key=lambda z: -z[0])[:12]:  # top in-sample → must hold up out-of-sample
            te = stats(simulate(d, p, L, S, cut))
            if te["n"] < 15 or te["pf"] < 1.1: continue
            cons = consistency(d, p, L, S, cut)
            if cons < 2: continue
            row = {**p, "train": tr, "test": te, "chunks_ok": f"{cons}/3", "trades_per_day": round(te["n"] / days_test, 1), "bars": len(d)}
            if iv == "1m" and (fast is None or te["t"] > fast["test"]["t"]): fast = row
            if te["pf"] >= 1.15 and (best is None or te["t"] > best["test"]["t"]): best = row
        print(f"{mkt} {iv}: {len(d)} bars, {len(cands)} candidates, best={best and best['interval']} fast={fast and fast['strategy']}", flush=True)
    return mkt, ({**best, "status": "active"} if best else {**DEFAULT, "status": "watch"}), fast


def optimize():
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(3) as ex:
        out = list(ex.map(opt_market, MARKETS))
    res = {m: p for m, p, _ in out}
    res["_cal"] = {m: calibrate(m) for m in MARKETS}
    res["_fast"] = {m: ({**f, "status": "active"} if f else {**FAST_DEFAULT, "status": "unproven"}) for m, _, f in out}
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
    if "🟩" in title: hexc = 0x2E7D32
    elif "🟦" in title: hexc = 0x1565C0
    title = f"{dot} {title}" if mkt else title
    print(f"\n=== {title}\n{body}")
    if t := os.getenv("NTFY_TOPIC"):
        try:
            requests.post("https://ntfy.sh/", timeout=15, json={"topic": t, "title": title, "message": body,
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
_KC, _KR, _PICK = {}, {}, {}


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
                dict(k=float(m["floor_strike"]), yb=f("yes_bid_dollars"), ya=f("yes_ask_dollars"), na=f("no_ask_dollars"), tk=m["ticker"]))
    for (close, ev), rows in sorted(evs.items()):
        rows.sort(key=lambda r: r["k"])
        if px := implied(rows):
            _KC[key] = dict(event=ev, close=close, rows=rows, px=px, t=time.time()); return _KC[key]


def kconv(mkt, etf_now):
    """Function that turns a fund (ETF) price level into the matching Kalshi price."""
    b = kalshi_book(mkt) if os.getenv("KALSHI", "1") == "1" else None
    c = (0, 1.0) if not b else _KR.get(mkt)
    if b and (not c or c[0] != b["t"]): c = _KR[mkt] = (b["t"], b["px"] / etf_now)  # re-anchor only when Kalshi refreshes
    f = lambda x: money(mkt, x * c[1]); f.r = c[1]
    return f


def kalshi_pick(mkt, up, min_left=8, tgt_k=None):
    b = kalshi_book(mkt, min_left) or kalshi_book(mkt)
    if b and tgt_k:  # prefer a cheaper strike (≤40¢) between price and target = bigger payout if the move plays out
        if up: cheap = [r for r in b["rows"] if b["px"] < r["k"] <= tgt_k and 0 < r["ya"] <= 0.40]
        else: cheap = [r for r in reversed(b["rows"]) if tgt_k <= r["k"] < b["px"] and 0 < r["na"] <= 0.40]
        if cheap:
            r = cheap[0]; side, cost = ("YES", r["ya"]) if up else ("NO", r["na"])
            _PICK[mkt] = dict(ticker=r["tk"], side=side, cost=cost)
            return (f'👉 BUY {side} · "Above {money(mkt, r["k"])}" · {b["close"].tz_convert(ET).strftime("%-I:%M %p")}\n'
                    f'    cost {cost * 100:.0f}¢ → pays $1 ({1 / cost:.1f}×) if the move reaches it')
    if not b: return "(no open Kalshi contract right now)"
    when = b["close"].tz_convert(ET).strftime("%-I:%M %p")
    if up: r, side, cost = next(((r, "YES", r["ya"]) for r in b["rows"] if r["k"] > b["px"] and 0 < r["ya"] < 1), (None,) * 3)
    else: r, side, cost = next(((r, "NO", r["na"]) for r in reversed(b["rows"]) if r["k"] < b["px"] and 0 < r["na"] < 1), (None,) * 3)
    if not r: return "(no good Kalshi strike right now)"
    _PICK[mkt] = dict(ticker=r["tk"], side=side, cost=cost)
    return f'👉 BUY {side} · "Above {money(mkt, r["k"])}" · {when}\n    cost {cost * 100:.0f}¢ → pays $1 if right'


TRADES_ONLY = os.getenv("ALERTS", "trades") == "trades"
MAIN_ON = os.getenv("MAIN_SIGNALS", "0") == "1"  # slow signals use hourly/daily contracts → off; only 15-min calls  # set ALERTS=all for extra heads-up alerts


BIG_X = float(os.getenv("BIG_X") or 10)  # payout multiple that counts as a big-payout (green) bet


def badge(cost):
    """🟩 big payout (≥10× back) vs 🟦 normal bet."""
    return "🟩 BIG PAYOUT" if cost and 1 / cost >= BIG_X else "🟦"


def new_trade(st, mkt, pos, lv, px):
    st["seq"] = st.get("seq", 0) + 1
    pos.update(id=st["seq"], at=dt.datetime.now(ET).strftime("%-I:%M %p"), at_px=lv(px))
    return st["seq"]


def busy(st, mkt): return any(mkt in st.get(k, {}) for k in ("pos", "fpos", "lpos"))




K15 = {"BRENT": "KXBRENT15M", "WTI": "KXWTI15M", "NATGAS": "KXNATGAS15M"}


def k15(mkt):
    """Current Kalshi 15-minute up/down contract for this market (cached 15s)."""
    key = f"15|{mkt}"
    if (c := _KC.get(key)) and time.time() - c["t"] < 15: return c
    try:
        ms = requests.get(f"{KALSHI}/markets", params={"series_ticker": K15[mkt], "status": "open", "limit": 5}, timeout=10).json().get("markets", [])
    except Exception: return None
    if not ms: return None
    m = min(ms, key=lambda x: x["close_time"]); f = lambda k: float(m.get(k) or 0)
    _KC[key] = dict(ticker=m["ticker"], k=float(m["floor_strike"]), close=pd.Timestamp(m["close_time"]), ya=f("yes_ask_dollars"),
                    na=f("no_ask_dollars"), yb=f("yes_bid_dollars"), nb=f("no_bid_dollars"), t=time.time())
    return _KC[key]


_SIG = {}  # per-minute log volatility per market (updated live)


def fair_up(kp, strike, mins_left, sig):
    """Random-walk odds that price finishes at/above strike: Φ(ln(kp/strike) / (σ√T))."""
    from math import erf, log, sqrt
    if not sig or mins_left <= 0: return None
    z = log(kp / strike) / (sig * sqrt(mins_left))
    return 0.5 * (1 + erf(z / sqrt(2)))


def pick15(mkt, up, lv, px_etf):
    """Text + contract info for the 15-min Kalshi bet matching a fast call (with a fair-value check)."""
    lv_now = lv(px_etf); kp = px_etf * getattr(lv, "r", 1.0)
    c = k15(mkt)
    if not c: return "(no 15-min Kalshi contract open right now)", None
    left = (c["close"] - pd.Timestamp.now(tz="UTC")).total_seconds() / 60
    end = c["close"].tz_convert(ET).strftime("%-I:%M")
    side, cost = ("YES", c["ya"]) if up else ("NO", c["na"])
    head = f"⏱ Kalshi 15-min ({end} close)\nStart {money(mkt, c['k'])} · now {lv_now}"
    if left < 4:
        return head + f"\n    Too late for this one ({left:.0f} min left).\n    👉 Next window: BUY {side} right when it opens", None
    if not 0 < cost < 1: return head + "\n    (no price offered right now)", None
    fu = fair_up(kp, c["k"], left, _SIG.get(mkt))
    val = ""
    if fu is not None:
        fair = (fu if up else 1 - fu) * 100; edge = fair - cost * 100
        val = (f"\nOdds ≈{fair:.0f}% vs {cost * 100:.0f}¢ → "
               + ("✅ good value" if edge >= 3 else "⚠️ pricey" if edge <= -8 else "≈ fair price"))
    return (head + f"\n👉 BUY {side} at {cost * 100:.0f}¢ (wins if it ends {'≥' if up else '<'} start)" + val,
            dict(ticker=c["ticker"], side=side, cost=cost, k=c["k"], close=str(c["close"])))


def contract_status(info):
    """(text, verdict) from Kalshi itself: verdict True/False = contract is up/down vs entry (or won/lost)."""
    if not info: return "", None
    try:
        m = requests.get(f"{KALSHI}/markets/{info['ticker']}", timeout=10).json()["market"]
    except Exception: return "", None
    paid = info["cost"] * 100
    if m.get("result"):
        won = m["result"].lower() == info["side"].lower()
        return f"\nKalshi {info['side']}: settled {'$1 ✅' if won else '$0 ❌'} (bought at {paid:.0f}¢)", won
    bid = float(m.get("yes_bid_dollars" if info["side"] == "YES" else "no_bid_dollars") or 0) * 100
    return f"\nKalshi {info['side']}: {paid:.0f}¢ → {bid:.0f}¢ now ({bid - paid:+.0f}¢)", bid > paid


def contract_value(info): return contract_status(info)[0]


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
        if MAIN_ON and p["status"] == "active" and (L[i] or S[i]) and i == len(d) - 1 and not busy(st, mkt):
            side = 1 if L[i] else -1; pos = open_pos(side, r.Close, r.atr, p); pos["interval"] = iv; st["pos"][mkt] = pos
            t = p.get("test") or {}; _PICK.pop(mkt, None)
            pick = kalshi_pick(mkt, side > 0, min(p['hold'] * BARS[iv][1], 180), pos["tgt"] * getattr(lv, "r", 1.0)); pos["k"] = _PICK.get(mkt)
            n = new_trade(st, mkt, pos, lv, r.Close)
            notify(f"#{n} {NAME[mkt]} · {'BUY signal ⬆️ price rising' if side > 0 else 'BUY signal ⬇️ price falling'}",
                   f"Price now {lv(r.Close)}\n{pick}\n"
                   f"🎯 Exit expected near {lv(pos['tgt'])}\n🛑 Exit early if price hits {lv(pos['stop'])}\n"
                   f"⏱ Usually lasts up to {hold_txt(p)}. #{n} SELL signal will follow." 
                   + (f"\n📊 Past: {t['win']:.0%} wins, profitable overall" if t else ""), "urgent", mkt)
        elif not TRADES_ONLY and iv not in INTRADAY and r.sq and r.sq_bars == 6 and (k := f"SQ|{mkt}|{bar}") not in sent:
            sent.add(k); notify(f"{NAME[mkt]}  👀 BIG MOVE BREWING",
                                f"Now: {lv(r.Close)}\nPrice is unusually quiet; a sharp move often follows.\n"
                                f"Don't bet yet. Wait for BET UP / BET DOWN.", "low", mkt)
    st["last"][mkt] = str(d.index[-1])


def exit_alert(mkt, pos, px, why, lv):
    good = s_pnl(pos, px) > 0
    title = {"STOP": "SELL signal 🛑 move failed", "TARGET": "SELL signal 💰 target reached", "TIME": "SELL signal ⏱ move is over",
             "END OF DAY": "SELL signal ⏱ market closing"}.get(why, "SELL NOW")
    if why == "STOP" and good: title = "SELL signal 💰 take profit"
    sell_msg(mkt, pos, title, px, lv)


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
    st, lines = load_state(), []
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
                     + (f"\n    Open signal #{pos.get('id', '?')}: {'UP' if pos['side'] > 0 else 'DOWN'}" if pos else ""))
    ev = events(hours=14)
    notify(f"📋 Market check · {dt.datetime.now(ET):%-I:%M %p}", "\n\n".join(lines + (["📅 Today: " + "; ".join(ev)] if ev else [])))


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
        if TRADES_ONLY: return
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
             f"Now: {lv(px)}\n" + (f"Very stretched; it often snaps back. Don't chase.\nBounce idea:\n{pick15(mkt, not up, lv, px)[0]}"
                                    if wild else f"Strong push; it may keep going.\nRide it:\n{pick15(mkt, up, lv, px)[0]}"), "urgent", 10)
    b5 = resample(m, 5)
    if len(b5) > 60:
        d5 = indicators(b5); r, pr = d5.iloc[-1], d5.iloc[-2]; vr3 = m.Volume.tail(3).mean() / (m.Volume.tail(390).mean() + 1e-9)
        e9, e21 = b5.Close.ewm(span=9, adjust=False).mean(), b5.Close.ewm(span=21, adjust=False).mean()
        x_now, x_prev = np.sign(e9.iloc[-1] - e21.iloc[-1]), np.sign(e9.iloc[-2] - e21.iloc[-2])
        if x_now != x_prev and x_now * r.mom > 0:
            up = x_now > 0
            fire("trend", f"{'↗️ TURNING UP' if up else '↘️ TURNING DOWN'}",
                 f"Now: {lv(px)}\nShort-term trend just flipped {'up' if up else 'down'}.\nPossible bet:\n{pick15(mkt, up, lv(px))[0]}", "high", 20)
        bias = "UP" if r.mom > 0 and r.mom > pr.mom else "DOWN" if r.mom < 0 and r.mom < pr.mom else None
        if r.sq and r.sq_bars >= 6 and vr3 > 1.5 and bias:
            fire("premove", f"🎯 MOVE COMING · leaning {bias}",
                 f"Now: {lv(px)}\nPrice coiled tight and buyers/sellers are waking up.\nGet ready:\n{pick15(mkt, bias == 'UP', lv, px)[0]}", "high", 30)
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
        px = m.Close.iloc[-1]; lv = kconv(mkt, px); c = k15(mkt)
        line = f"{COLOR[mkt][0]} {NAME[mkt]}  {lv(px)}"
        if c:
            line += (f"\n    15-min ({c['close'].tz_convert(ET):%-I:%M}): start {money(mkt, c['k'])} · "
                     f"YES {c['ya'] * 100:.0f}¢ / NO {c['na'] * 100:.0f}¢")
        op = next((st[k][mkt] for k in ("lpos", "fpos", "pos") if mkt in st.get(k, {})), None)
        line += f"\n    open: signal #{op.get('id', '?')}" if op else "\n    no call yet: watching"
        lines.append(line)
    if lines: notify(f"👀 Watching · {dt.datetime.now(ET):%-I:%M %p}", "\n".join(lines), "default")


def s_pnl(pos, px): return pos["side"] * (px - pos["entry"]) / pos["entry"] * 100


def manage_fast(mkt, px, st):
    """Every tick: trail the fast trade with the live price; SELL NOW when the move stalls, fails or times out."""
    pos = st.get("fpos", {}).get(mkt)
    if not pos: return False
    s_ = pos["side"]; pos["best"] = max(pos["best"], px) if s_ > 0 else min(pos["best"], px)
    gain_atr = s_ * (pos["best"] - pos["entry"]) / pos["atr"]
    if pos["trail"] and gain_atr >= 1:  # once up ≥1 ATR, lock profit with a trailing stop
        t = pos["best"] - s_ * pos["trail"] * pos["atr"]
        if s_ * (t - pos["stop"]) > 0: pos["stop"] = t
    why = None
    if (px <= pos["stop"]) if s_ > 0 else (px >= pos["stop"]):
        why = "LOCK" if s_ * (pos["stop"] - pos["entry"]) > 0 else "CUT"
    elif (px >= pos["tgt"]) if s_ > 0 else (px <= pos["tgt"]): why = "TARGET"
    elif time.time() - pos["t0"] > pos["hold"] * 60 or dt.datetime.now(ET).time() >= dt.time(15, 55): why = "DONE"
    k = pos.get("k")
    if not why and k and k.get("close") and (pd.Timestamp(k["close"]) - pd.Timestamp.now(tz="UTC")).total_seconds() < 75:
        lv = kconv(mkt, px); c15 = k15(mkt)
        bid = (c15["yb"] if k["side"] == "YES" else c15["nb"]) if c15 and c15["ticker"] == k["ticker"] else 0
        sell_msg(mkt, pos, "⏱ window ending: " + ("HOLD to collect $1" if bid >= 0.5 else "SELL what's left"), px, lv,
                 f"\n{k['side']} {'winning' if bid >= 0.5 else 'losing'} at {bid * 100:.0f}¢")
        del st["fpos"][mkt]; return True
    if not why: return False
    lv, mins = kconv(mkt, px), (time.time() - pos["t0"]) / 60
    title = {"LOCK": "SELL signal 💰 move stalling, take profit", "TARGET": "SELL signal 💰 target reached",
             "CUT": "SELL signal 🛑 move failed", "DONE": "SELL signal ⏱ move is over"}[why]
    sell_msg(mkt, pos, title, px, lv, f"\n(signal lasted {mins:.0f} min)")
    del st["fpos"][mkt]; return True


def live_ctx(m):
    """Market/trend read on recent 1-min bars for the rationale."""
    trend, vwap, r, flow = ctx_features(m.Close, m.Volume, m.index, m.Open)
    c = m.Close; et = m.index.tz_convert(ET); y = c[et.date < et[-1].date()]
    day = (c.iloc[-1] / y.iloc[-1] - 1) * 100 if len(y) else 0
    return dict(trend=int(trend.iloc[-1]), vwap=float(vwap.iloc[-1]), rsi=float(r.iloc[-1]), day=day, flow=float(flow.fillna(0).iloc[-1]),
                sig=float(np.log(c).diff().tail(390).std()))


def why_lines(mkt, cx, bdir, px, lv, cell, kind):
    tr = "UP ↗️" if cx["trend"] > 0 else "DOWN ↘️"
    supports = cx["trend"] == bdir
    vw_toward = (px < cx["vwap"]) if bdir > 0 else (px > cx["vwap"])
    lines = [f"• Bigger trend (4h): {tr}, {'backs' if supports else 'works against'} a bounce {'up' if bdir > 0 else 'down'}",
             f"• Today's avg price (VWAP) {lv(cx['vwap'])}: a bounce moves {'TOWARD' if vw_toward else 'away from'} it",
             f"• Momentum RSI {cx['rsi']:.0f} ({'oversold' if cx['rsi'] < 30 else 'overbought' if cx['rsi'] > 70 else 'neutral'}) · today {cx['day']:+.1f}%",
             f"• Last 5 min: {'BUYERS' if cx['flow'] > 0.1 else 'SELLERS' if cx['flow'] < -0.1 else 'balanced'} in control "
             f"({'backs' if cx['flow'] * bdir > 0 else 'against'} the bounce)"]
    p = cell[1] if kind == "ls" else 1 - cell[1]
    lines.append(f"• Last 30 days, {cell[0]} setups like this: {'bounced back' if kind == 'ls' else 'kept going'} {p:.0%}")
    return "\n".join(lines)


# ---------------- unified 15-min calls: BUY → (TAKE PROFIT | WRONG → FLIP | HOLD) → RESULT ----------------
KIND = {"fast": "⚡ Fast move", "ls": "🎯 Longshot", "fav": "💪 Edge pick", "ihm": "📈 Close pattern", "flip": "🔄 Flip"}


def sess(close):
    close = pd.Timestamp(close).tz_convert(ET)
    return f"{(close - pd.Timedelta(minutes=15)):%-I:%M}–{close:%-I:%M}"


def call_txt(mkt, k):
    return f"price ends {'AT/ABOVE' if k['side'] == 'YES' else 'BELOW'} {money(mkt, k['k'])} at {pd.Timestamp(k['close']).tz_convert(ET):%-I:%M}"


def ctx_bullets(cx, up, lv):
    tr = "UP ↗️" if cx["trend"] > 0 else "DOWN ↘️"
    return "\n".join([
        f"• 4h trend {tr}: {'supports' if (cx['trend'] > 0) == up else 'against'} this call",
        f"• VWAP {lv(cx['vwap'])}: price is {'above' if cx['px'] > cx['vwap'] else 'below'} today's average",
        f"• Last 5 min: {'buyers' if cx['flow'] > 0.1 else 'sellers' if cx['flow'] < -0.1 else 'nobody'} in control "
        f"({'supports' if cx['flow'] * (1 if up else -1) > 0.1 else 'neutral' if abs(cx['flow']) <= 0.1 else 'against'})",
        f"• RSI {cx['rsi']:.0f} · today {cx['day']:+.1f}%"])


def open_call(st, mkt, kind, side, c, lv, px, odds, why, tested, parent=None):
    """Create a numbered call on the current 15-min contract and send the BUY message."""
    cost = c["ya"] if side == "YES" else c["na"]
    k = dict(ticker=c["ticker"], side=side, cost=cost, k=c["k"], close=str(c["close"]))
    tp = min(0.95, max(2.5 * cost, cost + 0.25)) if kind == "ls" else min(0.92, cost + max(0.15, (1 - cost) * 0.6))
    bail = max(0.03, cost * 0.5)
    pos = dict(side=1 if side == "YES" else -1, entry=px, stop=0, tgt=0, best=px, n=0, t0=time.time(), kind=kind, k=k,
               tp=tp, bail=bail, parent=parent)
    st.setdefault("lpos", {})[mkt] = pos; st.setdefault("lswin", {})[mkt] = c["ticker"]
    n = new_trade(st, mkt, pos, lv, px)
    left = (c["close"] - pd.Timestamp.now(tz="UTC")).total_seconds() / 60
    title = f"{badge(cost)} #{n} {NAME[mkt]} · {sess(c['close'])} · BUY {side} {cost * 100:.0f}¢"
    if 1 / cost >= BIG_X: title += f" · $5 → ${5 / cost:.0f}"
    notify(title,
           f"{KIND[kind]}" + (f" (flip of #{parent})" if parent else "") + f"\nCall: {call_txt(mkt, k)}\n"
           f"Now {lv(px)} · {left:.0f} min left\n{odds}\nWhy:\n{why}\n"
           f"Plan: take profit ≈{tp * 100:.0f}¢ · wrong if ≤{bail * 100:.0f}¢ · else hold to $1\n"
           + ("✅ tested edge" if tested else "🧪 unproven: small size"), "urgent", mkt)
    return n


def sell_msg(mkt, pos, title, px, lv, extra=""):
    """Legacy exits (slow/fast engines without a 15-min contract)."""
    if pos.get("k"): return follow_msg(mkt, pos, "🔔", title, extra)
    notify(f"#{pos.get('id', '?')} {NAME[mkt]} · {title}", f"Price now {lv(px)}" + extra, "urgent", mkt)


def follow_msg(mkt, pos, icon, action, extra=""):
    k = pos["k"]
    notify(f"{icon} #{pos.get('id', '?')} {NAME[mkt]} · {sess(k['close'])} · {action}",
           f"Call #{pos.get('id', '?')}: BUY {k['side']} at {k['cost'] * 100:.0f}¢ ({call_txt(mkt, k)})" + extra, "urgent", mkt)


def odds_line(p, cost, label="Odds"):
    e = p - cost - kfee(cost)
    return f"{label} ≈{p:.0%} vs {cost * 100:.0f}¢ + {kfee(cost) * 100:.0f}¢ fee → " + (
        f"edge +{e * 100:.0f}¢ ✅" if e >= 0.03 else "≈ fair" if e > -0.03 else f"pricey ({e * 100:.0f}¢) ⚠️")


def fast_entry(mkt, d1, fp, st, cool):
    """1-min momentum signal → BUY on the 15-min contract in that direction."""
    if busy(st, mkt): return False
    L, S = signals(d1, fp); bar = str(d1.index[-1])
    if not (L[-1] or S[-1]) or st.setdefault("flast", {}).get(mkt) == bar: return False
    st["flast"][mkt] = bar
    up, px = bool(L[-1]), d1.Close.iloc[-1]; lv = kconv(mkt, px); c = k15(mkt)
    if not c or st.get("lswin", {}).get(mkt) == c["ticker"]: return False
    left = (c["close"] - pd.Timestamp.now(tz="UTC")).total_seconds() / 60
    if left < 4: return False
    side = "YES" if up else "NO"; cost = c["ya"] if up else c["na"]
    if not 0 < cost < 0.9: return False
    cx = live_ctx(d1); cx["px"] = px
    fu = fair_up(px * lv.r, c["k"], left, cx["sig"]); p = (fu if up else 1 - fu) if fu is not None else 0.5
    t = fp.get("test") or {}
    why = f"• 1-min {fp['strategy']} signal: momentum just turned {'UP' if up else 'DOWN'}\n" + ctx_bullets(cx, up, lv)
    open_call(st, mkt, "fast", side, c, lv, px, odds_line(p, cost, "Odds now") +
              (f"\nPast: {t['win']:.0%} of these moves paid off" if t else ""), why, bool(t))
    cool[(mkt, "spike")] = time.time()
    return True


def k15_call(mkt, m, px, st, lv, cal, night=False):
    """🎯 longshot (cheap bounce side) or 💪 edge pick (favored side), from calibrated history + context."""
    from math import log, sqrt
    if busy(st, mkt) or not cal or not cal.get("stable" if night else "table") or len(m) < 300: return False
    c = k15(mkt)
    if not c: return False
    T = (c["close"] - pd.Timestamp.now(tz="UTC")).total_seconds() / 60
    if not 4 <= T <= 12 or st.setdefault("lswin", {}).get(mkt) == c["ticker"]: return False
    if event_window(mkt, dt.datetime.now(ET), T): return False
    cx = live_ctx(m); cx["px"] = px; z = log(px * lv.r / c["k"]) / (cx["sig"] * sqrt(T))
    if abs(z) < 0.5: return False
    bdir = -1 if z > 0 else 1; cl = m.Close
    turning = (px > cl.iloc[-1] and cx["rsi"] < 45) if bdir > 0 else (px < cl.iloc[-1] and cx["rsi"] > 55)
    sname = session(dt.datetime.now(ET))
    if night:
        cell = (cal.get("stable") or {}).get(f"{sname}|{ls_bucket(abs(z))}|{'T+' if cx['trend'] == bdir else 'T-'}|{'turn' if turning else 'run'}")
    else:
        cell = cal["table"].get(ctx_key(abs(z), bdir, cx["trend"], px, cx["vwap"], turning, cx["flow"]))
    if not cell: return False
    kind = "ls" if turning else "fav"
    up = (bdir > 0) if kind == "ls" else (bdir < 0); side = "YES" if up else "NO"
    cost = c["ya"] if up else c["na"]; p = cell[1] if kind == "ls" else 1 - cell[1]
    if kind == "ls" and not (0 < cost <= LS_MAX_COST and p - cost - kfee(cost) >= LS_MIN_EDGE): return False
    if kind == "fav" and not (0 < cost < 0.92 and p - cost - kfee(cost) >= FAV_MIN_EDGE): return False
    where = "below" if bdir > 0 else "above"
    why = (f"• Price is {where} the start and {'turning back toward it' if kind == 'ls' else 'still pushing away'}\n"
           + ctx_bullets(cx, up, lv) + (f"\n• 🌙 {SESS_TXT[sname]}" if night else "")
           + f"\n• Last 30 days{' in this session' if night else ''}: {cell[0]} setups like this → "
           f"{'bounced back' if kind == 'ls' else 'kept going'} {p:.0%}")
    open_call(st, mkt, kind, side, c, lv, px, odds_line(p, cost), why,
              cal.get(f"night_{kind}_ok" if night else f"{kind}_ok"))
    return True


def ihm_call(mkt, m, px, st, lv, cal):
    """3:30 PM ET close pattern (Wen et al.; direction re-learned): fires once a day if validated."""
    ih = (cal or {}).get("ihm") or {}; now = dt.datetime.now(ET)
    if not ih.get("ok") or not (dt.time(15, 30, 20) <= now.time() <= dt.time(15, 33)) or busy(st, mkt): return False
    if st.setdefault("ihm_day", {}).get(mkt) == str(now.date()): return False
    et = m.index.tz_convert(ET); today = m[et.date == now.date()]; prev = m[et.date < now.date()]
    if not len(prev) or not len(today): return False
    tod = today.index.tz_convert(ET); at = lambda h, mi: today.Close[(tod.hour * 60 + tod.minute) < h * 60 + mi]
    wed = now.weekday() == 2 and mkt != "NATGAS"
    a, b = (at(10, 30), at(11, 0)) if wed else (prev.Close, at(10, 0))
    if not len(a) or not len(b): return False
    sig = b.iloc[-1] / a.iloc[-1] - 1; c = k15(mkt)
    if not c or abs(sig) < 0.001: return False
    up = (sig > 0) == (ih.get("dir", "follow") == "follow"); side = "YES" if up else "NO"; cost = c["ya"] if up else c["na"]
    if not (0 < cost < 0.9 and ih["hit"] - cost - kfee(cost) >= 0.02): return False
    st["ihm_day"][mkt] = str(now.date()); cx = live_ctx(m); cx["px"] = px
    why = (f"• {'10:30–11:00 (EIA day)' if wed else 'Overnight + first half-hour'} moved {sig * 100:+.2f}%\n"
           f"• Last half-hour has {'FOLLOWED' if ih.get('dir') == 'follow' else 'REVERSED'} that {ih['hit']:.0%} of {ih['n']} days "
           f"(recent {ih['hit_recent']:.0%})\n" + ctx_bullets(cx, up, lv))
    open_call(st, mkt, "ihm", side, c, lv, px, odds_line(ih["hit"], cost), why, True)
    st["ihm_day"][mkt] = str(now.date())
    return True


def manage_ls(mkt, px, st, lv):
    """Every tick, using the Kalshi contract's own price: TAKE PROFIT / WRONG (+ FLIP) / HOLD / RESULT."""
    pos = st.get("lpos", {}).get(mkt)
    if not pos: return False
    k = pos["k"]; c = k15(mkt); left = (pd.Timestamp(k["close"]) - pd.Timestamp.now(tz="UTC")).total_seconds() / 60
    if not c or c["ticker"] != k["ticker"]:  # window over → final result
        txt, won = contract_status(k)
        follow_msg(mkt, pos, "🏁" if won else "❌", f"RESULT: {'RIGHT ✅' if won else 'WRONG'}", txt)
        del st["lpos"][mkt]; return True
    if pos.get("held"): return False
    bid = c["yb"] if k["side"] == "YES" else c["nb"]; gain = (bid - k["cost"]) * 100
    if bid >= pos.get("tp", 0.9):
        follow_msg(mkt, pos, "✅", f"TAKE PROFIT: sell {k['side']} at {bid * 100:.0f}¢ ({gain:+.0f}¢)",
                   f"\nContract jumped {k['cost'] * 100:.0f}¢ → {bid * 100:.0f}¢ ({bid / k['cost']:.1f}×)")
        del st["lpos"][mkt]; return True
    if bid <= pos.get("bail", 0) and left >= 4 and pos.get("kind") != "flip":
        follow_msg(mkt, pos, "❌", f"WRONG: sell {k['side']} at {bid * 100:.0f}¢ ({gain:+.0f}¢)",
                   "\nPrice moved the other way. The opposite side is now favored.")
        del st["lpos"][mkt]
        opp = "NO" if k["side"] == "YES" else "YES"; oa = c["na"] if opp == "NO" else c["ya"]
        if 0 < oa <= 0.85:  # momentum tends to continue within the window → flip
            p = min(0.97, 1 - bid)
            open_call(st, mkt, "flip", opp, c, lv, px, odds_line(p, oa, "Market odds"),
                      f"• #{pos.get('id')} was wrong: price is going the other way\n• Within 15-min windows, moves tend to keep going",
                      False, parent=pos.get("id"))
        return True
    if left < 1.25:
        if bid >= 0.5:
            follow_msg(mkt, pos, "⏱", f"HOLD {k['side']} to settle (worth {bid * 100:.0f}¢ → $1)", "\nResult follows at the close.")
            pos["held"] = True; return True
        follow_msg(mkt, pos, "⏱", f"Losing: sell {k['side']} at {bid * 100:.0f}¢ or let it expire")
        del st["lpos"][mkt]; return True
    return False


def skip_reasons(mkt, m, px, lv):
    """Why this 15-min window is not worth betting. Returns (reasons, hard)."""
    from math import log, sqrt
    c = k15(mkt)
    if not c or len(m) < 300: return [], False
    T = (c["close"] - pd.Timestamp.now(tz="UTC")).total_seconds() / 60
    cx = live_ctx(m); r1 = np.log(m.Close).diff()
    quiet = r1.tail(30).std() / (r1.tail(390).std() + 1e-12)
    z = log(px * lv.r / c["k"]) / (cx["sig"] * sqrt(max(T, 1)))
    fav = max(c["ya"], c["na"]); reasons, hard = [], False
    if fav >= 0.90:
        reasons.append(f"Already decided: favorite costs {fav * 100:.0f}¢ → at most {100 - fav * 100:.0f}¢ gain before fees"); hard = True
    if ev := event_window(mkt, dt.datetime.now(ET), T):
        reasons.append(ev); hard = True
    soft = []
    if quiet < 0.7: soft.append(f"Very quiet: last 30 min moving {int((1 - quiet) * 100)}% less than usual")
    if abs(px - m.Close.ewm(span=240, adjust=False).mean().iloc[-1]) / px < 0.001: soft.append("Trend not in favor: flat vs 4h average, no direction")
    if abs(m.Close.iloc[-1] / m.Close.iloc[-16] - 1) < 0.0005: soft.append("Last 15 min went nowhere (<0.05%)")
    if abs(cx["flow"]) < 0.15: soft.append("Buyers and sellers balanced: no push either way")
    if abs(z) < 0.3 and 0.45 <= c["ya"] <= 0.55: soft.append(f"Coin flip at ~50¢ and the {kfee(0.5) * 100:.0f}¢ fee makes it a losing bet")
    if len(soft) >= 2: reasons += soft
    return reasons, hard


def skip_board(data, st, params):
    """Session preview at minute 1 and update at minute 7: which markets to SKIP (and why) vs in play."""
    now = dt.datetime.now(ET)
    if now.minute % 15 not in (1, 7) or now.time() >= dt.time(15, 55): return
    slot = now.strftime("%Y-%m-%d %H:%M")
    if st.get("skipslot") == slot: return
    st["skipslot"] = slot; w_end = now.replace(second=0, microsecond=0) + dt.timedelta(minutes=15 - now.minute % 15)
    label = f"{(w_end - dt.timedelta(minutes=15)):%-I:%M}–{w_end:%-I:%M}"
    done = set(st.get("skipped", {}).get(label, [])); skips, play = [], []
    for mkt, (_, etf) in MARKETS.items():
        if etf not in data: continue
        if busy(st, mkt): play.append((mkt, "call open")); continue
        m = data[etf]; px = m.Close.iloc[-1]; lv = kconv(mkt, px)
        why, hard = skip_reasons(mkt, m, px, lv)
        if why and mkt not in done: skips.append((mkt, why))
        elif not why: play.append((mkt, "watching for a setup"))
    if not skips: return
    st.setdefault("skipped", {})[label] = sorted(done | {k for k, _ in skips})
    body = "\n".join(f"{COLOR[k][0]} {NAME[k]}: SKIP\n" + "\n".join(f"   • {w}" for w in why) for k, why in skips)
    if play: body += "\n\n✅ In play: " + ", ".join(f"{COLOR[k][0]} {NAME[k]} ({t})" for k, t in play)
    notify(f"⛔ SKIP · {label} session" + (" (update)" if now.minute % 15 == 7 else ""), body, "default")


def night_bars(mkt):
    """~10-min-delayed 1-min futures bars (context) from Yahoo."""
    import yfinance as yf
    df = yf.Ticker(MARKETS[mkt][0]).history(period="2d", interval="1m", auto_adjust=False)
    return df[["Open", "High", "Low", "Close", "Volume"]].dropna()


def night_price(mkt, y):
    """Real-time price from Kalshi: strike-book implied price, else backed out of the 15-min YES price."""
    from math import exp, sqrt
    from statistics import NormalDist
    b = kalshi_book(mkt)
    if b: return b["px"]
    c = k15(mkt)
    if not c or len(y) < 60: return None
    mid = (c["ya"] + c["yb"]) / 2; T = (c["close"] - pd.Timestamp.now(tz="UTC")).total_seconds() / 60
    if not 0.05 < mid < 0.95 or T <= 0: return None
    sig = float(np.log(y.Close).diff().tail(390).std())
    return c["k"] * exp(NormalDist().inv_cdf(mid) * sig * sqrt(T))


def ident(mkt):
    f = lambda x: money(mkt, x); f.r = 1.0; return f


def market_mode(now):
    """'day' = US stock hours (fund prices, Alpaca); 'night' = futures open otherwise; 'closed' = weekend / 5-6pm break."""
    wd, t = now.weekday(), now.time()
    if wd == 5 or (wd == 4 and t >= dt.time(17)) or (wd == 6 and t < dt.time(18)) or dt.time(17) <= t < dt.time(18): return "closed"
    return "day" if wd < 5 and LIVE_OPEN <= t <= LIVE_CLOSE else "night"


def night_tick(st, params, cool, nh, yc):
    """Overnight: Kalshi real-time price + delayed futures context → longshots / edge picks / skip board / watch board."""
    now = dt.datetime.now(ET); minute = now.replace(second=0, microsecond=0); changed = False; boards = {}
    for mkt in MARKETS:
        if yc.get(mkt, (None,))[0] != minute:
            try: yc[mkt] = (minute, night_bars(mkt))
            except Exception as e: print("night bars", mkt, e); continue
        y = yc[mkt][1]; kp = night_price(mkt, y)
        if kp is None or len(y) < 300: continue
        h = nh.setdefault(mkt, []); h.append((pd.Timestamp.now(tz="UTC"), kp)); del h[:-240]
        hb = pd.Series([p for _, p in h], index=[t for t, _ in h]).resample("1min").ohlc().dropna()
        hb = hb.rename(columns=str.title).assign(Volume=0.0)
        m = pd.concat([y[y.index < hb.index[0]], hb]); m = m[~m.index.duplicated(keep="last")]
        _SIG[mkt] = float(np.log(y.Close).diff().tail(390).std()); lv = ident(mkt)
        changed |= manage_ls(mkt, kp, st, lv)
        if now.time() < dt.time(15, 50) or now.time() > dt.time(16, 10):
            changed |= k15_call(mkt, m.iloc[:-1], kp, st, lv, (params.get("_cal") or {}).get(mkt), night=True)
        boards[mkt] = (m, kp, lv)
    return changed, boards


def night_boards(st, boards):
    """Skip board (minute 1/7 of each session) + 10-min watch board for overnight."""
    now = dt.datetime.now(ET)
    if now.minute % 15 in (1, 7):
        slot = now.strftime("%Y-%m-%d %H:%M")
        if st.get("skipslot") != slot:
            st["skipslot"] = slot; w_end = now.replace(second=0, microsecond=0) + dt.timedelta(minutes=15 - now.minute % 15)
            label = f"{(w_end - dt.timedelta(minutes=15)):%-I:%M}–{w_end:%-I:%M}"; done = set(st.get("skipped", {}).get(label, []))
            skips, play = [], []
            for mkt, (m, kp, lv) in boards.items():
                if busy(st, mkt): play.append((mkt, "call open")); continue
                why, _ = skip_reasons(mkt, m, kp, lv)
                if why and mkt not in done: skips.append((mkt, why))
                elif not why: play.append((mkt, "watching"))
            if skips:
                st.setdefault("skipped", {})[label] = sorted(done | {k for k, _ in skips})
                body = "\n".join(f"{COLOR[k][0]} {NAME[k]}: SKIP\n" + "\n".join(f"   • {w}" for w in why) for k, why in skips)
                if play: body += "\n\n✅ In play: " + ", ".join(f"{COLOR[k][0]} {NAME[k]} ({t})" for k, t in play)
                notify(f"⛔ SKIP · 🌙 {label} session · {session(now)}", body, "default")
    if now.minute % 10 == 0 and st.get("nightpulse") != now.strftime("%H:%M"):
        st["nightpulse"] = now.strftime("%H:%M"); lines = []
        for mkt, (m, kp, lv) in boards.items():
            c = k15(mkt); line = f"{COLOR[mkt][0]} {NAME[mkt]}  {money(mkt, kp)}"
            if c: line += f"\n    15-min ({c['close'].tz_convert(ET):%-I:%M}): start {money(mkt, c['k'])} · YES {c['ya'] * 100:.0f}¢ / NO {c['na'] * 100:.0f}¢"
            op = next((st[k][mkt] for k in ("lpos",) if mkt in st.get(k, {})), None)
            lines.append(line + (f"\n    open: call #{op.get('id', '?')}" if op else "\n    watching"))
        if lines: notify(f"🌙 Watching · {now:%-I:%M %p} · {SESS_TXT[session(now)]}", "\n".join(lines), "default")


def snapshots():
    """Latest trade price per ETF (real-time, one request)."""
    hdr = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET"]}
    r = requests.get("https://data.alpaca.markets/v2/stocks/snapshots", headers=hdr, timeout=10,
                     params={"symbols": ",".join(v[1] for v in MARKETS.values()), "feed": os.getenv("ALPACA_FEED", "iex")})
    r.raise_for_status()
    return {k: (v.get("latestTrade") or {}).get("p") for k, v in r.json().items()}


def live():
    """Watch prices every TICK_SEC (15s): instant alerts on events; strategy on each closed bar; check-in on the clock."""
    if not ALPACA: sys.exit("live mode needs ALPACA_KEY / ALPACA_SECRET")
    t0, maxmin = time.time(), float(os.getenv("LIVE_MAX_MIN") or 1e9); nt = 0
    pulse_min, tick = int(os.getenv("PULSE_MIN") or 10), int(os.getenv("TICK_SEC") or 15)
    cool, data, params, nh, yc = {}, {}, load_params(), {}, {}
    if not MAIN_ON:  # drop any old slow-signal positions so they don't block 15-min calls
        st0 = load_state(); st0["pos"] = {}; json.dump(st0, open(STATE_FILE, "w"), indent=1, default=float)
    last_min = last_hour = last_pulse = None
    print(f"live mode: tick {tick}s, check-in every {pulse_min} min on the clock")
    while (time.time() - t0) / 60 < maxmin:
        now = dt.datetime.now(ET)
        mode = market_mode(now)
        if mode == "closed": time.sleep(60); continue
        if mode == "night":
            try:
                st = load_state(); ch, boards = night_tick(st, params, cool, nh, yc); night_boards(st, boards)
                json.dump(st, open(STATE_FILE, "w"), indent=1, default=float)
                if ch: persist("bot: night call")
                if now.minute < 2 and now.hour != last_hour:
                    last_hour = now.hour
                    if os.getenv("GIT_PERSIST"): os.system("git pull -q --rebase origin main"); params = load_params()
            except Exception as e:
                print("night error:", e)
            time.sleep(max(1, tick - time.time() % tick)); continue
        try:
            st = load_state(); st.setdefault("sent", []); changed = False
            minute = now.replace(second=0, microsecond=0)
            if minute != last_min and now.second >= 3:  # new minute: pull closed 1-min bars, run strategies
                last_min = minute
                since = min((d.index[-1] for d in data.values()), default=None)
                since = (since - pd.Timedelta(minutes=3)) if since is not None else pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=7)
                for sym, df in fetch_1m(since).items():
                    data[sym] = pd.concat([data.get(sym), df]).pipe(lambda x: x[~x.index.duplicated(keep="last")]).tail(6000)
                for mkt_, (_, etf_) in MARKETS.items():
                    if etf_ in data: _SIG[mkt_] = float(np.log(data[etf_].Close).diff().tail(390).std())
                for e in events(hours=0.25):
                    if (k := f"EV15|{e}|{now.date()}") not in st["sent"]:
                        st["sent"].append(k); notify("⏰ REPORT IN 15 MIN", e + "\nPrices can jump hard. Avoid new bets until after.", "urgent")
                sent = set(st["sent"])
                for mkt, (_, etf) in MARKETS.items():
                    p = {**DEFAULT, **params.get(mkt, {})}; n = BARS[p["interval"]][1]
                    if n <= 15 and etf in data:
                        m = data[etf]; b = resample(m[m.index + pd.Timedelta(minutes=1) <= pd.Timestamp.now(tz="UTC")], n)
                        if len(b) > 60 and str(b.index[-1]) != st.get("last", {}).get(mkt):
                            had = mkt in st.get("pos", {}); process(mkt, indicators(b), p, st, sent)
                            changed |= had != (mkt in st.get("pos", {}))
                st["sent"] = sorted(sent)[-300:]
                for mkt, (_, etf) in MARKETS.items():  # fast engine: spike-start detector on closed 1-min bars
                    if etf not in data or mkt in st.get("fpos", {}): continue
                    m1 = data[etf]; m1 = m1[m1.index + pd.Timedelta(minutes=1) <= pd.Timestamp.now(tz="UTC")]
                    if len(m1) >= 400 and now.time() < dt.time(15, 50):
                        fp = {**FAST_DEFAULT, **(params.get("_fast") or {}).get(mkt, {})}
                        changed |= fast_entry(mkt, indicators(m1.tail(1500)), fp, st, cool)
            px = snapshots(); nt += 1  # every tick: live price → spike/dip, trend, stop/target checks
            for mkt, (_, etf) in MARKETS.items():
                if etf not in data or not px.get(etf): continue
                m = data[etf]; m = m[m.index + pd.Timedelta(minutes=1) <= pd.Timestamp.now(tz="UTC")]
                cur = pd.Timestamp.now(tz="UTC").floor("min"); p_ = float(px[etf])
                changed |= manage_fast(mkt, p_, st)
                lv_ = kconv(mkt, p_); changed |= manage_ls(mkt, p_, st, lv_)
                if dt.datetime.now(ET).time() >= dt.time(15, 50): continue  # no new calls into the close
                cal_ = (params.get("_cal") or {}).get(mkt)
                changed |= ihm_call(mkt, m, p_, st, lv_, cal_) or k15_call(mkt, m, p_, st, lv_, cal_)
                row = pd.DataFrame({"Open": p_, "High": p_, "Low": p_, "Close": p_, "Volume": m.Volume.iloc[-1]}, index=[cur])
                changed |= bool(fast_checks(mkt, pd.concat([m, row]), st, cool))
            skip_board(data, st, params)
            json.dump(st, open(STATE_FILE, "w"), indent=1, default=float)
            if changed: persist("bot: live trade")
            if now.minute < 3 and now.hour != last_hour:  # hourly: refresh params + 1h strategies
                last_hour = now.hour
                if os.getenv("GIT_PERSIST"): os.system("git pull -q --rebase origin main"); params = load_params()
                hourly = [k for k in MARKETS if BARS[{**DEFAULT, **params.get(k, {})}["interval"]][1] > 15]
                if hourly: scan(hourly); persist()
            slot = minute.replace(minute=minute.minute - minute.minute % pulse_min) if pulse_min else None
            if pulse_min and slot != last_pulse and data:
                if last_pulse is not None or now.minute % pulse_min == 0: pulse(data, load_state())
                last_pulse = slot
        except Exception as e:
            print("live error:", e)
        time.sleep(max(1, tick - time.time() % tick))
    print(f"live ended after {nt} price checks"); persist()


def kalshi_discover():
    ser = requests.get(f"{KALSHI}/series", timeout=30).json().get("series", [])
    for x in ser:
        t = (x.get("title") or "").lower()
        if re.search(r"(natural gas|natgas|brent|wti|crude|oil)", t) and x.get("frequency") not in ("annual", "monthly", "quarterly", "custom", "one_off", "weekly", "daily"):
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


def calibrate_only():
    p = load_params(); p["_cal"] = {m: calibrate(m) for m in MARKETS}; json.dump(p, open(PARAMS_FILE, "w"), indent=1)


def audit():
    """Numbers + trend + recent-performance check."""
    import yfinance as yf
    params = load_params()
    for mkt, (fut, etf) in MARKETS.items():
        print(f"\n===== {mkt} =====")
        b = kalshi_book(mkt); c15 = k15(mkt)
        try:
            yfp = float(yf.Ticker(fut).history(period="1d", interval="1m").Close.iloc[-1])
        except Exception: yfp = None
        e1 = fetch_alpaca(etf, "1m", 3) if ALPACA else None
        print("PRICES  Kalshi-implied:", b and round(b["px"], 3), "| Yahoo futures (~10m delayed):", yfp and round(yfp, 3),
              "| gap:", f"{(b['px'] / yfp - 1) * 100:+.2f}%" if b and yfp else "n/a",
              "| 15m start:", c15 and c15["k"], "| ETF:", None if e1 is None else round(float(e1.Close.iloc[-1]), 2))
        d = indicators(fetch(mkt, "1h", 60)); r = d.iloc[-1]
        print(f"TREND   1h close {r.Close:.2f} | vs EMA50 {'above' if r.Close > r.ema else 'below'} | vs EMA200 "
              f"{'above' if r.Close > r.ema200 else 'below'} | 5d {(r.Close / d.Close.iloc[-36] - 1) * 100:+.1f}% | "
              f"vol pct {r.volp:.0%} | RSI {r.rsi:.0f}")
        for tag, p in (("MAIN", {**DEFAULT, **params.get(mkt, {})}), ("FAST", {**FAST_DEFAULT, **(params.get("_fast") or {}).get(mkt, {})})):
            days = 14 if p["interval"] in ("1m", "5m") else 30
            dd = indicators(fetch(mkt, p["interval"], days)); L, S = signals(dd, p)
            print(f"{tag:5} {p['strategy']}/{p['interval']} last {days}d: {stats(simulate(dd, p, L, S))} | validated: {p.get('test')} chunks {p.get('chunks_ok')}")


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
                live=live, livetest=lambda: (os.environ.update(LIVE_MAX_MIN='2', GIT_PERSIST='', STATE_FILE='/tmp/st.json'), live()), audit=audit, calibrate=calibrate_only, kalshi=kalshi_discover, kcheck=kcheck, loop=lambda: [(scan(), time.sleep(int(os.getenv("LOOP_SEC", 120)))) for _ in iter(int, 1)])
    cmds.get((sys.argv[1:] or ["scan"])[0], lambda: print(__doc__))()
