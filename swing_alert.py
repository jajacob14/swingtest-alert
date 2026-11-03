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

MARKETS = {"BRENT": ("BZ=F", "BNO"), "WTI": ("CL=F", "USO"), "NATGAS": ("NG=F", "UNG")}          # energy: day + night engines
METALS = {"GOLD": ("GC=F", "GLD"), "SILVER": ("SI=F", "SLV"), "COPPER": ("HG=F", "CPER"),         # Kalshi 15-min metals:
          "PLATINUM": ("PL=F", "PPLT"), "PALLADIUM": ("PA=F", "PALL")}                             # Kalshi-price engine 24/5
CRYPTO = {"BTC": ("BTC-USD", None), "ETH": ("ETH-USD", None), "SOL": ("SOL-USD", None), "XRP": ("XRP-USD", None),
          "DOGE": ("DOGE-USD", None), "BNB": ("BNB-USD", None), "HYPE": ("HYPE32196-USD", None), "NEAR": ("NEAR-USD", None),
          "ZEC": ("ZEC-USD", None)}
FX = {"EURUSD": ("EURUSD=X", None), "GBPUSD": ("GBPUSD=X", None), "USDJPY": ("JPY=X", None)}
EXTRA_ON = os.getenv("EXTRA_MARKETS", "0") == "1"  # crypto + FX: OFF (commodities only); set EXTRA_MARKETS=1 to enable
ALL = {**MARKETS, **METALS, **(CRYPTO if EXTRA_ON else {}), **(FX if EXTRA_ON else {})}
COINBASE = {"BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD", "XRP": "XRP-USD", "DOGE": "DOGE-USD", "NEAR": "NEAR-USD", "ZEC": "ZEC-USD"}
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
COLOR = {"BTC": ("🪙", "", 0xF7931A), "ETH": ("💎", "", 0x627EEA), "SOL": ("☀️", "", 0x14F195), "XRP": ("💧", "", 0x23292F),
         "DOGE": ("🐕", "", 0xC2A633), "BNB": ("🔶", "", 0xF3BA2F), "HYPE": ("🌊", "", 0x50D2C1), "NEAR": ("🌐", "", 0x00C08B),
         "ZEC": ("🛡️", "", 0xECB244), "EURUSD": ("💶", "", 0x1565C0), "GBPUSD": ("💷", "", 0x6A1B9A), "USDJPY": ("💴", "", 0xC62828),
         "GOLD": ("🟡", "", 0xFBC02D), "SILVER": ("⚪", "", 0x9E9E9E), "COPPER": ("🟤", "", 0x8D6E63),
         "PLATINUM": ("🟣", "", 0x7E57C2), "PALLADIUM": ("🔴", "", 0xE53935),
         "BRENT": ("🟢", "green_circle", 0x43A047), "WTI": ("🟠", "orange_circle", 0xFB8C00),
         "NATGAS": ("🔵", "large_blue_circle", 0x1E88E5)}


# ---------------- data ----------------
def fetch(mkt, interval, days):
    fut, etf = ALL[mkt]
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
    out, end = [], dt.datetime.now(dt.timezone.utc)
    for k in range(0, days, 7):
        e = end - dt.timedelta(days=k); b = e - dt.timedelta(days=min(7, days - k))
        df = yf_hist(ALL[mkt][0], start=b, end=e, interval="1m")
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


SH_SESS = {'US': 'US day', 'EVE': 'evening', 'ASIA': 'Asia', 'EU': 'Europe'}
SESS_TXT = {"US": "US day session", "EVE": "Evening session (after settlement, 6pm reopen)",
            "ASIA": "Asian session (thin trading)", "EU": "European session (London digests overnight news)"}


def event_window(mkt, now_et, mins_ahead=15):
    """Known jumpy windows (research-based). Returns a reason string or ''."""
    end = now_et + dt.timedelta(minutes=mins_ahead); m0, wd = now_et.hour * 60 + now_et.minute, now_et.weekday()
    def hit(a, b): return a <= m0 <= b or a <= end.hour * 60 + end.minute <= b
    if events(now_et, hours=mins_ahead / 60 + 0.05): return "EIA report inside this session"
    if mkt != "NATGAS" and wd == 1 and hit(16 * 60 + 15, 17 * 60): return "API oil inventory report (Tue 4:30 PM): after-hours jumps"
    if (mkt in MARKETS or mkt in METALS) and hit(18 * 60, 18 * 60 + 30): return "6 PM reopen: thin, gappy trading"
    if mkt == "NATGAS" and (hit(23 * 60 + 15, 23 * 60 + 59) or hit(90, 150) or hit(5 * 60 + 15, 5 * 60 + 59)):
        return "Weather-model update (GFS/European): nat gas jumps on forecast changes"
    if mkt in FX:
        if wd < 5 and hit(8 * 60 + 25, 8 * 60 + 45): return "8:30 AM US data: currencies jump on rate news"
        if wd < 5 and hit(10 * 60 + 55, 11 * 60 + 5): return "London 4pm FX fix: big orders cluster"
        if mkt == "USDJPY" and hit(19 * 60 + 50, 20 * 60): return "Tokyo fix: big yen orders cluster"
    if mkt in CRYPTO and wd < 5 and hit(8 * 60 + 25, 8 * 60 + 40): return "8:30 AM US data: crypto swings on rate news"
    if mkt in METALS:
        if wd < 5 and hit(8 * 60 + 25, 8 * 60 + 45): return "8:30 AM US data (jobs/CPI/claims): metals jump on rate news"
        if hit(20 * 60, 20 * 60 + 15): return "Shanghai open: Chinese buying/selling hits metals"
        if hit(3 * 60, 3 * 60 + 15): return "London open: volatility spike as Europe trades overnight news"
        if mkt in ("GOLD", "PLATINUM", "PALLADIUM") and (hit(5 * 60 + 25, 5 * 60 + 40) or hit(9 * 60 + 55, 10 * 60 + 10)):
            return "London price fix: big orders cluster here"
        if mkt == "SILVER" and hit(6 * 60 + 55, 7 * 60 + 10): return "London silver fix: big orders cluster here"
        if hit(13 * 60 + 25, 13 * 60 + 40): return "COMEX settlement (1:30 PM): end-of-day positioning"
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


def drift_stats(df):
    """Per session: share of 15-min windows that ended UP. Edge only if older 70% and newer 30% agree (≥3.5 pts)."""
    df = df.resample("1min").last().dropna(how="all"); c = df.Close; w = df.index.floor("15min")
    g = pd.DataFrame({"start": c.shift(1).groupby(w).first(), "end": c.groupby(w).last(), "n": c.groupby(w).size()})
    g = g[g.n >= 8].dropna(); g["up"] = g.end >= g.start
    g["sess"] = [session(t.tz_convert(ET)) for t in g.index]; cut = int(len(g) * 0.7); out = {}
    for sname, x in g.groupby("sess"):
        tr, te = x[x.index < g.index[cut]], x[x.index >= g.index[cut]]
        if len(tr) < 100 or len(te) < 60: continue
        ptr, pte = tr.up.mean(), te.up.mean()
        ok = bool((ptr - 0.5) * (pte - 0.5) > 0 and min(abs(ptr - 0.5), abs(pte - 0.5)) >= 0.035)
        p = min(ptr, pte) if ptr > 0.5 else max(ptr, pte)  # conservative
        out[sname] = dict(dir="UP" if p > 0.5 else "DOWN", p=round(float(p if p > 0.5 else 1 - p), 3),
                          older=round(float(ptr), 3), newer=round(float(pte), 3), n=len(x), ok=ok)
    return out


SPARK = "▁▂▃▄▅▆▇█"


def spark(vals):
    v = np.asarray(vals, float); lo, hi = np.nanmin(v), np.nanmax(v)
    return "".join(SPARK[int((x - lo) / (hi - lo + 1e-12) * 7)] for x in v)


def spike_parts(c, h, l, v, o):
    """Vectorized spike score 0-100 + direction from 1-min bars: acceleration, breakout, wake-up, flow."""
    r = np.log(c).diff(); sig = r.rolling(390, min_periods=60).std()
    z3 = np.log(c / c.shift(3)) / (sig * np.sqrt(3))
    brk = ((c > h.rolling(30).max().shift(3)) | (c < l.rolling(30).min().shift(3))).astype(float)
    wake = (r.rolling(5).std() / (r.rolling(30).std().shift(5) + 1e-12) > 1.8).astype(float)
    vv = v.where(v > 0, 1.0); flow = (np.sign(c - o) * vv).rolling(5).sum() / vv.rolling(5).sum()
    score = 100 * (0.35 * (z3.abs() / 3).clip(upper=1) + 0.25 * brk + 0.2 * flow.abs().clip(upper=1).fillna(0) + 0.2 * wake)
    return score, np.sign(z3), z3, sig


FEATS = ("m3", "m15", "m60", "trend", "flow", "vwap", "rsi", "brk")
FC_H = 10  # forecast horizon (minutes)


def feat_frame(df):
    """Per-minute features for the 10-minute direction model (all use only past data)."""
    c, h, l, o = df.Close, df.High, df.Low, df.Open; v = df.Volume.fillna(0)
    r = np.log(c).diff(); sig = r.rolling(390, min_periods=60).std()
    trend, vwap, rs, flow = ctx_features(c, v, df.index, o)
    f = pd.DataFrame({
        "m3": np.log(c / c.shift(3)) / (sig * np.sqrt(3)), "m15": np.log(c / c.shift(15)) / (sig * np.sqrt(15)),
        "m60": np.log(c / c.shift(60)) / (sig * np.sqrt(60)), "trend": trend, "flow": flow,
        "vwap": (np.log(c / vwap) / (sig * np.sqrt(60))).clip(-4, 4), "rsi": (rs - 50) / 50,
        "brk": np.where(c > h.rolling(30).max().shift(1), 1.0, np.where(c < l.rolling(30).min().shift(1), -1.0, 0.0))},
        index=df.index).clip(-5, 5)
    return f, sig


def forecast_stats(df):
    """Logistic model: P(price higher in 10 min). Trained on older 70%, judged on newest 30%."""
    df = df.resample("1min").last().dropna(how="all")
    f, sig = feat_frame(df); y = (df.Close.shift(-FC_H) > df.Close).astype(float)
    mv = (np.log(df.Close.shift(-FC_H) / df.Close).abs() / (sig * np.sqrt(FC_H)))
    d = pd.concat([f, y.rename("y"), mv.rename("mv")], axis=1).dropna()
    if len(d) < 3000: return {"ok": False, "n": len(d)}
    cut = int(len(d) * 0.7); tr, te = d.iloc[:cut], d.iloc[cut:]
    mu, sd = tr[list(FEATS)].mean(), tr[list(FEATS)].std() + 1e-9
    X = ((tr[list(FEATS)] - mu) / sd).to_numpy(); Y = tr.y.to_numpy(); w = np.zeros(X.shape[1] + 1)
    Xb = np.c_[np.ones(len(X)), X]
    for _ in range(400):  # gradient descent, light L2
        p = 1 / (1 + np.exp(-Xb @ w)); w -= 0.5 * (Xb.T @ (p - Y) / len(Y) + 0.001 * np.r_[0, w[1:]])
    Xt = np.c_[np.ones(len(te)), ((te[list(FEATS)] - mu) / sd).to_numpy()]; pt = 1 / (1 + np.exp(-Xt @ w))
    conf = (pt >= 0.6) | (pt <= 0.4); hit = ((pt >= 0.5) == (te.y.to_numpy() == 1))
    res = dict(w=[round(float(x), 5) for x in w], mu=[round(float(x), 6) for x in mu], sd=[round(float(x), 6) for x in sd],
               acc=round(float(hit.mean()), 3), acc_conf=round(float(hit[conf].mean()), 3) if conf.any() else 0,
               n_conf=int(conf.sum()), share_conf=round(float(conf.mean()), 3), move=round(float(d.mv.median()), 3))
    res["ok"] = bool(res["acc_conf"] >= 0.55 and res["n_conf"] >= 300)
    return res


WFEATS = FEATS + ("dz", "tleft")


def _fit_logit(X, Y, iters=500):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Xb @ w)); w -= 0.5 * (Xb.T @ (p - Y) / len(Y) + 0.001 * np.r_[0, w[1:]])
    return w


def window_stats(df):
    """Our own window-outcome model: P(15-min window ends UP) with 3-12 min left, from trend/momentum/flow/VWAP/RSI/
    breakout + distance to start. Tested on newest 30%: accuracy of 90%+ calls ('near locks') vs what price alone implied."""
    df = df.resample("1min").last().dropna(how="all"); c = df.Close; w = df.index.floor("15min")
    f, sig = feat_frame(df)
    full = pd.Series(1, index=df.index).groupby(w).transform("size") >= 8
    start = c.shift(1).groupby(w).transform("first"); end = c.groupby(w).transform("last")
    T = 14 - (df.index.tz_convert(ET).minute % 15)
    f["dz"] = (np.log(c / start) / (sig * np.sqrt(np.maximum(T, 1)))).clip(-6, 6); f["tleft"] = T / 12
    y = (end >= start).astype(float)
    d = pd.concat([f, y.rename("y")], axis=1)[full & (T >= 3) & (T <= 12)].dropna()
    if len(d) < 3000: return {"ok": False, "n": len(d)}
    cut = int(len(d) * 0.7); tr, te = d.iloc[:cut], d.iloc[cut:]
    mu, sd = tr[list(WFEATS)].mean(), tr[list(WFEATS)].std() + 1e-9
    wts = _fit_logit(((tr[list(WFEATS)] - mu) / sd).to_numpy(), tr.y.to_numpy())
    pt = 1 / (1 + np.exp(-(np.c_[np.ones(len(te)), ((te[list(WFEATS)] - mu) / sd).to_numpy()] @ wts)))
    conf = np.maximum(pt, 1 - pt); right = ((pt >= 0.5) == (te.y.to_numpy() == 1))
    fair = np.array([_phi(abs(x)) for x in te.dz.to_numpy()])  # what price/time alone implies (≈ the market)
    res = dict(w=[round(float(x), 5) for x in wts], mu=[round(float(x), 6) for x in mu], sd=[round(float(x), 6) for x in sd])
    for name, lo, hi in (("lock", 0.90, 1.01), ("hc", 0.75, 0.90)):
        msk = (conf >= lo) & (conf < hi)
        res[f"{name}_n"] = int(msk.sum()); res[f"{name}_acc"] = round(float(right[msk].mean()), 3) if msk.any() else 0
        res[f"{name}_fair"] = round(float(fair[msk].mean()), 3) if msk.any() else 0
        early = msk & (te.tleft.to_numpy() * 12 >= 5)  # 5+ minutes before the end
        res[f"{name}_early_n"] = int(early.sum()); res[f"{name}_early_acc"] = round(float(right[early].mean()), 3) if early.any() else 0
    res["ok"] = bool(res["lock_n"] >= 100 and res["lock_acc"] >= 0.90)
    return res


PFEATS = FEATS + ("volx", "score")


def proj_frame(df):
    f, sig = feat_frame(df)
    r = np.log(df.Close).diff()
    f["volx"] = (r.rolling(30).std() / (r.rolling(390, min_periods=60).std() + 1e-12)).clip(0, 5)
    sc, d, _, _ = spike_parts(df.Close, df.High, df.Low, df.Volume.fillna(0), df.Open)
    f["score"] = (sc * d.fillna(0) / 100).clip(-1, 1)  # signed spike score
    return f, sig


def proj_stats(df):
    """Projection model: expected move over 5/10 min (in σ units) + chance of a SHARP move (>1.5σ) up/down in 10 min.
    Trained on older 70%, judged on newest 30%."""
    df = df.resample("1min").last().dropna(how="all"); c = df.Close
    f, sig = proj_frame(df)
    y5 = np.log(c.shift(-5) / c) / (sig * np.sqrt(5)); y10 = np.log(c.shift(-10) / c) / (sig * np.sqrt(10))
    d = pd.concat([f, y5.rename("y5"), y10.rename("y10")], axis=1).dropna()
    if len(d) < 3000: return {"ok": False}
    cut = int(len(d) * 0.7); tr, te = d.iloc[:cut], d.iloc[cut:]
    mu, sd = tr[list(PFEATS)].mean(), tr[list(PFEATS)].std() + 1e-9
    X = np.c_[np.ones(len(tr)), ((tr[list(PFEATS)] - mu) / sd).to_numpy()]
    Xt = np.c_[np.ones(len(te)), ((te[list(PFEATS)] - mu) / sd).to_numpy()]
    ridge = lambda y: np.linalg.solve(X.T @ X + 5 * np.eye(X.shape[1]), X.T @ y)
    b5, b10 = ridge(tr.y5.to_numpy()), ridge(tr.y10.to_numpy())
    p10 = Xt @ b10; hit10 = float(((p10 > 0) == (te.y10.to_numpy() > 0))[np.abs(p10) > 0.15].mean())
    res = dict(mu=[round(float(x), 6) for x in mu], sd=[round(float(x), 6) for x in sd],
               b5=[round(float(x), 5) for x in b5], b10=[round(float(x), 5) for x in b10], dir_hit=round(hit10, 3))
    for side, cond in (("up", lambda y: y > 1.5), ("dn", lambda y: y < -1.5)):
        Ytr = cond(tr.y10).astype(float).to_numpy(); Yte = cond(te.y10).astype(float).to_numpy()
        w = _fit_logit(X[:, 1:], Ytr, 400); pt = 1 / (1 + np.exp(-(Xt @ w)))
        base = float(Yte.mean()); top = pt >= np.quantile(pt, 0.9)
        res[f"w_{side}"] = [round(float(x), 5) for x in w]; res[f"base_{side}"] = round(base, 4)
        res[f"lift_{side}"] = round(float(Yte[top].mean() / (base + 1e-9)), 2); res[f"top_{side}"] = round(float(Yte[top].mean()), 3)
    res["ok"] = bool(res["dir_hit"] >= 0.53)
    res["ok_big"] = bool(min(res["lift_up"], res["lift_dn"]) >= 1.5)
    return res


BOOM = dict(proj=0.3, score=0.45, add_dz=0.5, add_max=0.80, exit_score=0.45, peak=0.60, cash=0.92)


def boom_stats(df, pm):
    """BOOMING backtest with the live rules: enter when projection + spike score + momentum + trend all point the
    same way (6-12 min left); DOUBLE DOWN only after confirmation (+0.5σ, contract <80%, ≥3 min left);
    CASH OUT when the spike fades, the contract hits 92%, or 1 min left. Contract value ≈ fair odds ±2¢ spread."""
    if not pm or not pm.get("b10"): return {"ok": False}
    df = df.resample("1min").last().dropna(how="all"); c = df.Close; w = df.index.floor("15min")
    f, sig = proj_frame(df); X = f[list(PFEATS)]
    z = np.c_[np.ones(len(X)), ((X - np.array(pm["mu"])) / np.array(pm["sd"])).to_numpy()]
    r10 = pd.Series(z @ np.array(pm["b10"]), index=df.index)
    start = c.shift(1).groupby(w).transform("first"); end = c.groupby(w).transform("last")
    T = pd.Series(14 - (df.index.tz_convert(ET).minute % 15), index=df.index)
    dz = np.log(c / start) / (sig * np.sqrt(np.maximum(T, 1)))
    D = pd.DataFrame({"w": w, "r10": r10, "sc": f.score, "m3": f.m3, "tr": f.trend, "dz": dz, "T": T,
                      "won_up": end >= start}).dropna()
    trades = []
    for wk, g in D.groupby("w"):
        if len(g) < 8: continue
        cand = g[(g["T"].between(6, 12)) & (g.r10.abs() >= BOOM["proj"])]
        cand = cand[(np.sign(cand.r10) == np.sign(cand.sc)) & (cand.sc.abs() >= BOOM["score"]) &
                    (np.sign(cand.m3) == np.sign(cand.r10)) & (np.sign(cand.tr) == np.sign(cand.r10))]
        if not len(cand): continue
        e = cand.iloc[0]; d = 1 if e.r10 > 0 else -1; val = lambda x: _phi(x) if d > 0 else 1 - _phi(x)
        v0 = val(e.dz); costs = [v0 + 0.02 + kfee(v0)]; added = False; peak = abs(e.sc); exit_v = None
        for _, r in g[g.index > e.name].iterrows():
            v = val(r.dz); peak = max(peak, r.sc * d)
            if not added and (r.dz - e.dz) * d >= BOOM["add_dz"] and v < BOOM["add_max"] and r["T"] >= 3:
                costs.append(v + 0.02 + kfee(v)); added = True
            if (peak >= BOOM["peak"] and r.sc * d < BOOM["exit_score"]) or v >= BOOM["cash"] or r["T"] <= 1:
                exit_v = max(v - 0.02, 0); break
        payout = exit_v if exit_v is not None else float(e.won_up if d > 0 else not e.won_up)
        trades.append((wk, len(costs) * payout - sum(costs), sum(costs), float(e.won_up if d > 0 else not e.won_up)))
    if len(trades) < 60: return {"ok": False, "n": len(trades)}
    t = pd.DataFrame(trades, columns=["w", "pnl", "cost", "dir_right"]); cut = int(len(t) * 0.7); res = {"n": len(t)}
    for name, part in (("train", t.iloc[:cut]), ("test", t.iloc[cut:])):
        res[f"{name}_roi"] = round(float(part.pnl.sum() / part.cost.sum()), 3); res[f"{name}_win"] = round(float((part.pnl > 0).mean()), 3)
        res[f"{name}_dir"] = round(float(part.dir_right.mean()), 3)
    res["ok"] = bool(res["test_roi"] > 0.05 and res["test_win"] >= 0.55 and res["train_roi"] > 0 and len(t) - cut >= 30)
    return res


def proj_live(m, pm, sig1):
    """Projected % move in 5/10 min and sharp-move chances for the latest bar."""
    if not pm or not pm.get("b10"): return None
    f, _ = proj_frame(m); x = f.iloc[-1][list(PFEATS)]
    if x.isna().any(): return None
    z = np.r_[1.0, (x.to_numpy() - np.array(pm["mu"])) / np.array(pm["sd"])]
    r5, r10 = float(z @ np.array(pm["b5"])), float(z @ np.array(pm["b10"]))
    pu = float(1 / (1 + np.exp(-(z @ np.array(pm["w_up"]))))); pd_ = float(1 / (1 + np.exp(-(z @ np.array(pm["w_dn"])))))
    return dict(m5=r5 * sig1 * np.sqrt(5), m10=r10 * sig1 * np.sqrt(10), big_up=pu, big_dn=pd_,
                base_up=pm["base_up"], base_dn=pm["base_dn"], p_ok=pm.get("ok"), big_ok=pm.get("ok_big"), dir_hit=pm.get("dir_hit"))


def window_live(m, wm, dz, T):
    """P(window ends UP) right now from our model."""
    if not wm or not wm.get("w"): return None
    f, _ = feat_frame(m); x = f.iloc[-1][list(FEATS)]
    if x.isna().any(): return None
    v = np.r_[x.to_numpy(), np.clip(dz, -6, 6), T / 12]
    z = (v - np.array(wm["mu"])) / np.array(wm["sd"])
    return float(1 / (1 + np.exp(-(wm["w"][0] + z @ np.array(wm["w"][1:])))))


def forecast_live(m, fc):
    """P(up in 10 min) for the latest bar using a stored model."""
    if not fc or not fc.get("w"): return None
    f, _ = feat_frame(m); x = f.iloc[-1][list(FEATS)]
    if x.isna().any(): return None
    z = (x.to_numpy() - np.array(fc["mu"])) / np.array(fc["sd"])
    return float(1 / (1 + np.exp(-(fc["w"][0] + z @ np.array(fc["w"][1:])))))


LOCK_B = (0.90, 0.95, 0.98)


def lock_stats(df):
    """How often the leading side really wins when random-walk math says 90%+ (per bucket, per minutes-left band)."""
    df = df.resample("1min").last().dropna(how="all"); c = df.Close; w = df.index.floor("15min")
    full = pd.Series(1, index=df.index).groupby(w).transform("size") >= 8
    start = c.shift(1).groupby(w).transform("first"); end = c.groupby(w).transform("last")
    T = 14 - (df.index.tz_convert(ET).minute % 15)
    sig = np.log(c).diff().rolling(390, min_periods=60).std()
    dz = (np.log(c / start) / (sig * np.sqrt(np.maximum(T, 1)))).abs()
    lead = pd.Series([_phi(x) if x == x else np.nan for x in dz], index=df.index)
    won = ((end >= start) == (c >= start))
    d = pd.DataFrame({"lead": lead, "won": won, "T": T})[full & (T >= 1) & (T <= 12) & (lead >= LOCK_B[0])].dropna()
    out = {}
    for lo, hi in zip(LOCK_B, LOCK_B[1:] + (1.01,)):
        g = d[(d.lead >= lo) & (d.lead < hi)]
        if len(g) >= 100: out[f"{lo:.2f}"] = [len(g), round(float(g.won.mean()), 4)]
    return out


def lock_rate(cal, lead):
    """Measured win rate for a math-probability `lead` (falls back to a haircut of the math)."""
    tab = (cal or {}).get("lock") or {}; key = None
    for lo in LOCK_B:
        if lead >= lo: key = f"{lo:.2f}"
    return (tab[key][1], tab[key][0]) if key in tab else (lead - 0.03, 0)


def tier(p):
    return "NEAR LOCK" if p >= 0.90 else "HIGH CONFIDENCE" if p >= 0.75 else ""


def spike_stats(df):
    """Backtest: first minute per 15-min window (4-12 min left) with spike score ≥70 → buy that direction's contract."""
    df = df.resample("1min").last().dropna(how="all"); c = df.Close; w = df.index.floor("15min")
    score, d, z3, sig = spike_parts(c, df.High, df.Low, df.Volume.fillna(0), df.Open)
    start = c.shift(1).groupby(w).transform("first"); end = c.groupby(w).transform("last")
    T = 14 - (df.index.tz_convert(ET).minute % 15)
    ok = (score >= 70) & (T >= 4) & (T <= 12) & sig.notna() & (d != 0)
    x = pd.DataFrame({"w": w, "d": d, "dz": np.log(c / start) / (sig * np.sqrt(np.maximum(T, 1))),
                      "won": np.where(d > 0, end >= start, end < start)})[ok].groupby("w").head(1)
    if len(x) < 60: return {"n": len(x), "ok": False}
    cut = int(len(x) * 0.7); res = {"n": len(x)}
    for name, part in (("train", x.iloc[:cut]), ("test", x.iloc[cut:])):
        pnl = cost = 0
        for _, r in part.iterrows():
            price = (_phi(r.dz) if r.d > 0 else 1 - _phi(r.dz)) + 0.02
            if price >= 0.9: continue
            pnl += float(r.won) - price - kfee(price); cost += price
        res[f"{name}_roi"] = round(pnl / cost, 3) if cost else 0; res[f"{name}_win"] = round(float(part.won.mean()), 3)
    res["ok"] = bool(res["train_roi"] > 0.02 and res["test_roi"] > 0.03 and len(x) - cut >= 25)
    return res


def calibrate(mkt):
    drift, spike, fcast, lock, wmod, proj, boom = {}, {}, {}, {}, {}, {}, {}
    try:
        fdf = fetch_fut_1m(mkt); rows = ls_rows(fdf, rth=False); src = "yahoo futures 30d"; drift = drift_stats(fdf)
        spike = spike_stats(fdf); fcast = forecast_stats(fdf); lock = lock_stats(fdf); wmod = window_stats(fdf); proj = proj_stats(fdf); boom = boom_stats(fdf, proj)
    except Exception as e:
        print(mkt, "futures 1m failed:", e); rows = ls_rows(fetch(mkt, "1m", 60)); src = "etf 60d"
    cut = int(len(rows) * 0.7); tr, te = rows.iloc[:cut], rows.iloc[cut:]
    tab = {k: [len(g), round(float(g.won.mean()), 3)] for k, g in tr.groupby("key") if len(g) >= 25}
    stab = {k: [len(g), round(float(g.won.mean()), 3)] for k, g in tr.groupby("skey") if len(g) >= 25}
    res = dict(table=tab, stable=stab, setups=len(rows), src=src, drift=drift, spike=spike, fcast=fcast, lock=lock, wmod=wmod, proj=proj, boom=boom)
    for scope, part in (("all", te), ("night", te[~te.skey.str.startswith("US")])):
     for typ in ("ls", "fav"):  # validation on unseen 30%, session-aware table (same table day & night)
        nt = part
        pnl = cost = n = 0
        for _, r in nt.iterrows():
            cell = stab.get(r.skey)
            if not cell or (typ == "ls") != bool(r.turn): continue
            fair_b = _phi(-r.dist); price = (fair_b if typ == "ls" else 1 - fair_b) + 0.02
            p = cell[1] if typ == "ls" else 1 - cell[1]; won = r.won if typ == "ls" else not r.won
            if (price <= LS_MAX_COST if typ == "ls" else price < 0.92) and p - price - kfee(price) >= (LS_MIN_EDGE if typ == "ls" else FAV_MIN_EDGE):
                pnl += won - price - kfee(price); cost += price; n += 1
        res[f"{scope}_{typ}_n"], res[f"{scope}_{typ}_roi"] = n, round(pnl / cost, 3) if cost else 0
        res[f"{scope}_{typ}_ok"] = bool(n >= 15 and cost and pnl / cost > 0.03)
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
    res["_cal"] = {m: calibrate(m) for m in ALL}
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
KSERIES = {**{k: [] for k in ("BTC", "ETH", "SOL", "XRP", "DOGE", "BNB", "HYPE", "NEAR", "ZEC", "EURUSD", "GBPUSD", "USDJPY")},
           "BRENT": ["KXBRENTD"], "WTI": ["KXWTIH", "KXWTI"], "NATGAS": ["KXNATGASD"], "GOLD": ["KXGOLDH"],
           "SILVER": ["KXSILVERH"], "COPPER": [], "PLATINUM": ["KXPLATINUMH"], "PALLADIUM": ["KXPALLADIUMH"]}
NAME = {"BRENT": "BRENT", "WTI": "WTI", "NATGAS": "NAT GAS", "GOLD": "GOLD", "SILVER": "SILVER", "COPPER": "COPPER",
        "PLATINUM": "PLATINUM", "PALLADIUM": "PALLADIUM", "BTC": "BTC", "ETH": "ETH", "SOL": "SOL", "XRP": "XRP", "DOGE": "DOGE",
        "BNB": "BNB", "HYPE": "HYPE", "NEAR": "NEAR", "ZEC": "ZEC", "EURUSD": "EUR/USD", "GBPUSD": "GBP/USD", "USDJPY": "USD/JPY"}
DEC = {"NATGAS": 3, "SILVER": 3, "COPPER": 4, "BTC": 0, "XRP": 4, "DOGE": 5, "HYPE": 3, "NEAR": 3, "EURUSD": 5, "GBPUSD": 5, "USDJPY": 3}
REASON = {"STOP": "hit your stop: cut the loss", "TARGET": "hit the target 🎯", "TIME": "idea timed out",
          "END OF DAY": "market closing soon"}
_KC, _KR, _PICK = {}, {}, {}


def money(mkt, x): return f"{'' if mkt in FX else '$'}{x:,.{DEC.get(mkt, 2)}f}"


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


BIG_X = float(os.getenv("BIG_X") or 10)
MIN_PROB = float(os.getenv("MIN_PROB") or 0.62)
FAST_ON = os.getenv("FAST_CALLS", "0") == "1"           # 1-min momentum calls tested below MIN_PROB: off (same rules day & night)      # every call must have at least this win chance
LONGSHOTS = os.getenv("LONGSHOTS", "0") == "1"        # low-win-rate cheap bets: off unless enabled
CALL_LOG = "calls.jsonl"
MODEL_V = 2  # v2 = probabilities anchored to Kalshi's 15-min price; learning uses only this version's results


def log_call(mkt, pos, won, st=None):
    """Permanent record of every call's outcome (for live accuracy tracking)."""
    k = pos.get("k") or {}
    rec = dict(t=dt.datetime.now(ET).isoformat(timespec="minutes"), mkt=mkt, kind=pos.get("kind"), side=k.get("side"),
               cost=k.get("cost"), prob=pos.get("prob"), at=pos.get("at"), won=bool(won),  # won = prediction right AT SETTLEMENT
               close=pd.Timestamp(k["close"]).tz_convert(ET).isoformat(timespec="minutes") if k.get("close") else None,
               took_profit=bool(pos.get("took_profit")), was_behind=bool(pos.get("behind")), model_v=MODEL_V)
    try:
        with open(CALL_LOG, "a") as f: f.write(json.dumps(rec) + "\n")
    except Exception as e: print("log_call", e)


def scorecard(st):
    """Half-hour scorecard, sent only once every call whose window ended in that half-hour has a settled result."""
    now = dt.datetime.now(ET)
    if now.minute % 30 == 0 and st.get("scoreslot") != now.strftime("%Y-%m-%d %H:%M"):
        st["scoreslot"] = now.strftime("%Y-%m-%d %H:%M")
        st["score_due"] = now.replace(second=0, microsecond=0).isoformat()   # report this half-hour once results are in
    due = st.get("score_due")
    if not due: return
    due = pd.Timestamp(due)
    pending = [m for m, p in (st.get("lpos") or {}).items() if pd.Timestamp(p["k"]["close"]).tz_convert(ET) <= due]
    waited = (pd.Timestamp(now) - due).total_seconds() / 60
    if pending and waited < 15: return  # results not in yet: wait
    st["score_due"] = None
    try: log = pd.read_json(CALL_LOG, lines=True)
    except Exception: log = pd.DataFrame(columns=["close", "mkt", "won", "kind"])
    if len(log):
        log["c"] = pd.to_datetime(log["close"].fillna(log["t"]), utc=True).dt.tz_convert(ET)
        if "kind" in log: log = log[log.kind.fillna("") != "flip"]  # re-entries never count
    lo = due - pd.Timedelta(minutes=30)
    half = log[(log.c > lo) & (log.c <= due)] if len(log) else log
    today = log[(log.c.dt.date == due.date()) & (log.c <= due)] if len(log) else log
    if not len(today) and not pending: return  # nothing to report
    cnt = lambda d: (int(d.won.astype(bool).sum()), int((~d.won.astype(bool)).sum())) if len(d) else (0, 0)
    r30, w30 = cnt(half); rt, wt = cnt(today)
    lines = [f"Windows {lo:%-I:%M}–{due:%-I:%M}: {r30} right, {w30} wrong" + (f" ({r30 / (r30 + w30):.0%})" if r30 + w30 else ""),
             f"Today: {rt} right, {wt} wrong" + (f" ({rt / (rt + wt):.0%})" if rt + wt else "")]
    if len(half):
        lines.append("By market: " + ", ".join(f"{NAME.get(k, k)} {cnt(g)[0]}-{cnt(g)[1]}" for k, g in half.groupby("mkt")))
    if pending: lines.append(f"Still settling (not counted): {', '.join(NAME[m] for m in pending)}")
    lines.append("All results above are settled by Kalshi. Scored on whether each call's prediction was right at the close.")
    notify(f"Scorecard {lo:%-I:%M}–{due:%-I:%M}: {r30} right, {w30} wrong", "\n".join(lines), "default")


def learn_update(st):
    """Live record per (market, call type) → adjusted bar and probability blend. Runs after each settled result."""
    try: log = pd.read_json(CALL_LOG, lines=True)
    except Exception: return
    if not len(log): return
    log = log[log.kind.fillna("") != "flip"]
    log = log[log.get("model_v", pd.Series(1, index=log.index)).fillna(1) == MODEL_V]  # learn from the current model only
    out = {}
    if not len(log): st["learn"] = {}; st.pop("platt", None); return
    for (m, k), g in log.groupby(["mkt", "kind"]):
        n, w = len(g), int(g.won.astype(bool).sum()); exp_ = float(g.prob.fillna(MIN_PROB).mean())
        out[f"{m}|{k}"] = dict(n=n, w=w, rate=round(w / n, 3), expected=round(exp_, 3))
    st["learn"] = out
    if len(log) >= 20 and log.prob.notna().sum() >= 20:  # re-fit: P(win) = σ(a + b·logit(stated))
        g = log[log.prob.notna()]; x = np.log(np.clip(g.prob, 0.01, 0.99) / (1 - np.clip(g.prob, 0.01, 0.99))).to_numpy()
        y = g.won.astype(float).to_numpy(); a_, b_ = 0.0, 1.0
        for _ in range(800):
            p = 1 / (1 + np.exp(-(a_ + b_ * x))); ga = np.mean(p - y) + 0.02 * a_; gb = np.mean((p - y) * x) + 0.02 * (b_ - 1)
            a_ -= 0.3 * ga; b_ -= 0.3 * gb
        st["platt"] = dict(a=round(float(a_), 4), b=round(float(b_), 4), n=int(len(g)))


def need_prob(st, mkt, kind):
    """Win chance a call must have: base 62%, raised for combos losing live, lowered (min 60%) for ones beating forecast."""
    L = (st.get("learn") or {}).get(f"{mkt}|{kind}")
    if not L or L["n"] < 6: return MIN_PROB
    gap = L["rate"] - L["expected"]
    if L["n"] >= 10 and L["rate"] < 0.45: return 1.01           # keeps losing → switched off
    return float(min(0.95, max(0.60, MIN_PROB - 0.5 * gap)))    # behind forecast → stricter; ahead → a bit looser


def blend_prob(st, mkt, kind, p):
    """Re-fit to live results (all calls), then shrink toward this market+type's own record (k=10 pseudo-calls)."""
    pl = st.get("platt")
    if pl:
        q = min(max(p, 0.01), 0.99); p = float(1 / (1 + np.exp(-(pl["a"] + pl["b"] * np.log(q / (1 - q))))))
    L = (st.get("learn") or {}).get(f"{mkt}|{kind}")
    if not L or not L["n"]: return p
    adj = p + (L["rate"] - L["expected"]) * L["n"] / (L["n"] + 10)
    return float(min(0.99, max(0.01, adj)))


def agrees(st, mkt, up):
    """Multi-timeframe agreement: last 5 min moving the call's way, and trend or order flow backing it."""
    a = (st.get("ana") or {}).get(mkt) or {}
    if not a: return True
    sgn = 1 if up else -1
    if a.get("ch5", 0) * sgn < -0.0003: return False
    return a.get("tr_pct", 0) * sgn > 0 or a.get("flow", 0) * sgn > 0.1  # payout multiple that counts as a big-payout (green) bet


def badge(cost):
    """🟩 big payout (≥10× back) vs 🟦 normal bet."""
    return "🟩 BIG PAYOUT" if cost and 1 / cost >= BIG_X else "🟦"


def call_time(pos):
    """How a call is referred to: by the time it was sent, e.g. '6:42 PM call'."""
    return f"{pos.get('at', '?')} call"


def new_trade(st, mkt, pos, lv, px):
    st["seq"] = st.get("seq", 0) + 1
    pos.update(id=st["seq"], at=dt.datetime.now(ET).strftime("%-I:%M %p"), at_px=lv(px))
    return st["seq"]


def busy(st, mkt): return any(mkt in st.get(k, {}) for k in ("pos", "fpos", "lpos"))




K15 = {"BTC": "KXBTC15M", "ETH": "KXETH15M", "SOL": "KXSOL15M", "XRP": "KXXRP15M", "DOGE": "KXDOGE15M", "BNB": "KXBNB15M",
       "HYPE": "KXHYPE15M", "NEAR": "KXNEAR15M", "ZEC": "KXZEC15M", "EURUSD": "KXEURUSD15M", "GBPUSD": "KXGBPUSD15M",
       "USDJPY": "KXUSDJPY15M", "BRENT": "KXBRENT15M", "WTI": "KXWTI15M", "NATGAS": "KXNATGAS15M", "GOLD": "KXGOLD15M", "SILVER": "KXSILVER15M",
       "COPPER": "KXCOPPER15M", "PLATINUM": "KXPLATINUM15M", "PALLADIUM": "KXPALLADIUM15M"}


def k15(mkt):
    """Current Kalshi 15-minute up/down contract for this market (cached 15s)."""
    key = f"15|{mkt}"
    if (c := _KC.get(key)) and time.time() - c["t"] < 8: return c
    try:
        ms = requests.get(f"{KALSHI}/markets", params={"series_ticker": K15[mkt], "status": "open", "limit": 5}, timeout=10).json().get("markets", [])
    except Exception: return None
    ms = [x for x in ms if x.get("floor_strike") is not None]  # start price not set yet → not tradable yet
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
        return f"\nKalshi {info['side']}: settled {'$1 (won)' if won else '$0 (lost)'} (bought at {paid:.0f}¢)", won
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
            sent.add(k); notify("Big report today", e + "\nExpect sudden jumps around that time.", "high")
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
        trend = "up" if r.Close > r.ema and r.mom > 0 else "down" if r.Close < r.ema and r.mom < 0 else "sideways"
        pos = (st.get("pos") or {}).get(mkt)
        lines.append(f"{COLOR[mkt][0]} {NAME[mkt]}  {lv(r.Close)}  {'▲' if chg >= 0 else '▼'}{abs(chg):.1f}%\n"
                     f"    Trend: {trend}\n    Usual daily swing: ±{rng:.1f}%"
                     + ("\n    Quiet, big move likely" if r.sq else "")
                     + (f"\n    Open {call_time(pos)}: {'UP' if pos['side'] > 0 else 'DOWN'}" if pos else ""))
    ev = events(hours=14)
    notify(f"Market check {dt.datetime.now(ET):%-I:%M %p}", "\n\n".join(lines + (["Today: " + "; ".join(ev)] if ev else [])))


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
        sp.run(f'git add state.json; git add {CALL_LOG} 2>/dev/null; (git diff --cached --quiet || (git commit -qm "{msg}" && git pull -q --rebase origin main && git push -q))',
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
    """Day board for oil & gas, rendered from the live analysis."""
    lines = [board_line(m, st["ana"][m], st) for m in MARKETS if (st.get("ana") or {}).get(m)]
    if lines: notify(f"Oil & gas board {dt.datetime.now(ET):%-I:%M %p}", "\n".join(lines), "low")


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
KIND = {"boom": "BOOMING", "pre": "Sharp move ahead", "lock": "Near lock", "spike": "🔥 Spike", "drift": "📊 Session drift", "fast": "⚡ Fast move", "ls": "🎯 Longshot", "fav": "💪 Edge pick", "ihm": "📈 Close pattern", "flip": "🔄 Flip"}


def sess(close):
    close = pd.Timestamp(close).tz_convert(ET)
    return f"{(close - pd.Timedelta(minutes=15)):%-I:%M}–{close:%-I:%M}"


def call_txt(mkt, k):
    return f"price ends {'AT/ABOVE' if k['side'] == 'YES' else 'BELOW'} {money(mkt, k['k'])} at {pd.Timestamp(k['close']).tz_convert(ET):%-I:%M}"


def ctx_short(cx, up):
    """One line: trend · flow · RSI."""
    tr = f"4h trend {'up' if cx['trend'] > 0 else 'down'}{'' if (cx['trend'] > 0) == up else ' (against)'}"
    fl = "buyers in control" if cx["flow"] > 0.1 else "sellers in control" if cx["flow"] < -0.1 else ""
    if fl and cx["flow"] * (1 if up else -1) < 0: fl += " (against)"
    return ", ".join(x for x in (tr, fl) if x)


def ctx_bullets(cx, up, lv):
    tr = "UP ↗️" if cx["trend"] > 0 else "DOWN ↘️"
    return "\n".join([
        f"• 4h trend {tr}: {'supports' if (cx['trend'] > 0) == up else 'against'} this call",
        f"• VWAP {lv(cx['vwap'])}: price is {'above' if cx['px'] > cx['vwap'] else 'below'} today's average",
        f"• Last 5 min: {'buyers' if cx['flow'] > 0.1 else 'sellers' if cx['flow'] < -0.1 else 'nobody'} in control "
        f"({'supports' if cx['flow'] * (1 if up else -1) > 0.1 else 'neutral' if abs(cx['flow']) <= 0.1 else 'against'})",
        f"• RSI {cx['rsi']:.0f} · today {cx['day']:+.1f}%"])


def level_for(start, q_side, up, mins, sig):
    """Price at which the bet (UP or DOWN) would have win-chance q_side with `mins` left."""
    from math import exp, sqrt
    from statistics import NormalDist
    if not sig or mins <= 0: return None
    q = min(max(q_side, 0.02), 0.98); z = NormalDist().inv_cdf(q if up else 1 - q)
    return start * exp(z * sig * sqrt(mins))


def open_call(st, mkt, kind, side, c, lv, px, odds, why, tested, parent=None, prob=None):
    """Create a numbered call on the current 15-min contract and send the BUY message."""
    cost = c["ya"] if side == "YES" else c["na"]
    k = dict(ticker=c["ticker"], side=side, cost=cost, k=c["k"], close=str(c["close"]))
    tp = (min(0.95, max(2.5 * cost, cost + 0.25)) if kind == "ls" else
          0.97 if kind == "lock" else min(0.92, cost + max(0.12, (1 - cost) * 0.55)))  # scalp: sell into the move
    bail = max(0.03, cost * 0.5)
    if kind == "lock": tp, bail = 0.995, 0.60  # hold to the end; bail only if it really reverses
    pos = dict(side=1 if side == "YES" else -1, entry=px, stop=0, tgt=0, best=px, n=0, t0=time.time(), kind=kind, k=k,
               tp=tp, bail=bail, parent=parent, prob=prob)
    st.setdefault("lpos", {})[mkt] = pos; st.setdefault("lswin", {})[mkt] = c["ticker"]
    n = new_trade(st, mkt, pos, lv, px)
    left = (c["close"] - pd.Timestamp.now(tz="UTC")).total_seconds() / 60
    up = side == "YES"; big = 1 / cost >= BIG_X; prob = prob or None
    tg = tier(prob) if prob else ""
    if tg == "NEAR LOCK" and kind != "lock": tg = "HIGH CONFIDENCE"  # NEAR LOCK only from our window model
    close_t = pd.Timestamp(k["close"]).tz_convert(ET).strftime("%-I:%M")
    title = (f"{NAME[mkt]}: " + (f"BOOMING {'UP' if up else 'DOWN'} · " if kind == "boom" else "") + f"BUY {'UP' if up else 'DOWN'} · " + (f"{prob:.0%} to hit by {close_t}" if prob else f"by {close_t}")
             + (f" · {tg}" if tg else "") + (f" · BIG PAYOUT {1 / cost:.0f}x" if big else ""))
    sig = _SIG.get(mkt); tl = max(left * 0.6, 1)
    tpx = level_for(k["k"], tp, up, tl, sig)
    pk = lambda x: money(mkt, x)
    gain_tp = (tp - cost - kfee(cost)) / cost
    exits = (f"Sell high: when the bet is up about +{gain_tp:.0%}" + (f" (likely once {NAME[mkt].title()} {'reaches' if up else 'drops to'} "
             f"about {pk(tpx)})" if tpx else "") + ". If it doesn't get there, hold to the end."
             if kind != "lock" else "Hold to the end (near lock).")
    L = (st.get("learn") or {}).get(f"{mkt}|{kind}")
    rec = f" Live record for this call type here: {L['w']}-{L['n'] - L['w']}." if L else ""
    notify(title,
           f"Buy {'UP' if up else 'DOWN'}: wins if {NAME[mkt].title()} ends {'at or above' if up else 'below'} "
           f"{money(mkt, k['k'])} at {pd.Timestamp(k['close']).tz_convert(ET):%-I:%M} ({left:.0f} min left). Now {lv(px)}.\n"
           f"{exits} {odds[0].upper() + odds[1:]}.\n"
           f"Why: {why}." + ("" if tested else " Untested: small size.") + rec
           + (f"\n{analysis_block(mkt, st['ana'][mkt])}" if (st.get("ana") or {}).get(mkt) else ""),
           "urgent", mkt)
    return n


def sell_msg(mkt, pos, title, px, lv, extra=""):
    """Legacy exits (slow/fast engines without a 15-min contract)."""
    if pos.get("k"): return follow_msg(mkt, pos, "🔔", title, extra)
    notify(f"{NAME[mkt]} · {title} · {call_time(pos)}", f"Price now {lv(px)}" + extra, "urgent", mkt)


def follow_msg(mkt, pos, icon, action, extra=""):
    k = pos["k"]
    notify(f"{NAME[mkt]}: {action} · {call_time(pos)}",
           f"The {call_time(pos)} was BUY {'UP' if k['side'] == 'YES' else 'DOWN'}: needed {NAME[mkt].title()} "
           f"{'at or above' if k['side'] == 'YES' else 'below'} {money(mkt, k['k'])} at {pd.Timestamp(k['close']).tz_convert(ET):%-I:%M}." + extra,
           "urgent", mkt)


def odds_line(p, cost, label="Odds"):
    e = p - cost - kfee(cost)
    return (f"win chance {p:.0%} vs market {cost:.0%}" + (" (good value)" if e >= 0.03 else " (fair)" if e > -0.03 else " (overpriced)"))


def mkt_dz(c):
    """Where Kalshi's 15-min contract says price is vs the start, in σ√T units (it knows the true settlement price)."""
    from statistics import NormalDist
    mid = (c["ya"] + c["yb"]) / 2 if c.get("yb") else c["ya"]
    return NormalDist().inv_cdf(min(max(mid, 0.02), 0.98)), mid


def analyze(mkt, m, kp, lv, c, fc=None, wm=None, pm=None):
    """Numbers behind the board/alerts: move, σ, breakout, volatility, spike score, range & odds for this window."""
    from math import sqrt
    cl = m.Close
    if len(cl) < 60: return None
    p = cl.copy(); p.iloc[-1] = kp / getattr(lv, "r", 1.0)  # latest = live price (in source units)
    score, d, z3, sig = spike_parts(p, m.High, m.Low, m.Volume.fillna(0), m.Open)
    s1 = float(sig.iloc[-1]) if sig.notna().iloc[-1] else float(np.log(p).diff().std())
    r = np.log(p).diff(); volx = float(r.tail(30).std() / (r.tail(390).std() + 1e-12))
    a = dict(s1=s1, px=kp, ch5=float(p.iloc[-1] / p.iloc[-6] - 1), z3=float(z3.iloc[-1] or 0), score=float(score.iloc[-1] or 0),
             dir=int(d.iloc[-1] or 0), volx=volx, spark=spark(p.tail(12).values),
             hi30=float(m.High.iloc[-33:-3].max() * getattr(lv, "r", 1.0)), lo30=float(m.Low.iloc[-33:-3].min() * getattr(lv, "r", 1.0)))
    if c:
        T = max((c["close"] - pd.Timestamp.now(tz="UTC")).total_seconds() / 60, 0.1)
        dzm, mid = mkt_dz(c)
        a.update(T=T, start=c["k"], rng=kp * s1 * sqrt(T), p_up=mid, ya=c["ya"], na=c["na"])  # odds = Kalshi's, not our estimate
        mm0 = m.copy(); mm0.iloc[-1, mm0.columns.get_loc("Close")] = p.iloc[-1]
        wp = window_live(mm0, wm, dzm, T)  # our signals adjust Kalshi's view; they can't replace it
        if wp is not None: a.update(wm_p=wp, wm_ok=bool((wm or {}).get("ok")), wm_acc=(wm or {}).get("lock_acc", 0),
                                    wm_n=(wm or {}).get("lock_n", 0), wm_hc=(wm or {}).get("hc_acc", 0))
    tr_, vw_, rs_, fl_ = ctx_features(p, m.Volume.fillna(0), m.index, m.Open)
    ema = p.ewm(span=240, adjust=False).mean()
    a.update(tr_pct=float(p.iloc[-1] / ema.iloc[-1] - 1), m60=float(p.iloc[-1] / p.iloc[-61] - 1) if len(p) > 61 else 0.0,
             vw_pct=float(p.iloc[-1] / vw_.iloc[-1] - 1), rsi=float(rs_.iloc[-1]), flow=float(fl_.fillna(0).iloc[-1]),
             sess=session(dt.datetime.now(ET)))
    mm = m.copy(); mm.iloc[-1, mm.columns.get_loc("Close")] = p.iloc[-1]
    pj = proj_live(mm, pm, s1)
    if pj:
        a.update(pj); a["px5"] = kp * float(np.exp(pj["m5"])); a["px10"] = kp * float(np.exp(pj["m10"]))
    pu = forecast_live(mm, fc)
    if pu is not None:
        a.update(fc_p=pu, fc_ok=bool((fc or {}).get("ok")), fc_acc=(fc or {}).get("acc_conf", 0),
                 fc_move=kp * s1 * sqrt(FC_H) * (fc or {}).get("move", 0.7))
    dn = {1: "up", -1: "down"}.get(a["dir"], "")
    a["label"] = (f"BOOMING {dn}" if boom_signal(a) else None) or (f"SPIKE {dn}" if a["score"] >= 70 else f"move building {dn}" if a["score"] >= 45
                  else "coiled, move coming" if volx < 0.6 else "steady")
    return a


SESS_NOTE = {"EVE": "evening session: moves tend to keep going (snap-backs only 4-10%)",
             "ASIA": "Asia session: thin trading, some snap-backs (10-16%)",
             "EU": "Europe session: London open, most snap-backs for oil (16-19%)",
             "US": "US day session: snap-backs 7-15%"}


def analysis_block(mkt, a):
    """All factors, graphically and numerically, in three lines."""
    if not a: return ""
    fl = a.get("flow", 0); fs = f"{'buyers' if fl > 0 else 'sellers'} {50 + abs(fl) * 50:.0f}%" if abs(fl) > 0.05 else "buyers/sellers even"
    l1 = f"Chart (12 min): {a['spark']}  {a['ch5'] * 100:+.2f}% in 5 min, {a['volx']:.1f}x normal volatility"
    l2 = (f"Trend: 4h {'up' if a.get('tr_pct', 0) > 0 else 'down'} ({a.get('tr_pct', 0) * 100:+.2f}% vs avg), "
          f"1h {a.get('m60', 0) * 100:+.2f}%, {fs}, RSI {a.get('rsi', 50):.0f}, {a.get('vw_pct', 0) * 100:+.2f}% vs VWAP")
    fc = (f"10-min forecast {'UP' if a['fc_p'] >= 0.5 else 'DOWN'} {max(a['fc_p'], 1 - a['fc_p']):.0%}"
          + ("" if a.get("fc_ok") else " (low confidence)")) if "fc_p" in a else "no 10-min forecast"
    l3 = f"Spike score {a['score']:.0f}/100 ({a['label']}), {fc}, {SESS_NOTE.get(a.get('sess'), '')}"
    return "\n".join((l1, l2, l3))


def board_line(mkt, a, st):
    """Two plain lines per market: what it's doing now, then what to do."""
    op = (st.get("lpos") or {}).get(mkt)
    l1 = (f"{COLOR[mkt][0]} {NAME[mkt]} {money(mkt, a['px'])}  {a['ch5'] * 100:+.2f}% in 5 min  {a['spark']}  {a['label']}"
          + (f" ({a['score']:.0f}/100)" if a["score"] >= 45 else "") + (f"  [{call_time(op)} open]" if op else ""))
    out = l1 + "\n    " + action_line(mkt, a)
    if a["score"] >= 45 or ("start" in a and max(a["p_up"], 1 - a["p_up"]) >= 0.75) or (a.get("fc_ok") and max(a.get("fc_p", .5), 1 - a.get("fc_p", .5)) >= 0.6):
        out += "\n    " + analysis_block(mkt, a).split("\n")[1]  # trend line for the markets that matter right now
    return out


def proj_line(mkt, a):
    """Projected prices in 5/10 min + sharp-move risk vs normal."""
    if "px10" not in a: return ""
    out = f"In 5 min ~{money(mkt, a['px5'])} ({a['m5'] * 100:+.2f}%), in 10 min ~{money(mkt, a['px10'])} ({a['m10'] * 100:+.2f}%)"
    if a.get("big_ok"):
        ru, rd = a["big_up"] / (a["base_up"] + 1e-9), a["big_dn"] / (a["base_dn"] + 1e-9)
        if max(ru, rd) >= 2:
            up = ru > rd
            out += (f". Sharp {'SPIKE' if up else 'DROP'} risk next 10 min: {(a['big_up'] if up else a['big_dn']):.0%} "
                    f"(normally {(a['base_up'] if up else a['base_dn']):.0%})")
    if "start" in a:
        T = a["T"]; pend = a["px"] * float(np.exp((a["m10"] if T > 7 else a["m5"]) * min(T, 10) / (10 if T > 7 else 5)))
        out += f". Projected at the close: ~{money(mkt, pend)}, {'ABOVE' if pend >= a['start'] else 'BELOW'} the start {money(mkt, a['start'])}"
    if a.get("pj_live") is not None: out += f" (projections right {a['pj_live']:.0%} live)"
    return out + ("" if a.get("p_ok") else " (low-confidence projection)")


def action_line(mkt, a):
    """Next-10-minute outlook + what to do with the current 15-min contract."""
    parts = []
    if (pl := proj_line(mkt, a)): parts.append(pl)
    if "fc_p" in a:
        pu = a["fc_p"]; up = pu >= 0.5; conf = max(pu, 1 - pu)
        if conf >= 0.6:
            parts.append(f"Next 10 min: likely {'UP' if up else 'DOWN'} ({conf:.0%}) toward {money(mkt, a['px'] + (a['fc_move'] if up else -a['fc_move']))}"
                         + ("" if a.get("fc_ok") else ", low confidence"))
        else:
            parts.append(f"Next 10 min: no clear direction, range about {money(mkt, a['fc_move'])}")
    if "start" in a:
        T = a["T"]
        if "fc_p" in a and max(a["fc_p"], 1 - a["fc_p"]) >= 0.6 and a.get("fc_ok") and T >= 4:
            fc_up = a["fc_p"] >= 0.5; target = a["px"] + (a["fc_move"] if fc_up else -a["fc_move"])
            want_up = target >= a["start"]; cost = a["ya"] if want_up else a["na"]
            if want_up != fc_up:  # forecast move won't cross the start → the current leader stays favored
                parts.append(f"{'bounce' if fc_up else 'dip'} likely but probably not past the start {money(mkt, a['start'])}, "
                             f"{'DOWN' if not want_up else 'UP'} still favored")
                return ". ".join(x[0].upper() + x[1:] for x in parts) + "."
            parts.append(f"BUY {'UP' if want_up else 'DOWN'}, ends {'above' if want_up else 'below'} {money(mkt, a['start'])}" if cost < 0.8
                         else f"{'UP' if want_up else 'DOWN'} is already priced in, skip")
        else:
            wp = a.get("wm_p"); lead_up = (wp if wp is not None else a["p_up"]) >= 0.5
            lead = max(wp, 1 - wp) if wp is not None else 0; mk = a["ya"] if lead_up else a["na"]
            if lead >= 0.9 and a.get("wm_ok"):
                parts.append(f"NEAR LOCK (our analysis {lead:.0%}, tested {a['wm_acc']:.0%}): BUY {'UP' if lead_up else 'DOWN'}, "
                             f"ends {'above' if lead_up else 'below'} {money(mkt, a['start'])} in {T:.0f} min. Kalshi prices {mk:.0%}")
            elif lead >= 0.75:
                parts.append(f"HIGH CONFIDENCE (our analysis {lead:.0%}): {'UP' if lead_up else 'DOWN'}, {T:.0f} min left. Kalshi prices {mk:.0%}")
            elif T < 4: parts.append(f"window ends in {T:.0f} min, wait for the next one")
            else: parts.append("wait")
    return ". ".join(x[0].upper() + x[1:] for x in parts if x) + "."


def live_ready(st, mkt):
    """Calls need ≥20 min of real-time 1-min data so short-term features are current (day or night)."""
    return st.get("live_min", {}).get(mkt, 0) >= 20


def fc_conflict(st, mkt, up):
    """True if a validated 10-min forecast strongly points the other way."""
    a = (st.get("ana") or {}).get(mkt) or {}
    return bool(a.get("fc_ok") and "fc_p" in a and max(a["fc_p"], 1 - a["fc_p"]) >= 0.6 and (a["fc_p"] >= 0.5) != up)


def lock_call(st, mkt, a, lv, cal):
    """NEAR LOCK from our own analysis: window model ≥90% AND proven ≥90% on unseen data, ideally 5-10 min out,
    and Kalshi hasn't fully priced it (so it's worth buying)."""
    if "wm_p" not in a or not a.get("wm_ok") or busy(st, mkt) or not 4 <= a["T"] <= 11 or not live_ready(st, mkt): return False
    up = a["wm_p"] >= 0.5; conf = blend_prob(st, mkt, "lock", max(a["wm_p"], 1 - a["wm_p"]))
    if conf < max(0.90, need_prob(st, mkt, "lock")): return False
    c = k15(mkt)
    if not c or st.setdefault("lockwin", {}).get(mkt) == c["ticker"]: return False
    if event_window(mkt, dt.datetime.now(ET), a["T"]) or regime_extra(st, mkt): return False  # jumps break locks
    cost = c["ya"] if up else c["na"]
    if not 0.70 <= cost < 0.93 or conf - cost - kfee(cost) < 0.03: return False  # Kalshi must lean our way; need some edge
    if fc_conflict(st, mkt, up) or not agrees(st, mkt, up): return False  # forecast + last 5 min must agree
    if conf - cost > 0.25: return False  # huge disagreement with Kalshi = our data is probably off: skip
    st["lockwin"][mkt] = c["ticker"]
    why = (f"our analysis says {conf:.0%} ({'UP' if up else 'DOWN'}); its 90%+ calls were right {a['wm_acc']:.0%} of "
           f"{a['wm_n']:,} times on unseen days; Kalshi only prices {cost:.0%}; " + ctx_short(dict(trend=1 if a.get('tr_pct', 0) > 0 else -1, flow=a.get('flow', 0)), up))
    open_call(st, mkt, "lock", "YES" if up else "NO", c, lv, a["px"], odds_line(conf, cost), why, True, prob=conf)
    return True


def apply_proj_bias(st, mkt, a):
    """Correct the projection by its live average error once there are 30+ scored projections."""
    E = (st.get("pj_err") or {}).get(mkt)
    if not E or E["n"] < 30 or "px10" not in a: return
    a["m10"] += E["bias"]; a["m5"] += E["bias"] / 2
    a["px10"] = a["px"] * float(np.exp(a["m10"])); a["px5"] = a["px"] * float(np.exp(a["m5"]))
    a["pj_live"] = E["hit"] / E["n"]


def track_projection(st, mkt, a):
    """Save each minute's 10-min projection; 10 min later score it vs reality (direction hit + % error)."""
    if "px10" not in a: return
    now = pd.Timestamp.now(tz="UTC").floor("min"); H = st.setdefault("pj_hist", {}).setdefault(mkt, [])
    if not H or H[-1][0] != str(now): H.append([str(now), a["px"], a["px10"]])
    E = st.setdefault("pj_err", {}).setdefault(mkt, {"n": 0, "hit": 0, "bias": 0.0})
    keep = []
    for t, p0, pp in H:
        if pd.Timestamp(t) <= now - pd.Timedelta(minutes=10):
            real = (a["px"] / p0 - 1); pred = (pp / p0 - 1)
            if abs(pred) > 1e-5:
                E["n"] += 1; E["hit"] += int((real > 0) == (pred > 0))
                E["bias"] = round(E["bias"] + ((real - pred) - E["bias"]) / min(E["n"], 200), 7)  # running mean of error
        else: keep.append([t, p0, pp])
    st["pj_hist"][mkt] = keep[-15:]


def boom_signal(a):
    """Same entry test as the backtest, on live numbers. Returns direction (+1/-1) or 0."""
    if "m10" not in a or not a.get("s1"): return 0
    r10 = a["m10"] / (a["s1"] * np.sqrt(10)); sc = a["score"] / 100 * (a["dir"] or 0); d = 1 if r10 > 0 else -1
    ok = (abs(r10) >= BOOM["proj"] and np.sign(sc) == d and abs(sc) >= BOOM["score"] and np.sign(a.get("z3", 0)) == d
          and np.sign(a.get("tr_pct", 0)) == d)
    return d if ok else 0


def boom_call(st, mkt, a, lv, cal):
    """BOOMING: buy part now, DOUBLE DOWN on confirmation, CASH OUT when the spike fades. Only where it backtested well."""
    bt = (cal or {}).get("boom") or {}
    d = boom_signal(a)
    if not d or not bt.get("ok") or "start" not in a or not 6 <= a["T"] <= 12 or busy(st, mkt) or not live_ready(st, mkt): return False
    up = d > 0; c = k15(mkt)
    if not c or event_window(mkt, dt.datetime.now(ET), a["T"]) or fc_conflict(st, mkt, up): return False
    cost = c["ya"] if up else c["na"]; wp = a.get("wm_p"); p = blend_prob(st, mkt, "boom", (wp if up else 1 - wp) if wp is not None else 0.5)
    if not 0 < cost < 0.75 or p < need_prob(st, mkt, "boom"): return False
    dz0 = mkt_dz(c)[0]; add_px = level_for(c["k"], _phi(dz0 + 0.5 * d) if up else 1 - _phi(dz0 + 0.5 * d), up, max(a["T"] - 2, 1), a["s1"])
    why = (f"booming: projected {a['m10'] * 100:+.2f}% in 10 min, spike score {a['score']:.0f}/100 and building, momentum and trend aligned. "
           f"Backtest: {bt['test_win']:.0%} of these trades made money, {bt['test_roi']:+.0%} return on unseen days")
    open_call(st, mkt, "boom", "YES" if up else "NO", c, lv, a["px"], odds_line(p, cost), why, True, prob=p)
    pos = st["lpos"][mkt]; pos.update(dz0=dz0, dir=d, added=False, peak=a["score"], costs=[cost])
    notify(f"{NAME[mkt]}: BOOMING PLAN", f"1) Buy {'UP' if up else 'DOWN'} with HALF your stake now."
           + (f"\n2) DOUBLE DOWN (add the other half) only if {NAME[mkt].title()} {'reaches' if up else 'drops to'} about "
              f"{money(mkt, add_px)} with 3+ min left. Never add if it goes against you." if add_px else "")
           + "\n3) CASH OUT when you get the alert (spike fading, bet near max, or 1 min left).", "high", mkt)
    return True


def manage_boom(mkt, pos, st, c, bid, left):
    """Boom trades: DOUBLE DOWN on confirmation, CASH OUT on exhaustion. Returns True if it handled the tick."""
    k = pos["k"]; d = pos.get("dir", 1); a = (st.get("ana") or {}).get(mkt) or {}
    dzm = mkt_dz(c)[0]; ask = c["ya"] if k["side"] == "YES" else c["na"]
    sc = (a.get("score", 0) * (a.get("dir") or 0)) * d; pos["peak"] = max(pos.get("peak", 0), sc)
    if not pos.get("added") and (dzm - pos["dz0"]) * d >= BOOM["add_dz"] and 0 < ask < BOOM["add_max"] and left >= 3:
        pos["added"] = True; pos["costs"].append(ask)
        gain = (bid - pos["costs"][0]) / pos["costs"][0]
        follow_msg(mkt, pos, "", f"DOUBLE DOWN NOW (booming confirmed, bet up {gain:+.0%})",
                   " Add the other half now. Cash-out alert will follow.")
        return True
    if (pos["peak"] >= BOOM["peak"] * 100 and sc < BOOM["exit_score"] * 100) or bid >= BOOM["cash"] or left <= 1.25:
        why = "spike fading" if bid < BOOM["cash"] and left > 1.25 else "bet near max" if bid >= BOOM["cash"] else "1 min left"
        tot = sum(pos["costs"]); pnl = (len(pos["costs"]) * bid - tot) / tot
        follow_msg(mkt, pos, "", f"CASH OUT NOW ({why}, total {pnl:+.0%})", " Scored at the close on the direction call.")
        pos["took_profit"] = True; pos["held"] = True
        return True
    return False


def premove_alert(st, mkt, a, lv, cal, cool):
    """Sharp move LIKELY in the next 10 min (≥3× normal chance, model validated): a BUY call if everything agrees,
    otherwise a heads-up."""
    if not a.get("big_ok") or "start" not in a or not live_ready(st, mkt): return False
    ru, rd = a["big_up"] / (a["base_up"] + 1e-9), a["big_dn"] / (a["base_dn"] + 1e-9)
    up = ru > rd; r = max(ru, rd); pbig = a["big_up"] if up else a["big_dn"]
    if r < 3 or pbig < 0.2 or time.time() - cool.get((mkt, "pre"), 0) < 900: return False
    cool[(mkt, "pre")] = time.time(); c = k15(mkt)
    wp = a.get("wm_p"); pw = (wp if up else 1 - wp) if wp is not None else None
    detail = (f"Projected: ~{money(mkt, a['px5'])} in 5 min, ~{money(mkt, a['px10'])} in 10 min. "
              f"Chance of a sharp {'spike' if up else 'drop'}: {pbig:.0%} (normally {(a['base_up'] if up else a['base_dn']):.0%}).")
    if (c and pw is not None and pw >= need_prob(st, mkt, "pre") and 4 <= a["T"] <= 12 and not busy(st, mkt)
            and not fc_conflict(st, mkt, up) and 0 < (c["ya"] if up else c["na"]) < 0.85):
        cost = c["ya"] if up else c["na"]
        open_call(st, mkt, "pre", "YES" if up else "NO", c, lv, a["px"], odds_line(pw, cost),
                  f"sharp {'spike' if up else 'drop'} {r:.1f}x more likely than normal in the next 10 min; " + detail, True, prob=pw)
        return True
    notify(f"{NAME[mkt]}: SHARP {'SPIKE' if up else 'DROP'} LIKELY next 10 min ({pbig:.0%})", detail +
           " Not a call yet: the other checks don't all agree.", "high", mkt)
    return False


def spike_alert(st, mkt, a, lv, cal, cool):
    """🔥 Spike starting: a ✅ call where the spike score backtested profitable, otherwise a 🧪 heads-up."""
    if a["score"] < 70 or not a["dir"] or "start" not in a or busy(st, mkt) or not live_ready(st, mkt): return False
    if time.time() - cool.get((mkt, "spk"), 0) < 900: return False
    cool[(mkt, "spk")] = time.time(); up = a["dir"] > 0; c = k15(mkt)
    side = "YES" if up else "NO"; cost = (a["ya"] if up else a["na"]); sp = (cal or {}).get("spike") or {}
    move = f"{a['ch5'] * 100:+.2f}% in 5 min ({abs(a['z3']):.1f}x a normal move)" + (f", broke the 30-min {'high' if up else 'low'} "
           f"{money(mkt, a['hi30'] if up else a['lo30'])}" if (up and a['px'] > a['hi30']) or (not up and a['px'] < a['lo30']) else "")
    p = min(0.95, (a["p_up"] if up else 1 - a["p_up"]) + max(0.0, sp.get("test_roi", 0)) * cost)
    p = blend_prob(st, mkt, "spike", p)
    if c and sp.get("ok") and 4 <= a["T"] <= 12 and 0 < cost < 0.85 and p >= need_prob(st, mkt, "spike") and p - cost <= 0.25 and not fc_conflict(st, mkt, up):
        open_call(st, mkt, "spike", side, c, lv, a["px"], odds_line(p, cost), f"spike starting, {move}", True, prob=p)
        return True
    notify(f"{NAME[mkt]} SPIKE {'UP' if up else 'DOWN'} starting now",
           f"{money(mkt, a['px'])}, {move}. {a['spark']}\n"
           f"Typical range for the next {a['T']:.0f} min: about {money(mkt, a['rng'])}.\n"
           + (f"Do not chase: on {NAME[mkt]}, buying after a spike starts has lost money in testing ({sp.get('test_roi', 0):+.0%})."
              if sp.get("n") else f"Untested: BUY {'UP' if up else 'DOWN'} rides it ({a['T']:.0f} min left)."), "high", mkt)
    return False


def fast_entry(mkt, d1, fp, st, cool):
    """1-min momentum signal → BUY on the 15-min contract in that direction."""
    if busy(st, mkt) or not fp.get("test"): return False  # only validated fast setups
    L, S = signals(d1, fp); bar = str(d1.index[-1])
    if not (L[-1] or S[-1]) or st.setdefault("flast", {}).get(mkt) == bar: return False
    st["flast"][mkt] = bar
    up, px = bool(L[-1]), d1.Close.iloc[-1]; lv = kconv(mkt, px); c = k15(mkt)
    if not c or st.get("lswin", {}).get(mkt) == c["ticker"]: return False
    left = (c["close"] - pd.Timestamp.now(tz="UTC")).total_seconds() / 60
    if left < 4: return False
    side = "YES" if up else "NO"; cost = c["ya"] if up else c["na"]
    if not 0 < cost < 0.9 or fc_conflict(st, mkt, up) or not agrees(st, mkt, up): return False
    cx = live_ctx(d1); cx["px"] = px
    fu = fair_up(px * lv.r, c["k"], left, cx["sig"]); p = (fu if up else 1 - fu) if fu is not None else 0.5
    if p < MIN_PROB: return False
    t = fp.get("test") or {}
    why = "momentum turning, " + ctx_short(cx, up)
    open_call(st, mkt, "fast", side, c, lv, px, odds_line(p, cost, "Odds now") +
              (f"\nPast: {t['win']:.0%} of these moves paid off" if t else ""), why, bool(t))
    cool[(mkt, "spike")] = time.time()
    return True


def k15_call(mkt, m, px, st, lv, cal, night=False):
    """🎯 longshot (cheap bounce side) or 💪 edge pick (favored side), from calibrated history + context."""
    if busy(st, mkt) or not cal or not cal.get("stable") or len(m) < 300: return False
    if not live_ready(st, mkt): return False
    c = k15(mkt)
    if not c: return False
    T = (c["close"] - pd.Timestamp.now(tz="UTC")).total_seconds() / 60
    if not 4 <= T <= 12 or st.setdefault("lswin", {}).get(mkt) == c["ticker"]: return False
    if event_window(mkt, dt.datetime.now(ET), T): return False
    cx = live_ctx(m); cx["px"] = px
    if night and _SIG.get(mkt): cx["sig"] = _SIG[mkt]  # σ from clean futures bars, not the Kalshi/Yahoo join
    z = mkt_dz(c)[0]  # distance from the start as Kalshi sees it (true settlement price)
    if abs(z) < 0.5: return False
    bdir = -1 if z > 0 else 1; cl = m.Close
    turning = (px > cl.iloc[-1] and cx["rsi"] < 45) if bdir > 0 else (px < cl.iloc[-1] and cx["rsi"] > 55)
    sname = session(dt.datetime.now(ET))
    cell = (cal.get("stable") or {}).get(f"{sname}|{ls_bucket(abs(z))}|{'T+' if cx['trend'] == bdir else 'T-'}|{'turn' if turning else 'run'}")
    if not cell: return False
    kind = "ls" if turning else "fav"
    if kind == "ls" and not LONGSHOTS: return False
    if kind == "fav" and T > 10: return False  # first minutes of a window are noise
    up = (bdir > 0) if kind == "ls" else (bdir < 0); side = "YES" if up else "NO"
    cost = c["ya"] if up else c["na"]; p = cell[1] if kind == "ls" else 1 - cell[1]
    tested = cal.get(f"all_{kind}_ok", cal.get(f"night_{kind}_ok"))
    a_ = (st.get("ana") or {}).get(mkt) or {}
    if a_.get("score", 0) >= 70 and a_.get("dir") and (a_["dir"] > 0) != up: return False  # never fade a live spike
    if fc_conflict(st, mkt, up): return False                                                # never fight the forecast
    if kind == "fav" and not tested: return False                       # edge picks only where the edge held on unseen data
    if kind == "ls" and mkt not in MARKETS and mkt not in METALS: return False  # untested longshots only on commodities
    xe = regime_extra(st, mkt) + (0.02 if st.get("thin", {}).get(mkt) else 0)
    if kind == "ls" and (xe or not (0 < cost <= LS_MAX_COST and p - cost - kfee(cost) >= LS_MIN_EDGE)): return False
    if kind == "fav" and not (0 < cost < 0.92 and p - cost - kfee(cost) >= FAV_MIN_EDGE + xe): return False
    p = blend_prob(st, mkt, kind, p)
    if kind == "fav" and (p < need_prob(st, mkt, kind) or not agrees(st, mkt, up)): return False
    if p - cost > 0.25: return False  # suspect data: don't bet on a huge disagreement with Kalshi
    why = (("snap-back setup" if kind == "ls" else "move still running") + f", {p:.0%} win rate in history, " + ctx_short(cx, up)
           + (", thin hours" if st.get("thin", {}).get(mkt) else ""))
    open_call(st, mkt, kind, side, c, lv, px, odds_line(p, cost), why, tested, prob=p)
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
    if not (0 < cost < 0.9 and ih["hit"] - cost - kfee(cost) >= 0.02) or blend_prob(st, mkt, "ihm", ih["hit"]) < need_prob(st, mkt, "ihm"): return False
    st["ihm_day"][mkt] = str(now.date()); cx = live_ctx(m); cx["px"] = px
    why = f"end-of-day pattern, {ih['hit']:.0%} win rate, " + ctx_short(cx, up)
    open_call(st, mkt, "ihm", side, c, lv, px, odds_line(ih["hit"], cost), why, True, prob=ih["hit"])
    st["ihm_day"][mkt] = str(now.date())
    return True


def drift_call(mkt, m, px, st, lv, cal):
    """Early in a 15-min window, price still at the start: bet the session's validated up/down tendency."""
    from math import log, sqrt
    now = dt.datetime.now(ET); d = ((cal or {}).get("drift") or {}).get(session(now))
    if not d or not d.get("ok") or busy(st, mkt) or len(m) < 120 or not live_ready(st, mkt): return False
    c = k15(mkt)
    if not c or st.setdefault("lswin", {}).get(mkt) == c["ticker"]: return False
    T = (c["close"] - pd.Timestamp.now(tz="UTC")).total_seconds() / 60
    if not 10 <= T <= 14 or event_window(mkt, now, T): return False
    sig = float(np.log(m.Close).diff().tail(390).std())
    if not sig or abs(log(px * lv.r / c["k"])) / (sig * sqrt(T)) > 0.3: return False
    up = d["dir"] == "UP"; side = "YES" if up else "NO"; cost = c["ya"] if up else c["na"]
    if fc_conflict(st, mkt, up) or blend_prob(st, mkt, "drift", d["p"]) < need_prob(st, mkt, "drift") or d["p"] - cost > 0.25: return False
    if not (0 < cost < 0.8 and d["p"] - cost - kfee(cost) >= 0.02 + regime_extra(st, mkt)): return False
    cx = live_ctx(m); cx["px"] = px
    why = f"{SH_SESS[session(now)]} session tends {d['dir'].lower()}, {d['p']:.0%} win rate, " + ctx_short(cx, up)
    open_call(st, mkt, "drift", side, c, lv, px, odds_line(d["p"], cost), why, True, prob=d["p"])
    return True


def manage_ls(mkt, px, st, lv):
    """Every tick, using the Kalshi contract's own price: SELL (profit) / SELL (wrong → flip) / HOLD / WON-LOST."""
    pos = st.get("lpos", {}).get(mkt)
    if not pos: return False
    k = pos["k"]; c = k15(mkt); left = (pd.Timestamp(k["close"]) - pd.Timestamp.now(tz="UTC")).total_seconds() / 60
    cost = k["cost"] * 100
    if not c or c["ticker"] != k["ticker"]:  # window over → final result
        _, won = contract_status(k)
        if won is None: return False
        if pos.get("took_profit"):
            follow_msg(mkt, pos, "", f"RESULT: prediction {'RIGHT' if won else 'WRONG'} at the close (profit was taken earlier)")
        else:
            follow_msg(mkt, pos, "", f"RESULT: RIGHT, WON (+{(100 - cost) / cost:.0%} on stake)" if won else "RESULT: WRONG, LOST (stake gone)")
        log_call(mkt, pos, won); learn_update(st)
        del st["lpos"][mkt]; return True
    if pos.get("held"): return False
    bid = c["yb"] if k["side"] == "YES" else c["nb"]; gain = bid * 100 - cost
    if pos.get("kind") == "boom": return manage_boom(mkt, pos, st, c, bid, left)
    if bid >= pos.get("tp", 0.9):
        follow_msg(mkt, pos, "", f"SELL HIGH NOW (bet up {gain / cost:+.0%})",
                   " Scored at the close on whether the prediction was right.")
        pos["took_profit"] = True; pos["held"] = True; return True
    if bid <= 0.25 and left >= 3 and not pos.get("behind"):  # info only: binary bets are best held to the end
        pos["behind"] = True
        follow_msg(mkt, pos, "", f"BEHIND (worth {bid * 100:.0f}% now)",
                   f" It can still come back with {left:.0f} min left. Holding is usually best; sell only if you want out.")
        return True
    if left < 1.25:
        if bid >= 0.5:
            follow_msg(mkt, pos, "", "HOLD TO THE END, winning, pays in full at the close"); pos["held"] = True; return True
        follow_msg(mkt, pos, "", f"LOSING with {left:.0f} min left: likely lost")
        pos["held"] = True; return True
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


def short_reason(r):
    """'Very quiet: last 30 min…' → 'very quiet'; keeps the key number for 'Already decided'."""
    if r.startswith("Already decided"): return "already decided (" + r.split("costs ")[1].split("¢")[0] + "¢)"
    if r.startswith("Coin flip"): return "50/50 + fee"
    return r.split(": ")[0].replace("Trend not in favor", "no trend").replace("(", "").replace(")", "").lower()


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
    body = "\n".join(f"{COLOR[k][0]} {NAME[k]}: skip ({', '.join(short_reason(w) for w in why)})" for k, why in skips)
    if play: body += "\nIn play: " + ", ".join(NAME[k] for k, _ in play)
    notify(f"Skip list for {label}", body, "default")


def yf_hist(sym, **kw):
    """yfinance with retries (its local cache can lock under parallel use)."""
    import yfinance as yf
    for i in range(4):
        try: return yf.Ticker(sym).history(auto_adjust=False, **kw)
        except Exception:
            if i == 3: raise
            time.sleep(0.5 + i)


def night_bars(mkt):
    """1-min bars (context) from Yahoo: futures ~10 min delayed; crypto/FX near real-time."""
    df = yf_hist(ALL[mkt][0], period="2d", interval="1m")
    df = df[["Open", "High", "Low", "Close", "Volume"]].dropna()
    df.index = df.index.tz_convert("UTC"); return df


PYSYM = {"WTI": "Commodities.Index.PYTHOIL/USD", "BRENT": "Commodities.Index.BRENT/USD", "NATGAS": "Commodities.Index.NATGAS/USD",
         "GOLD": "Metal.Index.GOLD/USD", "SILVER": "Metal.Index.SILVER/USD", "COPPER": "Commodities.Index.COPPER/USD",
         "PLATINUM": "Metal.XPT/USD", "PALLADIUM": "Metal.XPD/USD"}
_PYID = {}


def pyth_price(mkt):
    """Kalshi's settlement source, live. Needs PYTH_API_KEY (Pyth now requires a key)."""
    key = os.getenv("PYTH_API_KEY")
    if not key: return None
    try:
        if not _PYID:
            for at in ("commodities", "metal"):
                for f in requests.get("https://hermes.pyth.network/v2/price_feeds", params={"asset_type": at}, timeout=15).json():
                    _PYID[f["attributes"]["symbol"]] = f["id"]
        r = requests.get("https://hermes.pyth.network/v2/updates/price/latest", headers={"Authorization": f"Bearer {key}"},
                         params={"ids[]": _PYID[PYSYM[mkt]], "parsed": "true"}, timeout=10).json()
        p = r["parsed"][0]["price"]; return int(p["price"]) * 10 ** p["expo"]
    except Exception as e:
        print("pyth", mkt, str(e)[:60]); return None


def kraken_gold():
    """PAXG (1 token = 1 oz gold) last trade from Kraken's free public API: live 24/7 gold proxy."""
    try:
        r = requests.get("https://api.kraken.com/0/public/Ticker", params={"pair": "PAXGUSD"}, timeout=10).json()["result"]
        return float(next(iter(r.values()))["c"][0])
    except Exception: return None


def night_price(mkt, y):
    """Live price: Pyth (if key) → Kalshi strike book → backed out of the 15-min YES price → Kraken PAXG (gold)."""
    from math import exp, sqrt
    from statistics import NormalDist
    if (p := pyth_price(mkt)) is not None: return p
    if mkt in COINBASE:  # free real-time crypto trades
        try: return float(requests.get(f"https://api.exchange.coinbase.com/products/{COINBASE[mkt]}/ticker", timeout=8).json()["price"])
        except Exception: pass
    b = kalshi_book(mkt) if KSERIES.get(mkt) else None
    if b: return b["px"]
    c = k15(mkt)
    if not c or len(y) < 60: return kraken_gold() if mkt == "GOLD" else None
    mid = (c["ya"] + c["yb"]) / 2; T = (c["close"] - pd.Timestamp.now(tz="UTC")).total_seconds() / 60
    if not 0.05 < mid < 0.95 or T <= 0:
        return kraken_gold() if mkt == "GOLD" else (float(y.Close.iloc[-1]) if mkt in CRYPTO or mkt in FX else None)
    sig = float(np.log(y.Close).diff().tail(390).std())
    return c["k"] * exp(NormalDist().inv_cdf(mid) * sig * sqrt(T))


def ident(mkt):
    f = lambda x: money(mkt, x); f.r = 1.0; return f


def market_mode(now):
    """'day' = US stock hours (fund prices via Alpaca for oil & gas); otherwise 'night' (Kalshi-price engine).
    Each market is then switched on/off by whether Kalshi has a live 15-min contract for it."""
    return "day" if now.weekday() < 5 and LIVE_OPEN <= now.time() <= LIVE_CLOSE else "night"


def night_tick(st, params, cool, nh, yc, only=None):
    """Overnight: Kalshi real-time price + delayed futures context → longshots / edge picks / skip board / watch board."""
    now = dt.datetime.now(ET); minute = now.replace(second=0, microsecond=0); changed = False; boards = {}
    mkts = list(only or ALL); openm = []
    from concurrent.futures import ThreadPoolExecutor
    def bars_safe(k):
        try: return night_bars(k)
        except Exception as e: print("night bars", k, e); return None
    with ThreadPoolExecutor(12) as ex:  # fetch everything in parallel, then decide sequentially
        list(ex.map(k15, mkts))
        need = [k for k in mkts if _KC.get(f"15|{k}") and yc.get(k, (None,))[0] != minute]
        for k, df in zip(need, ex.map(bars_safe, need)):
            if df is not None and len(df): yc[k] = (minute, df)
    for mkt in mkts:
      try:
        c0 = k15(mkt)
        if not c0 or not (c0["ya"] > 0 or c0["na"] > 0):  # no live 15-min contract → this market is closed now
            changed |= manage_ls(mkt, 0.0, st, ident(mkt)) if mkt in st.get("lpos", {}) and not c0 else False
            continue
        openm.append(mkt)
        if mkt not in yc: continue
        y = yc[mkt][1]; kp = night_price(mkt, y)
        if kp is None or len(y) < 300: continue
        if mkt not in nh and (st.get("nh") or {}).get(mkt):  # restore live history saved by the previous run
            nh[mkt] = [(pd.Timestamp(t), float(p)) for t, p in st["nh"][mkt]]
        h = nh.setdefault(mkt, [])
        if len(h) >= 3:  # glitch filter: ignore a reading that jumps >6 normal 1-min moves from the recent median
            med = float(np.median([p for _, p in h[-3:]])); s1 = float(np.log(y.Close).diff().tail(390).std() or 1e-4)
            if abs(np.log(kp / med)) > 6 * s1: print("glitch", mkt, kp, "vs", med); kp = med
        h.append((pd.Timestamp.now(tz="UTC"), kp)); h[:] = [x for x in h if x[0] > pd.Timestamp.now(tz="UTC") - pd.Timedelta(minutes=240)]
        mins = sorted({t.floor("min") for t, _ in h}); st.setdefault("live_min", {})[mkt] = len(mins)
        st.setdefault("nh", {})[mkt] = [[str(t), round(p, 6)] for t, p in h[::max(1, len(h) // 240)][-240:]]
        hb = pd.Series([p for _, p in h], index=[t for t, _ in h]).resample("1min").ohlc().dropna()
        hb = hb.rename(columns=str.title).assign(Volume=0.0)
        ov = hb.Close.reindex(y.index).dropna()  # minutes where both Kalshi and (delayed) Yahoo exist
        if len(ov) >= 3:  # rescale Yahoo to Kalshi's price level so the join has no fake jump
            r = float((ov / y.Close.reindex(ov.index)).median()); y = y.assign(**{k: y[k] * r for k in ("Open", "High", "Low", "Close")})
        elif len(y):
            r = kp / float(y.Close.iloc[-1]); y = y.assign(**{k: y[k] * r for k in ("Open", "High", "Low", "Close")})
        m = pd.concat([y[y.index < hb.index[0]], hb]); m = m[~m.index.duplicated(keep="last")]
        _SIG[mkt] = float(np.log(y.Close).diff().tail(390).std()); lv = ident(mkt)
        changed |= manage_ls(mkt, kp, st, lv)
        cal_ = (params.get("_cal") or {}).get(mkt)
        if now.time() < dt.time(15, 50) or now.time() > dt.time(16, 10):
            changed |= (ihm_call(mkt, m, kp, st, lv, cal_) or drift_call(mkt, m.iloc[:-1], kp, st, lv, cal_)
                        or k15_call(mkt, m.iloc[:-1], kp, st, lv, cal_, night=True))
        regime_update(st, mkt, y); boards[mkt] = (m, kp, lv)  # volatility from one clean source
        try:
            a = analyze(mkt, m, kp, lv, k15(mkt), (cal_ or {}).get("fcast"), (cal_ or {}).get("wmod"), (cal_ or {}).get("proj")); st.setdefault("ana", {})[mkt] = a
            if a: apply_proj_bias(st, mkt, a); track_projection(st, mkt, a)
            if a: changed |= (boom_call(st, mkt, a, lv, cal_) or spike_alert(st, mkt, a, lv, cal_, cool)
                              or premove_alert(st, mkt, a, lv, cal_, cool) or lock_call(st, mkt, a, lv, cal_))
        except Exception as e: print("analyze", mkt, e)
        st.setdefault("thin", {})[mkt] = bool(len(y) and pd.Timestamp.now(tz="UTC") - y.index[-1] > pd.Timedelta(minutes=25))
      except Exception as e:
        print("night", mkt, "error:", e)
    announce_open(st, mkts, openm)
    return changed, boards


def announce_open(st, mkts, openm):
    """One message when markets open/close on Kalshi (their 15-min contracts appear/disappear)."""
    prev = st.setdefault("open", {}); opened, closed = [], []
    for k in mkts:
        now_open = k in openm
        if prev.get(k) is None: prev[k] = now_open; continue  # first sight: just record
        if now_open != prev[k]: (opened if now_open else closed).append(k); prev[k] = now_open
    if opened or closed:
        lines = [f"{COLOR[k][0]} {NAME[k]}: open, watching for calls" for k in opened] + \
                [f"{COLOR[k][0]} {NAME[k]}: closed, paused until it reopens" for k in closed]
        notify("Market hours update", "\n".join(lines), "default")


def night_boards(st, boards, night=True):
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
                body = "\n".join(f"{COLOR[k][0]} {NAME[k]}: skip ({', '.join(short_reason(w) for w in why)})" for k, why in skips)
                if play: body += "\nIn play: " + ", ".join(NAME[k] for k, _ in play)
                notify(f"Skip list for {label}", body, "default")
    if now.minute % 10 == 0 and st.get("nightpulse") != now.strftime("%H:%M"):
        st["nightpulse"] = now.strftime("%H:%M"); lines = []
        for mkt, (m, kp, lv) in boards.items():
            a = (st.get("ana") or {}).get(mkt)
            lines.append(board_line(mkt, a, st) if a else f"{COLOR[mkt][0]} {NAME[mkt]} {money(mkt, kp)}")
        shut = [k for k, v in st.get("open", {}).items() if v is False and k not in boards]
        if shut: lines.append("Closed now: " + ", ".join(NAME[k] for k in shut))
        if lines: notify(f"Market board {now:%-I:%M %p} ({SH_SESS[session(now)]} session)", "\n".join(lines), "low")


def snapshots():
    """Latest trade price per ETF (real-time, one request)."""
    hdr = {"APCA-API-KEY-ID": os.environ["ALPACA_KEY"], "APCA-API-SECRET-KEY": os.environ["ALPACA_SECRET"]}
    r = requests.get("https://data.alpaca.markets/v2/stocks/snapshots", headers=hdr, timeout=10,
                     params={"symbols": ",".join(v[1] for v in MARKETS.values()), "feed": os.getenv("ALPACA_FEED", "iex")})
    r.raise_for_status()
    return {k: (v.get("latestTrade") or {}).get("p") for k, v in r.json().items()}


MODE_TXT = {
    "day": "Day mode: real-time fund prices for oil & gas (Alpaca); metals on Kalshi prices. Fast calls on.",
    "night": "Overnight mode: live prices from Kalshi, context from futures (≈10 min delayed). Fast calls paused; "
             "edge picks, long shots, drift calls and skip boards continue.",
    "closed": "No markets open: no new calls. Open calls still get their results.",
    "night*": "Day data isn't updating (holiday, early close or outage) → switched oil & gas to overnight mode. Rechecking every 5 min."}


def regime_update(st, mkt, m):
    """Volatility regime with hysteresis: HIGH when last 30 min moves >2× normal, back to NORMAL under 1.4×."""
    r = np.log(m.Close).diff().dropna()
    if len(r) < 200: return
    ratio = float(r.tail(30).std() / (r.tail(390).std() + 1e-12)); reg = st.setdefault("regime", {}); cur = reg.get(mkt, "NORMAL")
    new = "HIGH" if cur == "NORMAL" and ratio > 2.0 else "NORMAL" if cur == "HIGH" and ratio < 1.4 else cur
    if new != cur:
        reg[mkt] = new
        notify(f"{NAME[mkt]}: {'high volatility' if new == 'HIGH' else 'volatility back to normal'}",
               (f"Moves are {ratio:.1f}× normal speed. Calls now need +2¢ more edge; long shots paused." if new == "HIGH"
                else f"Volatility settled ({ratio:.1f}× normal). Normal call rules resume."), "default", mkt)


def regime_extra(st, mkt): return 0.02 if st.get("regime", {}).get(mkt) == "HIGH" else 0.0


def settle_only(st):
    """During the break: only report results of calls whose 15-min window has closed."""
    changed = False
    for mkt, pos in list(st.get("lpos", {}).items()):
        try:
            c = k15(mkt)
            if c and c["ticker"] == pos["k"]["ticker"]: continue
            if pd.Timestamp(pos["k"]["close"]) > pd.Timestamp.now(tz="UTC"): continue
            txt, won = contract_status(pos["k"])
            if won is None: continue
            follow_msg(mkt, pos, "", f"RESULT: {'RIGHT' if won else 'WRONG'} at the close"); log_call(mkt, pos, won); learn_update(st)
            del st["lpos"][mkt]; changed = True
        except Exception as e: print("settle", mkt, e)
    return changed


def prune_state(st):
    for k in ("skipped",):
        if len(st.get(k, {})) > 40: st[k] = dict(sorted(st[k].items())[-40:])
    st["sent"] = sorted(set(st.get("sent", [])))[-300:]


def day_fresh(data, now):
    """Is day data (Alpaca fund bars) actually updating? Grace period after the open."""
    if now.time() < dt.time(9, 45) or not data: return True
    last = max(d.index[-1] for d in data.values())
    return (pd.Timestamp.now(tz="UTC") - last) < pd.Timedelta(minutes=20)


def live():
    """Supervisor: picks day / night / break mode every tick, switches safely, never lets one market break the rest."""
    import traceback
    if not ALPACA: sys.exit("live mode needs ALPACA_KEY / ALPACA_SECRET")
    t0, maxmin = time.time(), float(os.getenv("LIVE_MAX_MIN") or 1e9)
    pulse_min, tick = int(os.getenv("PULSE_MIN") or 10), int(os.getenv("TICK_SEC") or 10)
    cool, data, nh, yc = {}, {}, {}, {}
    S = dict(params=load_params(), last_min=None, last_hour=None, last_pulse=None, nt=0, errs=0, saved=time.time(), recheck=0)
    st0 = load_state(); learn_update(st0)
    if not MAIN_ON: st0["pos"] = {}
    for key in ("lpos", "open", "regime", "thin", "lswin"):  # forget markets no longer tracked (e.g. crypto/FX)
        if isinstance(st0.get(key), dict): st0[key] = {k: v for k, v in st0[key].items() if k in ALL}
    json.dump(st0, open(STATE_FILE, "w"), indent=1, default=float)
    print(f"live supervisor: tick {tick}s · markets: {', '.join(ALL)}")

    def day_tick(st, now):
        params = S["params"]
        st.setdefault("sent", []); changed = False
        minute = now.replace(second=0, microsecond=0)
        if minute != S['last_min'] and now.second >= 3:  # new minute: pull closed 1-min bars, run strategies
            S['last_min'] = minute
            since = min((d.index[-1] for d in data.values()), default=None)
            since = (since - pd.Timedelta(minutes=3)) if since is not None else pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=7)
            for sym, df in fetch_1m(since).items():
                data[sym] = pd.concat([data.get(sym), df]).pipe(lambda x: x[~x.index.duplicated(keep="last")]).tail(6000)
            for mkt_, (_, etf_) in MARKETS.items():
                if etf_ in data: _SIG[mkt_] = float(np.log(data[etf_].Close).diff().tail(390).std())
            for e in events(hours=0.25):
                if (k := f"EV15|{e}|{now.date()}") not in st["sent"]:
                    st["sent"].append(k); notify("Report in 15 minutes", e + "\nPrices can jump hard. Avoid new bets until after.", "urgent")
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
                if FAST_ON and len(m1) >= 400 and now.time() < dt.time(15, 50):
                    fp = {**FAST_DEFAULT, **(params.get("_fast") or {}).get(mkt, {})}
                    changed |= fast_entry(mkt, indicators(m1.tail(1500)), fp, st, cool)
        px = snapshots(); S['nt'] += 1  # every tick: live price → spike/dip, trend, stop/target checks
        for mkt, (_, etf) in MARKETS.items():
          try:
            if etf not in data or not px.get(etf): continue
            if not k15(mkt): continue  # Kalshi closed this market's 15-min contracts
            _recent = data[etf].index[data[etf].index > pd.Timestamp.now(tz="UTC") - pd.Timedelta(minutes=60)]
            st.setdefault("live_min", {})[mkt] = len(_recent)
            regime_update(st, mkt, data[etf])
            try:
                _m = data[etf]; _m = _m[_m.index + pd.Timedelta(minutes=1) <= pd.Timestamp.now(tz="UTC")]
                _lv = kconv(mkt, float(px[etf])); _a = analyze(mkt, _m, float(px[etf]) * _lv.r, _lv, k15(mkt), ((params.get("_cal") or {}).get(mkt) or {}).get("fcast"), ((params.get("_cal") or {}).get(mkt) or {}).get("wmod"),
                                ((params.get("_cal") or {}).get(mkt) or {}).get("proj"))
                st.setdefault("ana", {})[mkt] = _a
                if _a: apply_proj_bias(st, mkt, _a); track_projection(st, mkt, _a)
                _c = (params.get("_cal") or {}).get(mkt)
                if _a: changed |= (boom_call(st, mkt, _a, _lv, _c) or spike_alert(st, mkt, _a, _lv, _c, cool)
                                   or premove_alert(st, mkt, _a, _lv, _c, cool) or lock_call(st, mkt, _a, _lv, _c))
            except Exception as e: print("analyze", mkt, e)
            m = data[etf]; m = m[m.index + pd.Timedelta(minutes=1) <= pd.Timestamp.now(tz="UTC")]
            cur = pd.Timestamp.now(tz="UTC").floor("min"); p_ = float(px[etf])
            changed |= manage_fast(mkt, p_, st)
            lv_ = kconv(mkt, p_); changed |= manage_ls(mkt, p_, st, lv_)
            if dt.datetime.now(ET).time() >= dt.time(15, 50): continue  # no new calls into the close
            cal_ = (params.get("_cal") or {}).get(mkt)
            changed |= (ihm_call(mkt, m, p_, st, lv_, cal_) or drift_call(mkt, m, p_, st, lv_, cal_)
                        or k15_call(mkt, m, p_, st, lv_, cal_))
            row = pd.DataFrame({"Open": p_, "High": p_, "Low": p_, "Close": p_, "Volume": m.Volume.iloc[-1]}, index=[cur])
            changed |= bool(fast_checks(mkt, pd.concat([m, row]), st, cool))
          except Exception as e:
            print("day", mkt, "error:", e)
        skip_board(data, st, params)
        try:
            ch2, mb = night_tick(st, params, cool, nh, yc, only=[k for k in ALL if k not in MARKETS]); changed |= ch2; night_boards(st, mb, night=False)
        except Exception as e: print("metals error:", e)
        slot = minute.replace(minute=minute.minute - minute.minute % pulse_min) if pulse_min else None
        if pulse_min and slot != S['last_pulse'] and data:
            if S['last_pulse'] is not None or now.minute % pulse_min == 0: pulse(data, load_state())
            S['last_pulse'] = slot
        return changed

    while (time.time() - t0) / 60 < maxmin:
        now = dt.datetime.now(ET); mode = market_mode(now); shown = mode
        if mode == "day" and not day_fresh(data, now):
            mode, shown = "night", "night*"
            if time.time() - S["recheck"] > 300:  # try Alpaca again every 5 min
                S["recheck"] = time.time()
                try:
                    since = max((d.index[-1] for d in data.values()), default=pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=7))
                    for sym, df in fetch_1m(since - pd.Timedelta(minutes=3)).items():
                        data[sym] = pd.concat([data.get(sym), df]).pipe(lambda x: x[~x.index.duplicated(keep="last")]).tail(6000)
                except Exception as e: print("alpaca recheck:", e)
        try:
            st = load_state()
            if st.get("mode") != shown and not (st.get("mode") == "idle" and shown == "night"):  # announce once
                notify(f"Mode: {'overnight (day data down)' if shown == 'night*' else {'day': 'day', 'night': 'overnight', 'closed': 'closed'}[shown]}", MODE_TXT[shown], "default")
                st["mode"] = shown; yc.clear()  # keep live price history across mode switches
            if mode == "night":
                changed, boards = night_tick(st, S["params"], cool, nh, yc); night_boards(st, boards)
                if not boards:  # every market closed (e.g. weekend): idle, still report results
                    changed |= settle_only(st)
                    if st.get("mode") != "idle":
                        notify("Mode: idle", "No Kalshi commodity 15-min markets are open right now. Waiting for the reopen; "
                               "open calls still get their results.", "default"); st["mode"] = "idle"
                    mode = "closed"
                elif st.get("mode") == "idle": st["mode"] = None
            else: changed = day_tick(st, now)
            try: scorecard(st)
            except Exception as e: print("scorecard", e)
            prune_state(st); json.dump(st, open(STATE_FILE, "w"), indent=1, default=float)
            if changed or time.time() - S["saved"] > 600: persist("bot: live"); S["saved"] = time.time()
            S["errs"] = 0
        except Exception as e:
            S["errs"] += 1; print("tick error:", e); traceback.print_exc()
            if S["errs"] == 30: notify("Data problem", f"Live loop failing for ~5 min ({str(e)[:80]}). Retrying automatically.", "high")
        if now.minute < 3 and now.hour != S["last_hour"]:  # hourly: pull fresh calibration / params
            S["last_hour"] = now.hour
            try:
                if os.getenv("GIT_PERSIST"): os.system("git pull -q --rebase origin main")
                S["params"] = load_params()
            except Exception as e: print("param refresh:", e)
        time.sleep(30 if mode == "closed" else max(1, tick - time.time() % tick))
    print(f"live ended after {S['nt']} price checks"); persist()


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
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(4) as ex: cal = dict(zip(ALL, ex.map(calibrate, ALL)))
    p = load_params(); p["_cal"] = cal; json.dump(p, open(PARAMS_FILE, "w"), indent=1)


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


def discover2():
    allf = []
    for at in ("commodities", "metal"):
        allf += requests.get("https://hermes.pyth.network/v2/price_feeds", params={"asset_type": at}, timeout=20).json()
    pick = {f["attributes"]["symbol"]: f for f in allf}
    f = pick.get("Commodities.Index.PYTHOIL/USD"); print("ATTR", json.dumps(f["attributes"])[:400])
    g = pick.get("Metal.Index.GOLD/USD"); print("ATTR", json.dumps(g["attributes"])[:400]) if g else None
    for fid in (f["id"], "0x" + f["id"]):
        r = requests.get("https://hermes.pyth.network/v2/updates/price/latest", params={"ids[]": fid, "parsed": "true"}, timeout=20)
        print("LATEST", fid[:10], r.status_code, r.text[:300])
    now = int(time.time())
    for sym in ("Commodities.Index.PYTHOIL/USD", "Commodities.PYTHOIL/USD", "PYTHOIL/USD", "Metal.Index.GOLD/USD", "Metal.XAU/USD", "Crypto.BTC/USD"):
        r = requests.get("https://benchmarks.pyth.network/v1/shims/tradingview/history",
                         params={"symbol": sym, "resolution": "1", "from": now - 7200, "to": now}, timeout=30)
        print("HIST", sym, r.status_code, r.text[:160])
    r = requests.get("https://benchmarks.pyth.network/v1/shims/tradingview/symbols", params={"symbol": "Commodities.Index.PYTHOIL/USD"}, timeout=30)
    print("SYMINFO", r.status_code, r.text[:300])
    r = requests.get(f"https://benchmarks.pyth.network/v1/updates/price/{now - 600}", params={"ids": f["id"], "parsed": "true"}, timeout=30)
    print("BENCH_AT", r.status_code, r.text[:300])


def nighttest():
    """One dry overnight pass (no pushes): checks every data pipe for all 8 markets."""
    os.environ["NTFY_TOPIC"] = ""; st, nh, yc = {}, {}, {}
    t0 = time.time(); ch, boards = night_tick(st, load_params(), {}, nh, yc)
    for mkt in ALL:
        c = k15(mkt); b = boards.get(mkt)
        print("NT", mkt, "| live px", b and round(b[1], 4), "| yahoo bars", len(yc[mkt][1]) if mkt in yc else 0,
              "| 15m", c and (c["ticker"], c["k"], c["ya"], c["na"]), "| skip?", b and skip_reasons(mkt, b[0], b[1], b[2])[0][:2])
    print("NT gold kraken", kraken_gold(), "| pass took", round(time.time() - t0, 1), "s")


def kraw():
    """Every Kalshi series with intraday/daily frequency that has OPEN markets right now (any category)."""
    from concurrent.futures import ThreadPoolExecutor
    ser = [x for x in requests.get(f"{KALSHI}/series", timeout=30).json().get("series", [])
           if x.get("frequency") in ("fifteen_min", "hourly", "daily")]
    def cnt(x):
        try:
            ms = requests.get(f"{KALSHI}/markets", params={"series_ticker": x["ticker"], "status": "open", "limit": 200}, timeout=20).json().get("markets", [])
            live = [m for m in ms if float(m.get("yes_ask_dollars") or 0) > 0 or float(m.get("no_ask_dollars") or 0) > 0]
            return (x["ticker"], x.get("title"), x.get("frequency"), x.get("category"), len(ms), len(live),
                    min((m["close_time"] for m in ms), default=None))
        except Exception: return None
    with ThreadPoolExecutor(16) as ex: rows = [r for r in ex.map(cnt, ser) if r and r[5]]
    for r in sorted(rows, key=lambda r: (r[3] or "", r[2], r[0])): print("OPEN", *r, sep=" | ")


def perf():
    """Score every call sent in the last 12h (from the ntfy topic history)."""
    t = os.getenv("NTFY_TOPIC")
    msgs = [json.loads(x) for x in requests.get(f"https://ntfy.sh/{t}/json", params={"poll": 1, "since": "12h"}, timeout=30).text.splitlines() if x.strip()]
    msgs = [m for m in msgs if m.get("event") == "message"]
    buys = [m for m in msgs if re.search(r"BUY (UP|DOWN)|BUY signal|BUY (YES|NO) |· BUY ", m.get("title") or "")]
    outs = [m for m in msgs if re.search(r"TAKE PROFIT|GET OUT|SELL NOW|RESULT|HOLD|LOSING|SELL what|WON|LOST", m.get("title") or "")]
    print("PERF messages", len(msgs), "buys", len(buys), "outcomes", len(outs))
    try:
        log = pd.read_json(CALL_LOG, lines=True)
        print("PERF LOG", len(log), "calls · win rate", f"{log.won.mean():.0%}")
        for k, g in log.groupby("kind"): print("PERF LOG", k, len(g), f"{g.won.mean():.0%}")
        for k, g in log.groupby("mkt"): print("PERF LOG", k, len(g), f"{g.won.mean():.0%}")
    except Exception as e: print("PERF LOG none yet", e)
    from collections import Counter
    cnt = Counter()
    for m in outs:
        ti = m["title"]
        k = ("profit" if "TAKE PROFIT" in ti or "take profit" in ti else "wrong" if "wrong" in ti else "won" if "WON" in ti else
             "lost" if "LOST" in ti else "hold" if "HOLD" in ti else "losing_end" if "LOSING" in ti or "what's left" in ti else "other")
        cnt[k] += 1
    print("PERF outcomes", dict(cnt))
    for m in buys[-40:]: print("PERF BUY", dt.datetime.fromtimestamp(m["time"], ET).strftime("%H:%M"), "|", m["title"][:90], "|", (m.get("message") or "").split("\n")[3 if len((m.get("message") or "").split("\n")) > 3 else 0][:80])
    for m in outs[-60:]: print("PERF OUT", dt.datetime.fromtimestamp(m["time"], ET).strftime("%H:%M"), "|", m["title"][:100])


def tally(since_hour=None):
    """One notification: right vs wrong for this evening (settled calls), by call type and market."""
    since_hour = int(os.getenv("TALLY_FROM") or 18)
    d = pd.read_json(CALL_LOG, lines=True)
    d["c"] = pd.to_datetime(d["close"].fillna(d["t"]), utc=True).dt.tz_convert(ET)
    now = dt.datetime.now(ET); start = (now if now.hour >= since_hour else now - dt.timedelta(days=1)).replace(hour=since_hour, minute=0, second=0, microsecond=0)
    d = d[d.c >= start]
    if not len(d): notify("Evening tally", "No settled calls yet this evening."); return
    r, w = int(d.won.sum()), int((~d.won.astype(bool)).sum())
    lines = [f"Since {start:%-I:%M %p}: {r} right, {w} wrong ({r / (r + w):.0%}). Calls claimed {d.prob.mean():.0%} on average."]
    for k, g in d.groupby("kind"): lines.append(f"{KIND.get(k, k)}: {int(g.won.sum())}-{int((~g.won.astype(bool)).sum())}")
    lines.append("By market: " + ", ".join(f"{NAME.get(k, k)} {int(g.won.sum())}-{int((~g.won.astype(bool)).sum())}" for k, g in d.groupby("mkt")))
    lines.append("Fix applied: predictions now anchored to Kalshi's own 15-min price and re-fit to these results.")
    notify(f"Evening tally: {r} right, {w} wrong", "\n".join(lines), "high")


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
                live=live, tally=tally, perf=perf, kraw=kraw, nighttest=nighttest, livetest=lambda: (os.environ.update(LIVE_MAX_MIN='2', GIT_PERSIST='', STATE_FILE='/tmp/st.json'), live()), audit=audit, calibrate=calibrate_only, discover2=discover2, kalshi=kalshi_discover, kcheck=kcheck, loop=lambda: [(scan(), time.sleep(int(os.getenv("LOOP_SEC", 120)))) for _ in iter(int, 1)])
    cmds.get((sys.argv[1:] or ["scan"])[0], lambda: print(__doc__))()
