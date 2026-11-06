#!/usr/bin/env python3
"""Kalshi COMMODITY scanner: whales, spikes, trends + 15-min UP/DOWN predictions. REPORTS ONLY (never trades, no key).

Markets: WTI, Brent, NatGas, gold, silver, copper, platinum, palladium (Kalshi 15-min up/down + hourly/daily markets).
  🎯 Edge call    model beats Kalshi's 15-min price by 4+ pts after fees on a PROVEN market
  📈 15-min board once per window: every commodity's UP/DOWN odds vs Kalshi + whale flow
  🐋 Whale        big money on any commodity market (sliced orders merged), bullish/bearish, what past whales did next
  ⚡ Spike        fast jump on a commodity market
  ✅/❌ Result     every edge call graded at settlement · 📊 digest every 6h
Data, all combined: (1) the commodity bot's 3-week Kalshi cache, (2) fresh Kalshi pulls of the last 3 weeks + past
months, (3) every window's trades (order flow + big-money flow), (4) whale history this scanner gathered live.
Model: p = σ(logit(Kalshi mid) + w·x), so it learns only what Kalshi's own price misses. Trained on 3 weeks, tested on the
newest 30%, then re-checked on past months it never saw. PROVEN = beats Kalshi on both. Retrains every 6h; live misses x1.5.

Switches: kwhale/switches.json (markets on/off, alert types on/off, pause_all), re-read every 5 min while live.
Commands: build | live | train | report | doctor | testnotify | selftest
"""
import glob, json, math, os, re, subprocess, sys, threading, time
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import numpy as np, pandas as pd, requests

for _k, _v in list(os.environ.items()):  # tolerate secrets pasted with stray spaces/newlines
    if _v != _v.strip(): os.environ[_k] = _v.strip()


def E(k, d): return type(d)(os.getenv(k) or d)


API, WEB = "https://api.elections.kalshi.com/trade-api/v2", "https://kalshi.com/markets"
DIR = E("KW_DIR", "kwhale"); DATA = f"{DIR}/data"   # data/ lives in the Actions cache; model.json + report.md go in git
OLD_CACHE = "data"                                   # commodity bot's 3-week Kalshi cache (read only)
COMMS = ("WTI", "BRENT", "NATGAS", "GOLD", "SILVER", "COPPER", "PLATINUM", "PALLADIUM")
K15 = {c: f"KX{c}15M" for c in COMMS}
SHOW = ("GOLD", "SILVER", "WTI", "BRENT", "COPPER", "NATGAS", "PALLADIUM", "PLATINUM")  # Kalshi's on-screen order (display only; COMMS stays the model's order)
KEYS = {"WTI": ("WTI", "OIL"), "BRENT": ("BRENT",), "NATGAS": ("NATGAS", "NG"), "GOLD": ("GOLD",), "SILVER": ("SILVER",),
        "COPPER": ("COPPER",), "PLATINUM": ("PLATINUM",), "PALLADIUM": ("PALLADIUM",)}
MIN_WHALE = E("KW_MIN_WHALE", 500.0)      # commodity markets are thin: $500+ merged order = whale
ALERT_WHALE = E("KW_ALERT_WHALE", 2000.0)
BIG = 100.0                               # single trade ≥ $100 counts toward big-money flow in 15-min windows
EDGE = E("KW_EDGE", 0.04)                 # model must beat Kalshi's ask by 4 pts after fees
KMAX = 0.70                               # never suggest paying over 70¢ (call it before Kalshi prices it in)
POLL, RPS = E("KW_POLL", 8), E("KW_RPS", 10.0)
WEEKS_D, MONTHS_D, SAMPLE = E("KW_WEEKS_DAYS", 21), E("KW_MONTHS_DAYS", 90), E("KW_MONTHS_SAMPLE", 3)
CLUSTER_GAP, CK = 30, (12, 9, 6, 3)
ET = ZoneInfo("America/New_York")
SESS = ("ASIA", "EU", "US")
KF = ("dmid1", "dmid3", "dmid5", "spread", "kvol", "vcum", "tleft", "ext", "ofi3", "bigc") + tuple(f"s_{s}" for s in SESS) + tuple(f"m_{c}" for c in COMMS)
KCOLS = ["ticker", "close", "strike", "up", "ts", "bid", "ask", "last", "vol", "yf", "nf", "bf"]


# ---------------- utils ----------------
def ts_of(s): return datetime.fromisoformat(str(s).replace("Z", "+00:00")).timestamp()
def fnum(x, d=0.0):
    try: return float(x)
    except (TypeError, ValueError): return d
def sig(z): return 1 / (1 + np.exp(-np.clip(z, -30, 30)))
def logit(p): p = np.clip(np.asarray(p, float), 0.01, 0.99); return np.log(p / (1 - p))
def fee(p): return math.ceil(7 * p * (1 - p) - 1e-9) / 100  # Kalshi taker fee per contract
def fees(a): return np.array([fee(x) for x in np.clip(np.asarray(a, float), 0.01, 0.99)])
def et(t, f="%-I:%M%p"): return datetime.fromtimestamp(t, ET).strftime(f).lower()
def money(x): return f"${x:,.0f}"
def cents(p): return f"{p * 100:.0f}¢"
def slog(v, s=100.0): return np.sign(v) * np.log1p(np.abs(v) / s)
def slug(s): return "-".join(w for w in "".join(c if c.isalnum() else " " for c in s.lower()).split())
def load_json(p, d):
    try: return json.load(open(p))
    except Exception: return d
def save_json(p, o):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True); tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=float); os.replace(tmp, p)
SW_DEFAULT = {"pause_all": False, "markets": {c: True for c in COMMS},
              "alerts": {"board": True, "edge_calls": True, "results": True, "whales": True, "spikes": True, "digest": True, "open_close": True, "low_spikes": True, "pred_results": True, "board_update": True}}
_SW = {"sw": None, "t": 0}


def switches(force=False):
    """kwhale/switches.json: turn markets / alert types on or off, or pause everything. Edit it on GitHub; the live bot
    re-reads it from the remote branch every 5 min (no restart). Data collection and learning never stop."""
    if _SW["sw"] is not None and not force and time.time() - _SW["t"] < 300: return _SW["sw"]
    txt = None
    if os.getenv("GIT_PERSIST"):
        br = os.getenv("GITHUB_REF_NAME", "main")
        r = subprocess.run(f"git fetch -q origin {br} && git show origin/{br}:{DIR}/switches.json", shell=True, capture_output=True, text=True)
        txt = r.stdout if r.returncode == 0 else None
    try: sw = json.loads(txt) if txt else load_json(f"{DIR}/switches.json", {})
    except ValueError: sw = _SW["sw"] or {}; print("switches.json is not valid JSON: keeping previous switches", flush=True)
    out = json.loads(json.dumps(SW_DEFAULT))
    out["pause_all"] = bool(sw.get("pause_all", False))
    for k in ("markets", "alerts"): out[k].update({a: bool(b) for a, b in (sw.get(k) or {}).items() if a in out[k]})
    if _SW["sw"] and out != _SW["sw"]: print("switches changed:", out, flush=True)
    _SW.update(sw=out, t=time.time()); return out


def on(kind, comm=None):
    sw = switches()
    return not sw["pause_all"] and sw["alerts"].get(kind, True) and (comm is None or sw["markets"].get(comm, True))


def comm_of(tk):
    s = str(tk).split("-")[0].upper()
    if not s.startswith("KX"): return None
    s = s[2:]
    for c, ks in KEYS.items():
        if any(s.startswith(k) for k in ks): return c
    return None
def is15(tk, comm=None):
    comm = comm or comm_of(tk); return bool(comm) and str(tk).upper().startswith(K15[comm] + "-")


def label15(meta, tk):
    """'15-min · target $4,041.83' instead of the market's question text."""
    m = re.search(r"Target Price:\s*([^\]]+)", meta.get("title") or "")
    return "15-min window" + (f" · target {m.group(1).strip()}" if m else "")


def session(t):
    h = datetime.fromtimestamp(t, ET).hour
    return "US" if 9 <= h < 18 else ("EU" if 3 <= h < 9 else "ASIA")


# ---------------- Kalshi public API ----------------
SES = requests.Session(); SES.headers["User-Agent"] = "kalshi-commodity-scanner/2.0"
_LOCK, _LAST = threading.Lock(), [0.0]


def get(path, **params):
    for i in range(5):
        with _LOCK:
            w = 1 / RPS - (time.time() - _LAST[0])
            if w > 0: time.sleep(w)
            _LAST[0] = time.time()
        try:
            r = SES.get(API + path, params={k: v for k, v in params.items() if v is not None}, timeout=20)
            if r.status_code == 429: time.sleep(2 ** i); continue
            if r.status_code in (400, 404): return {}
            r.raise_for_status(); return r.json()
        except (requests.RequestException, ValueError) as e:
            if i == 4: print("GET failed", path, e, flush=True); return {}
            time.sleep(2 ** i)
    return {}


def parse(t):
    """Trade -> (ts, id, ticker, side +1 YES / -1 NO, yes_price, contracts, $ paid by taker)."""
    yp = fnum(t.get("yes_price_dollars"), None)
    if yp is None: yp = fnum(t.get("yes_price")) / 100
    npx = fnum(t.get("no_price_dollars"), None)
    if npx is None: npx = 1 - yp
    n = fnum(t.get("count_fp"), None)
    if n is None: n = fnum(t.get("count"))
    sd = 1 if (t.get("taker_side") or "").lower() == "yes" else -1
    return ts_of(t["created_time"]), t.get("trade_id", ""), t.get("ticker", ""), sd, yp, n, n * (yp if sd > 0 else npx)


def trades_since(t0, max_pages=30):
    """Commodity trades with ts >= t0, oldest first (the public feed covers every market; we keep commodities)."""
    out, cur = [], None
    for _ in range(max_pages):
        j = get("/markets/trades", limit=1000, min_ts=int(t0), cursor=cur); tr = j.get("trades") or []
        for x in tr:
            if comm_of(x.get("ticker", "")):
                try: out.append(parse(x))
                except Exception: pass
        cur = j.get("cursor")
        if not cur or not tr: break
    return sorted(out, key=lambda r: r[0])


_CUT = {}


def trade_cutoff():
    if "t" not in _CUT:
        j = get("/historical/cutoff"); v = j.get("trades_created_ts") or j.get("trades_cutoff_ts")
        _CUT["t"] = ts_of(v) if isinstance(v, str) else fnum(v, 0)
    return _CUT["t"]


def ticker_trades(tk, t0, t1):
    """All trades of one market in [t0, t1] (historical archive for old ones)."""
    paths = ("/historical/trades",) if t1 < trade_cutoff() else ("/markets/trades",)
    out = []
    for path in paths:
        cur = None
        for _ in range(20):
            j = get(path, ticker=tk, limit=1000, min_ts=int(t0), max_ts=int(t1) + 1, cursor=cur); tr = j.get("trades") or []
            mine = [x for x in tr if x.get("ticker", tk) == tk]
            if tr and not mine: break                     # endpoint ignored the ticker filter: don't page the whole exchange
            for x in mine:
                try: out.append(parse(x))
                except Exception: pass
            cur = j.get("cursor")
            if not cur or not tr: break
    return out


def minute_flow(trs):
    """Trades -> {candle end ts: [YES taker $, NO taker $, signed big-trade $]}."""
    f = defaultdict(lambda: [0.0, 0.0, 0.0])
    for ts, _, _, sd, _, _, usd in trs:
        b = f[int(math.ceil(ts / 60) * 60)]; b[0 if sd > 0 else 1] += usd
        if usd >= BIG: b[2] += sd * usd
    return f


def cval(cd, side, k="close"):
    d = cd.get(side) or {}
    v = d.get(f"{k}_dollars")
    if v is None:
        v = fnum(d.get(k), float("nan"))
        return v / 100 if v > 1.0 else v  # legacy cent fields
    return fnum(v, float("nan"))


def candles(series, tk, t0, t1):
    for path in (f"/series/{series}/markets/{tk}/candlesticks", f"/historical/markets/{tk}/candlesticks"):
        cs = get(path, start_ts=int(t0), end_ts=int(t1), period_interval=1).get("candlesticks") or []
        if cs: return cs
    return []


def window_rows(mkt, m, upto=None):
    """One 15-min window -> 1-min Kalshi quote rows + that minute's order flow (same schema offline and live)."""
    t1 = int(ts_of(m["close_time"])); t_end = min(t1, int(upto)) if upto else t1
    fl = minute_flow(ticker_trades(m["ticker"], t1 - 900, t_end))
    out = []
    for cd in candles(K15[mkt], m["ticker"], t1 - 900, t_end):
        e = int(cd["end_period_ts"]); y, n, b = fl.get(e, (0.0, 0.0, 0.0))
        out.append(dict(ticker=m["ticker"], close=m["close_time"], strike=m.get("floor_strike"), up=int(m.get("result") == "yes"),
                        ts=e, bid=cval(cd, "yes_bid"), ask=cval(cd, "yes_ask"), last=cval(cd, "price"),
                        vol=fnum(cd.get("volume_fp", cd.get("volume"))), yf=round(y, 2), nf=round(n, 2), bf=round(b, 2)))
    return out


def settled_windows(mkt, since):
    """Settled 15-min windows closing after `since`: live listing, then the historical archive."""
    got = {}
    for path in ("/markets", "/historical/markets"):
        cur = None
        for _ in range(300):
            j = get(path, series_ticker=K15[mkt], status="settled" if path == "/markets" else None, limit=1000, cursor=cur, min_close_ts=int(since))
            ms = j.get("markets") or []
            for m in ms:
                if m.get("ticker", "").startswith(K15[mkt] + "-") and m.get("result") in ("yes", "no") and m.get("close_time") and ts_of(m["close_time"]) >= since: got.setdefault(m["ticker"], m)
            cur = j.get("cursor")
            if not cur or not ms or ts_of(ms[-1].get("close_time") or "2000-01-01T00:00:00Z") < since: break
        if got and min(ts_of(m["close_time"]) for m in got.values()) < since + 2 * 86400: break
    return sorted(got.values(), key=lambda m: m["close_time"])


def kpath(mkt): return f"{DATA}/k15_{mkt}.csv.gz"


def read_gz(p, cols=None):
    try: d = pd.read_csv(p)
    except Exception: return pd.DataFrame(columns=cols or [])
    for c in cols or []:
        if c not in d: d[c] = np.nan
    return d


def load_k(mkt):
    """Our cache (with order flow) ∪ the commodity bot's cache, deduped (ours wins)."""
    d = pd.concat([read_gz(kpath(mkt), KCOLS), read_gz(f"{OLD_CACHE}/k_{mkt}.csv.gz", KCOLS)], ignore_index=True)
    return d.drop_duplicates(["ticker", "ts"], keep="first") if len(d) else d


def kfetch(mkt, days, sample=1, recent_days=WEEKS_D, deadline=None):
    """Pull settled windows of the last `days` (every `sample`-th one older than `recent_days`) with trades, and
    add order flow to the commodity bot's windows we only have quotes for. Newest first, saved every chunk,
    stops at `deadline` (the next build continues where this one stopped)."""
    mine = read_gz(kpath(mkt), KCOLS); have = set(mine.ticker); now = time.time()
    ms = [m for m in settled_windows(mkt, now - days * 86400) if m["ticker"] not in have]
    ms = [m for i, m in enumerate(ms) if ts_of(m["close_time"]) >= now - recent_days * 86400 or i % sample == 0]
    old = read_gz(f"{OLD_CACHE}/k_{mkt}.csv.gz", KCOLS); old = old[~old.ticker.isin(have)]
    known = {m["ticker"] for m in ms}
    enrich = old.drop_duplicates("ticker")[["ticker", "close", "strike", "up"]]
    enrich = [dict(ticker=r.ticker, close_time=r.close, floor_strike=r.strike, result="yes" if r.up == 1 else "no")
              for r in enrich.itertuples() if r.ticker not in known]
    todo = sorted(ms + enrich, key=lambda m: m["close_time"], reverse=True); done = 0
    for i in range(0, len(todo), 150):
        if deadline and time.time() > deadline: break
        ch = todo[i:i + 150]
        with ThreadPoolExecutor(4) as ex: rows = [r for rs in ex.map(lambda m: window_rows(mkt, m), ch) for r in rs]
        done += len(ch)
        if rows:
            allr = pd.concat([read_gz(kpath(mkt), KCOLS), pd.DataFrame(rows, columns=KCOLS)], ignore_index=True).drop_duplicates(["ticker", "ts"])
            allr = allr[allr.close.map(ts_of) >= now - (MONTHS_D + 10) * 86400]
            os.makedirs(DATA, exist_ok=True); allr.to_csv(kpath(mkt), index=False, compression="gzip")
    print(f"KFETCH {mkt}: {done}/{len(todo)} windows pulled ({len(ms)} new, {len(enrich)} bot windows given order flow) · "
          f"total {load_k(mkt).ticker.nunique()}" + (" · stopped at time budget" if done < len(todo) else ""), flush=True)


def harvest():
    """Keep the commodity part of everything this scanner gathered before (all-markets runs), drop the rest."""
    wh = []
    for p in glob.glob(f"{DATA}/whales_*.csv.gz"):
        d = read_gz(p)
        if len(d): wh.append(d[d.tk.map(comm_of).notna()])
    n_marks = 0
    for p in glob.glob(f"{DATA}/marks_*.csv.gz"):
        d = read_gz(p); n_marks += int(d.tk.map(comm_of).notna().sum()) if len(d) else 0
    out = pd.concat([read_gz(f"{DATA}/c_whales.csv.gz")] + wh, ignore_index=True) if wh else read_gz(f"{DATA}/c_whales.csv.gz")
    if len(out): out.drop_duplicates(["t", "tk", "sd"]).to_csv(f"{DATA}/c_whales.csv.gz", index=False, compression="gzip")
    for p in glob.glob(f"{DATA}/*"):
        if not os.path.basename(p).startswith(("k15_", "c_whales", "meta", "state", "live_preds")): os.remove(p)
    print(f"HARVEST: {len(out)} commodity whale events kept · {n_marks} commodity snapshots seen", flush=True)
    return out


def whale_stats():
    """Per commodity: how whales did 15m / 1h later (from all whale history gathered so far)."""
    d = read_gz(f"{DATA}/c_whales.csv.gz")
    if not len(d) or "r15" not in d: return {}
    d["comm"] = d.tk.map(comm_of)
    return {c: [int(len(g)), float(g.r15.sum()), float(g.r60.sum())] for c, g in d.dropna(subset=["r15"]).groupby("comm")}


# ---------------- features + model (same code offline and live) ----------------
def kcols(kd):
    """1-min Kalshi quotes + flow -> per-minute features (shared by the settlement model and the cheap-spike model)."""
    kd = kd.dropna(subset=["bid", "ask"]).copy()
    if not len(kd): return kd
    for c in ("yf", "nf", "bf", "vol"): kd[c] = pd.to_numeric(kd.get(c, 0), errors="coerce").fillna(0)
    kd["mid"] = (kd.bid + kd.ask) / 2; kd = kd.sort_values(["ticker", "ts"]); g = kd.groupby("ticker")
    for n in (1, 3, 5): kd[f"dmid{n}"] = (kd.mid - g.mid.shift(n)).fillna(0)
    kd["spread"] = kd.ask - kd.bid
    r3 = lambda col: g[col].transform(lambda v: v.rolling(3, min_periods=1).sum())
    kd["kvol"] = np.log1p(r3("vol")); kd["vcum"] = np.log1p(g.vol.cumsum())
    y3, n3 = r3("yf"), r3("nf"); kd["ofi3"] = (y3 - n3) / (y3 + n3 + 1); kd["bigc"] = slog(g.bf.cumsum())
    kd["cl"] = kd.close.map(ts_of); kd["tl"] = (kd.cl - kd.ts) / 60
    return kd


def kframe(kd):
    """1-min Kalshi quotes + flow -> one row per window-minute with 3-12 min left: features, Kalshi mid, outcome."""
    kd = kcols(kd)
    if not len(kd): return kd
    kd = kd[(kd.tl >= 3) & (kd.tl <= 12) & (kd.mid > 0.02) & (kd.mid < 0.98)].copy()
    kd["tleft"] = kd.tl / 12; kd["ext"] = (kd.mid - 0.5).abs()
    ss = kd.ts.map(session)
    for s in SESS: kd[f"s_{s}"] = (ss == s).astype(float)
    kd["mkt"] = kd.ticker.map(comm_of)
    for c in COMMS: kd[f"m_{c}"] = (kd.mkt == c).astype(float)
    return kd.replace([np.inf, -np.inf], np.nan).dropna(subset=list(KF) + ["mid"])


LOW, LEV = 0.20, 0.03   # cheap side = ask ≤ 20¢; alert when expected profit ≥ 3¢/contract after fees
LF = ("lask", "dmid1s", "dmid3s", "dmid5s", "spread", "kvol", "vcum", "tleft", "ofi3s", "bigcs") + \
     tuple(f"s_{s}" for s in SESS) + tuple(f"m_{c}" for c in COMMS)


def feev(a): a = np.clip(np.asarray(a, float), 0.01, 0.99); return np.ceil(7 * a * (1 - a) - 1e-9) / 100


def lframe(kd):
    """Cheap contracts (either side ≤ 20¢, 2-13 min left). Target = sell at 2x the entry (at least +10¢).
    hit = that side's bid reached the target later in the window; pnl = buy at ask + fee, sell at target (fee) if hit,
    otherwise hold to settlement."""
    kd = kcols(kd)
    if not len(kd): return kd
    kd = kd.sort_values(["ticker", "ts"]); g = kd.groupby("ticker")
    later_max = lambda v: v.iloc[::-1].cummax().iloc[::-1].shift(-1)
    kd["fyb"] = g.bid.transform(later_max); kd["nb"] = 1 - kd.ask; kd["fnb"] = kd.groupby("ticker").nb.transform(later_max)
    ss = kd.ts.map(session); mk = kd.ticker.map(comm_of); out = []
    for sgn in (1, -1):
        d = kd.assign(side=sgn, lask=kd.ask if sgn > 0 else 1 - kd.bid, fb=kd.fyb if sgn > 0 else kd.fnb,
                      win=(pd.to_numeric(kd.up, errors="coerce") == (1 if sgn > 0 else 0)).astype(float))
        d = d[(d.tl >= 2) & (d.tl <= 13) & (d.lask >= 0.02) & (d.lask <= LOW)].copy()
        for n in (1, 3, 5): d[f"dmid{n}s"] = d[f"dmid{n}"] * sgn
        d["ofi3s"], d["bigcs"] = d.ofi3 * sgn, d.bigc * sgn; out.append(d)
    d = pd.concat(out); d["tgt"] = np.minimum(np.maximum(2 * d.lask, d.lask + 0.10), 0.99)
    d["hit"] = (d.fb >= d.tgt - 1e-9).astype(float)
    d["cost"] = d.lask + feev(d.lask); d["pnl"] = np.where(d.hit == 1, d.tgt - feev(d.tgt), d.win) - d.cost
    d["tleft"] = d.tl / 12; ss = d.ts.map(session)
    for x in SESS: d[f"s_{x}"] = (ss == x).astype(float)
    d["mkt"] = d.ticker.map(comm_of)
    for c in COMMS: d[f"m_{c}"] = (d.mkt == c).astype(float)
    return d.replace([np.inf, -np.inf], np.nan).dropna(subset=list(LF))


def ltrain(D, w8=None):
    X = D[list(LF)].to_numpy(float); mu, sd = X.mean(0), np.maximum(X.std(0), 1e-4); y = D.hit.to_numpy(float)
    b = float(logit(np.clip(y.mean(), 0.01, 0.99)))
    w = fit_offset(np.clip((X - mu) / sd, -6, 6), y, np.full(len(y), b), w8)
    return dict(w=[round(float(v), 5) for v in w], mu=[round(float(v), 6) for v in mu], sd=[round(float(v), 6) for v in sd], b=round(b, 5))


def lp(M, D):
    Z = np.clip((D[list(LF)].to_numpy(float) - np.asarray(M["mu"])) / np.asarray(M["sd"]), -6, 6)
    return sig(M["b"] + Z @ np.asarray(M["w"]))


def lev(M, D):
    """Expected profit per contract: spike to target (sell) or, if not, assume it expires worthless (conservative)."""
    p = lp(M, D); return p, p * (D.tgt.to_numpy() - feev(D.tgt)) - D.cost.to_numpy()


def leval(M, D):
    """Betting test on unseen rows: first minute per window-side with expected profit ≥ LEV."""
    if not len(D): return {}
    p, ev = lev(M, D)
    B = D.assign(p=p, ev=ev)[ev >= LEV].sort_values("ts").groupby(["ticker", "side"]).head(1)
    r = dict(rows=int(len(D)), base=round(float(D.hit.mean()), 3), trades=int(len(B)))
    if len(B): r.update(hit=round(float(B.hit.mean()), 3), pred=round(float(B.p.mean()), 3), roi=round(float(B.pnl.sum() / B.cost.sum()), 3),
                        avg_ask=round(float(B.lask.mean()), 3))
    return r


def lproven(W, Mo, n_w=10, n_m=20):
    ok = lambda r, n: bool(r and r.get("trades", 0) >= n and (r.get("roi") or -1) > 0)
    return ok(W, n_w) and ok(Mo, n_m)


def fmt_low(r):
    if not r: return "no data"
    s = f"cheap rows {r['rows']:,}, spike-to-target normally {r['base']:.0%}"
    if r.get("trades"): s += f" · alerts {r['trades']}: hit {r['hit']:.0%} (model said {r['pred']:.0%}), ROI {r['roi']:+.0%} at avg {r['avg_ask'] * 100:.0f}¢"
    return s


def train_low(now):
    """Cheap-spike model: weeks (older 70% → newest 30%) and months (weeks → older months), per market."""
    D = pd.concat([lframe(load_k(m)) for m in COMMS], ignore_index=True)
    if not len(D): return {}
    Wk, Mo = D[D.cl >= now - WEEKS_D * 86400], D[D.cl < now - WEEKS_D * 86400]
    wins = Wk.sort_values("cl").ticker.drop_duplicates().tolist(); cut = set(wins[int(len(wins) * 0.7):])
    tr, te = Wk[~Wk.ticker.isin(cut)], Wk[Wk.ticker.isin(cut)]
    Mw, Mwk = ltrain(tr), ltrain(Wk); Mdep = ltrain(D, np.asarray(0.5 ** ((D.cl.max() - D.cl) / (21 * 86400)), float))
    by = lambda M, X: {str(k): leval(M, g) for k, g in X.groupby("mkt")} if len(X) else {}
    L = dict(weeks=dict(test=leval(Mw, te), test_by=by(Mw, te)), months=dict(test=leval(Mwk, Mo), test_by=by(Mwk, Mo)), model=Mdep)
    L["proven"] = {c: lproven(L["weeks"]["test_by"].get(c), L["months"]["test_by"].get(c)) for c in COMMS}
    return L


def fit_offset(X, y, off, w8=None, lam=0.02, iters=900):
    """Logistic regression with Kalshi's log-odds as a fixed offset: learns only what Kalshi's price misses."""
    w = np.zeros(X.shape[1]); w8 = np.ones(len(y)) if w8 is None else w8 / w8.mean()
    for _ in range(iters):
        p = sig(off + X @ w); w -= 0.3 * (X.T @ ((p - y) * w8) / len(y) + lam * w)
    return w


def train_on(D, w8=None):
    X = D[list(KF)].to_numpy(float); mu, sd = X.mean(0), np.maximum(X.std(0), 1e-4)  # constant columns stay finite after rounding
    w = fit_offset(np.clip((X - mu) / sd, -6, 6), D.up.to_numpy(float), logit(D.mid), w8)
    return dict(w=[round(float(v), 5) for v in w], mu=[round(float(v), 6) for v in mu], sd=[round(float(v), 6) for v in sd])


def p_of(M, D):
    Z = np.clip((D[list(KF)].to_numpy(float) - np.asarray(M["mu"])) / np.asarray(M["sd"]), -6, 6)
    return sig(logit(D.mid) + Z @ np.asarray(M["w"]))


def evaluate(M, D):
    """Model vs Kalshi on unseen rows + a betting test: first minute per window where the model beats the ask by EDGE
    after fees (ask ≤ 70¢), held to settlement."""
    if not len(D): return {}
    p = p_of(M, D); y = D.up.to_numpy(float); mid = D.mid.to_numpy()
    ll = lambda q: float(-np.mean(y * np.log(np.clip(q, 1e-6, 1)) + (1 - y) * np.log(np.clip(1 - q, 1e-6, 1))))
    up = p >= 0.5; ps = np.where(up, p, 1 - p); ask = np.where(up, D.ask, 1 - D.bid)
    B = pd.DataFrame(dict(ticker=D.ticker.to_numpy(), ts=D.ts.to_numpy(), up=up, y=y, ask=ask, edge=ps - ask - fees(ask)))
    bet = B[(B.edge >= EDGE) & (B.ask <= KMAX) & (B.ask > 0.03)].sort_values("ts").groupby("ticker").head(1)
    won = (bet.up == (bet.y == 1)).astype(float); cost = bet.ask + fees(bet.ask)
    return dict(windows=int(D.ticker.nunique()), rows=int(len(D)), ll_model=round(ll(p), 4), ll_kalshi=round(ll(mid), 4),
                acc_model=round(float((up == (y == 1)).mean()), 3), acc_kalshi=round(float(((mid >= 0.5) == (y == 1)).mean()), 3),
                trades=int(len(bet)), win=round(float(won.mean()), 3) if len(bet) else None,
                roi=round(float((won - cost).sum() / cost.sum()), 3) if len(bet) else None)


def eval_by(M, D, key): return {str(k): evaluate(M, g) for k, g in D.groupby(key)} if len(D) else {}


def proven(W, Mo, n_w=15, n_m=25):
    """Beats Kalshi on BOTH the newest weeks and the older months, with a profitable betting test on each."""
    ok = lambda r, n: bool(r and r.get("trades", 0) >= n and (r.get("roi") or -1) > 0 and r["ll_model"] <= r["ll_kalshi"])
    return ok(W, n_w) and ok(Mo, n_m)


def train(push=True):
    D = pd.concat([kframe(load_k(m)) for m in COMMS], ignore_index=True); old = load_json(f"{DIR}/model.json", {})
    if not len(D): print("train: no data"); return old
    now = time.time(); Wk, Mo = D[D.cl >= now - WEEKS_D * 86400], D[D.cl < now - WEEKS_D * 86400]
    if Wk.ticker.nunique() < 300: print(f"train: only {Wk.ticker.nunique()} recent windows (need 300)"); return old
    wins = Wk.sort_values("cl").ticker.drop_duplicates().tolist(); cut = set(wins[int(len(wins) * 0.7):])
    tr, te = Wk[~Wk.ticker.isin(cut)], Wk[Wk.ticker.isin(cut)]
    Mw, Mwk = train_on(tr), train_on(Wk)                    # weeks-only models (tested on newest weeks / on months)
    miss = set(load_json(f"{DATA}/state.json", {}).get("missed", []))
    w8 = 0.5 ** ((D.cl.max() - D.cl) / (21 * 86400)) * np.where(D.ticker.isin(miss), 1.5, 1.0)
    Mdep = train_on(D, np.asarray(w8, float))               # deployed: everything; recent + live misses weigh more
    flow_cov = float(((D.yf if "yf" in D else 0) + (D.nf if "nf" in D else 0) > 0).mean())
    R = dict(trained=int(now), flow_coverage=round(flow_cov, 3), whale_events=int(len(read_gz(f"{DATA}/c_whales.csv.gz"))),
             weeks=dict(windows=len(wins), test=evaluate(Mw, te), test_by=eval_by(Mw, te, "mkt")),
             months=dict(windows=int(Mo.ticker.nunique()), test=evaluate(Mwk, Mo), test_by=eval_by(Mwk, Mo, "mkt"),
                         by_month=eval_by(Mwk, Mo.assign(mon=pd.to_datetime(Mo.cl, unit="s").dt.strftime("%Y-%m")), "mon")))
    R["proven"] = {c: proven(R["weeks"]["test_by"].get(c), R["months"]["test_by"].get(c)) for c in COMMS}
    R["model"] = Mdep; R["feats"] = sorted(((KF[i], Mdep["w"][i]) for i in range(len(KF))), key=lambda z: -abs(z[1]))[:5]
    try: R["low"] = train_low(now)
    except Exception as e: print("low-spike model:", e, flush=True); R["low"] = old.get("low", {})
    save_json(f"{DIR}/model.json", R); write_report(R); print(summary(R), flush=True)
    if push: notify("🧠 Commodity model retrained", summary(R), 3)
    return R


def fmt_eval(r):
    if not r: return "no data"
    s = f"{r['windows']} windows · right {r['acc_model']:.0%} vs Kalshi {r['acc_kalshi']:.0%} · logloss {r['ll_model']} vs {r['ll_kalshi']}"
    if r.get("trades"): s += f" · edge bets {r['trades']}: won {r['win']:.0%}, ROI {r['roi']:+.0%}"
    return s


def summary(R):
    L = [f"Last 3 weeks (newest 30%, unseen): {fmt_eval(R['weeks']['test'])}",
         f"Past months (unseen, {R['months']['windows']} windows): {fmt_eval(R['months']['test'])}"]
    pv = [c for c, v in R["proven"].items() if v]
    L.append("PROVEN (beats Kalshi in both): " + (", ".join(pv) if pv else "none yet: boards show odds, no edge calls"))
    L.append("Leans on: " + ", ".join(f"{k} {'+' if v > 0 else '−'}" for k, v in R["feats"]))
    lo = R.get("low") or {}
    if lo:
        L.append(f"Cheap-spike alerts · weeks: {fmt_low(lo['weeks']['test'])}")
        L.append(f"Cheap-spike alerts · months: {fmt_low(lo['months']['test'])}")
        pl = [c for c in SHOW if lo.get("proven", {}).get(c)]
        L.append("Cheap-spike PROVEN: " + (", ".join(pl) if pl else "none yet"))
    return "\n".join(L)


def write_report(R):
    L = ["# Kalshi commodity 15-min model report", f"Trained {datetime.fromtimestamp(R['trained'], ET):%Y-%m-%d %H:%M} ET", "",
         "Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).",
         "**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on "
         f"older months it never saw. Edge bets buy at the ask + fee when the model beats it by {EDGE * 100:.0f}+ pts (≤70¢), held to settlement.",
         f"Order-flow coverage: {R['flow_coverage']:.0%} of rows · commodity whale events on file: {R['whale_events']}", "",
         "| Market | Weeks test | Months test | Proven |", "|---|---|---|---|"]
    for c in SHOW:
        L.append(f"| {c} | {fmt_eval(R['weeks']['test_by'].get(c))} | {fmt_eval(R['months']['test_by'].get(c))} | {'✅' if R['proven'][c] else '—'} |")
    L += ["", f"**All weeks:** {fmt_eval(R['weeks']['test'])}", "", f"**All months:** {fmt_eval(R['months']['test'])}", "", "| Month | Result |", "|---|---|"]
    L += [f"| {k} | {fmt_eval(v)} |" for k, v in sorted(R["months"]["by_month"].items())]
    L += ["", "Strongest signals: " + ", ".join(f"`{k}` {v:+.3f}" for k, v in R["feats"])]
    lo = R.get("low") or {}
    if lo:
        L += ["", "## Cheap-spike alerts", f"Contracts at {LOW * 100:.0f}¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) "
              "if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ "
              f"{LEV * 100:.0f}¢ per contract.", "", "| Market | Weeks test | Months test | Proven |", "|---|---|---|---|"]
        for c in SHOW:
            L.append(f"| {c} | {fmt_low(lo['weeks']['test_by'].get(c))} | {fmt_low(lo['months']['test_by'].get(c))} | {'✅' if lo['proven'].get(c) else '—'} |")
        L += ["", f"**All weeks:** {fmt_low(lo['weeks']['test'])}", "", f"**All months:** {fmt_low(lo['months']['test'])}"]
    os.makedirs(DIR, exist_ok=True); open(f"{DIR}/report.md", "w").write("\n".join(L) + "\n")


# ---------------- live: whales, spikes, flow ----------------
class Meta:
    def __init__(self): self.m = load_json(f"{DATA}/meta.json", {}); self.se = {}; self.bad = set()

    def get(self, tk):
        if tk in self.m: return self.m[tk]
        if tk in self.bad: return None
        mk = get(f"/markets/{tk}").get("market")
        if not mk: self.bad.add(tk); return None
        s = tk.split("-")[0]
        if s not in self.se: self.se[s] = get(f"/series/{s}").get("series") or {}
        st = (mk.get("strike_type") or "").lower(); title = mk.get("title") or tk; sub = mk.get("yes_sub_title") or ""
        if sub and sub.lower() not in title.lower(): title = f"{title} [{sub}]"
        d = 1 if (s.upper().endswith("15M") or st.startswith("greater")) else (-1 if st.startswith("less") else 0)  # is YES bullish?
        e = mk.get("event_ticker", "")
        self.m[tk] = dict(title=title[:90], comm=comm_of(tk), dir=d, close=ts_of(mk["close_time"]) if mk.get("close_time") else 0,
                          link=f"{WEB}/{s.lower()}/{slug(self.se[s]['title'])}/{e.lower()}" if self.se[s].get("title") else f"{WEB}/{s.lower()}")
        return self.m[tk]

    def save(self):
        now = time.time(); self.m = {k: v for k, v in self.m.items() if v and (not v["close"] or v["close"] > now - 3 * 86400)}
        save_json(f"{DATA}/meta.json", self.m)


class Tk:
    __slots__ = ("mids", "bid", "bid_t", "ask", "ask_t", "last", "cl", "tr", "spike_t")
    def __init__(self): self.mids, self.tr = deque(), deque(); self.bid = self.ask = self.last = None; self.bid_t = self.ask_t = 0; self.cl = {}; self.spike_t = 0
    def fresh(self, t): return self.bid is not None and self.ask is not None and t - self.bid_t < 600 and t - self.ask_t < 600 and self.ask >= self.bid
    def mid(self, t): return (self.bid + self.ask) / 2 if self.fresh(t) else self.last
    def mid_at(self, t):
        for ts, m in reversed(self.mids):
            if ts <= t: return m
        return self.mids[0][1] if self.mids else None


class Live:
    def __init__(self, meta, st):
        self.meta, self.T = meta, defaultdict(Tk)
        self.flow = st.get("flow", {})            # comm -> {hour: bullish $ (YES on up/above markets, NO on below)}
        self.unw = st.get("unw", {})              # comm -> [whales, opposite whales after (likely cash-outs), minutes, gain]
        self.recent = st.get("recent", {})        # ticker -> whales of last 3h
        self.pend_w = st.get("pend_w", [])        # whales awaiting 15m/60m grading
        self.wstats = whale_stats() or st.get("wstats", {})  # comm -> [n, sum r15, sum r60] from all whale history
        self.calls = st.get("calls", [])          # edge calls (graded at settlement)
        self.snaps = st.get("snaps", {})          # 15-min ticker -> checkpoint predictions
        self.missed = st.get("missed", []); self.rows = []
        self.wl = [w for w in st.get("wl", []) if len(w) > 4]  # graded board leans: [t1, comm, lean right, kalshi right, bet?, bet won]
        self.res_pend = st.get("res_pend", {})    # window close -> graded rows waiting to be sent together
        self.shown = st.get("shown", {})          # ticker -> exactly what the board showed (graded at settlement)
        self.stats = st.get("stats", dict(trades=0, whales=0, vol=0.0)); self.quiet = 0; self.cool = {}; self.sent_h = defaultdict(int)

    def ingest(self, ts, tk, sd, yp, n, usd, alert=True):
        self.stats["trades"] += 1; k = self.T[tk]; m0 = k.mid(ts)
        if sd > 0: k.ask, k.ask_t = yp, ts
        else: k.bid, k.bid_t = yp, ts
        k.last = yp; m = k.mid(ts); k.mids.append((ts, m)); k.tr.append((ts, sd, usd))
        while len(k.mids) > 1 and k.mids[1][0] < ts - 3900: k.mids.popleft()
        while k.tr and k.tr[0][0] < ts - 300: k.tr.popleft()
        c = k.cl.get(sd)
        if c and ts - c[1] <= CLUSTER_GAP: c[1] = ts; c[2] += usd; c[3] += 1; c[4] += n
        else:
            if c: self.close_whale(tk, sd, c, alert)
            k.cl[sd] = [ts, ts, usd, 1, n, m0 if m0 is not None else m]
        thr = 0.15 if tk.split("-")[0].upper().endswith("15M") else 0.05
        if alert and ts - k.spike_t > 900 and k.fresh(ts):
            a = k.mid_at(ts - 120)
            if a is not None and abs(m - a) >= thr and sum(x[2] for x in k.tr if x[0] >= ts - 120) >= 200:
                k.spike_t = ts; self.spike(tk, k, ts, a, m)

    def tick(self, now, alert=True):
        for tk, k in list(self.T.items()):
            for sd, c in list(k.cl.items()):
                if now - c[1] > CLUSTER_GAP: self.close_whale(tk, sd, c, alert); k.cl.pop(sd)
            if not k.cl and k.mids and k.mids[-1][0] < now - 7200: self.T.pop(tk)
        keep = []
        for e in self.pend_w:  # grade whales: price 15m / 60m later from their side's view
            if now < e["t"] + 3600: keep.append(e); continue
            k = self.T.get(e["tk"]); f = lambda t: (k.mid_at(t) if k and k.mids else None) or e["m1"]
            s = (lambda x: x) if e["sd"] > 0 else (lambda x: 1 - x)
            r15, r60 = s(f(e["t"] + 900)) - e["px"], s(f(e["t"] + 3600)) - e["px"]
            w = self.wstats.setdefault(e["comm"], [0, 0.0, 0.0]); w[0] += 1; w[1] += r15; w[2] += r60
            self.rows.append(dict(t=e["t"], tk=e["tk"], sd=e["sd"], usd=e.get("usd", 0), px=e["px"], r15=round(r15, 4), r60=round(r60, 4)))
        self.pend_w = keep

    def flush(self):
        if not self.rows: return
        p = f"{DATA}/c_whales.csv.gz"; os.makedirs(DATA, exist_ok=True)
        pd.DataFrame(self.rows).to_csv(p, mode="ab", index=False, header=not os.path.exists(p), compression="gzip"); self.rows = []

    def close_whale(self, tk, sd, c, alert):
        t0, t1, usd, nprints, cnt, m_before = c
        if usd < MIN_WHALE or t0 <= self.quiet: return
        meta = self.meta.get(tk) or {}; comm = meta.get("comm") or comm_of(tk); px = usd / max(cnt, 1e-9); k = self.T[tk]
        self.stats["whales"] += 1; self.stats["vol"] += usd
        bull = sd * meta.get("dir", 0)
        if bull: f = self.flow.setdefault(comm, {}); h = str(int(t1 // 3600)); f[h] = f.get(h, 0) + bull * usd
        u = self.unw.setdefault(comm, [0, 0, 0.0, 0.0]); u[0] += 1
        for w in self.recent.get(tk, []):
            if w[1] == -sd and len(w) == 4 and usd >= 0.5 * w[2]: u[1] += 1; u[2] += (t0 - w[0]) / 60; u[3] += (1 - px) - w[3]; w.append(1)
        self.recent.setdefault(tk, []).append([t0, sd, usd, px])
        self.pend_w.append(dict(t=t0, tk=tk, comm=comm, sd=sd, usd=round(usd, 2), px=px, m1=k.mid(t1)))
        print(f"WHALE {money(usd):>8} {'YES' if sd > 0 else 'NO '} @{cents(px):>4} x{nprints:<3} {meta.get('title', tk)[:70]}", flush=True)
        if not alert or usd < ALERT_WHALE or not is15(tk, comm) or not on("whales", comm) or not self.allow("whale", tk, 600, 6): return
        side = "YES" if sd > 0 else "NO"
        L = [label15(meta, tk), f"{side} @ {cents(px)} · {nprints} prints merged" + (f" · {'BULLISH' if bull > 0 else 'BEARISH'} {comm}" if bull else "")]
        pre = ((k.mid_at(t0 - 1) or m_before) - (k.mid_at(t0 - 600) or m_before)) * sd * 100
        if abs(pre) >= 3: L.append(f"{'Chasing' if pre > 0 else 'Fading'}: price moved {pre:+.0f}¢ {'their way' if pre > 0 else 'against them'} in the last 10m")
        w = self.wstats.get(comm)
        if w and w[0] >= 15: L.append(f"Past {comm} whales: {w[1] / w[0] * 100:+.1f}¢ after 15m, {w[2] / w[0] * 100:+.1f}¢ after 1h (n={w[0]})")
        if u[0] >= 20 and u[1]: L.append(f"{u[1] / u[0]:.0%} of {comm} whales see an opposite whale (likely cash-out) ~{u[2] / u[1]:.0f}m later, avg {u[3] / u[1] * 100:+.1f}¢")
        L.append("Whale flow: " + self.flow_txt(comm))
        notify(f"🐋 {money(usd)} {side} · {comm}", "\n".join(L), 4 if usd >= 4 * ALERT_WHALE else 3, meta.get("link"))

    def spike(self, tk, k, ts, a, m):
        meta = self.meta.get(tk) or {}; comm = meta.get("comm") or comm_of(tk)
        if not is15(tk, comm) or not on("spikes", comm) or not self.allow("spike", tk, 900, 4): return
        bull = (1 if m > a else -1) * meta.get("dir", 0)
        notify(f"⚡ {comm} spike {'UP ' if bull > 0 else 'DOWN ' if bull < 0 else ''}{abs(m - a) * 100:.0f}¢",
               f"{label15(meta, tk)}\nYES {cents(a)} → {cents(m)} in 2m · {money(sum(x[2] for x in k.tr if x[0] >= ts - 120))} traded\nWhale flow: {self.flow_txt(comm)}",
               4, meta.get("link"))

    def allow(self, kind, tk, cool, cap):
        hr = int(time.time() // 3600)
        if time.time() - self.cool.get((kind, tk), 0) < cool or self.sent_h[(kind, hr)] >= cap: return False
        self.cool[(kind, tk)] = time.time(); self.sent_h[(kind, hr)] += 1; return True

    def flow_txt(self, comm):
        h = int(time.time() // 3600); f = self.flow.get(comm, {})
        f1 = sum(v for k, v in f.items() if int(k) >= h); f24 = sum(v for k, v in f.items() if int(k) > h - 24)
        tag = lambda x: f"{'+' if x >= 0 else '−'}{money(abs(x))}{' bullish' if x > 0 else ' bearish' if x < 0 else ''}"
        return f"{tag(f1)} this hour · {tag(f24)} 24h"

    def state(self):
        h = int(time.time() // 3600) - 24
        self.flow = {c: {k: v for k, v in f.items() if int(k) > h} for c, f in self.flow.items()}
        self.recent = {t: [w for w in ws if w[0] > time.time() - 10800] for t, ws in self.recent.items() if ws}
        self.calls = [c for c in self.calls if c.get("won") is None or c["t"] > time.time() - 14 * 86400]
        return dict(flow=self.flow, unw=self.unw, recent=self.recent, pend_w=self.pend_w, wstats=self.wstats, calls=self.calls,
                    snaps=self.snaps, missed=self.missed[-500:], stats=self.stats, last_ts=self.quiet,
                    wl=[w for w in self.wl if w[0] > time.time() - 7 * 86400], res_pend=self.res_pend,
                    shown={k: v for k, v in self.shown.items() if v["t1"] > time.time() - 7200})


# ---------------- live: 15-min predictions ----------------
def open_window(c):
    ms = get("/markets", series_ticker=K15[c], status="open", limit=5).get("markets") or []
    ms = [m for m in ms if m.get("floor_strike") is not None]
    return min(ms, key=lambda m: m["close_time"]) if ms else None


_ROWS = {}


def low_live(R, c):
    """Cheap side of this window right now (≤ 20¢) -> (side, ask, target, p_hit, base, ev) if the model expects profit."""
    M = (R.get("low") or {}).get("model"); rows = _ROWS.get(c)
    if not M or not rows: return None
    D = lframe(pd.DataFrame(rows, columns=KCOLS))
    if not len(D): return None
    D = D[D.ts == D.ts.max()]
    if not len(D): return None
    p, ev = lev(M, D); i = int(np.argmax(ev)); r = D.iloc[i]
    base = ((R["low"]["weeks"]["test_by"].get(c) or {}).get("base")) or float(sig(M["b"]))
    return dict(side="YES (UP)" if r.side > 0 else "NO (DOWN)", up=bool(r.side > 0), ask=float(r.lask), tgt=float(r.tgt), p=float(p[i]),
                base=float(base), ev=float(ev[i]), tl=float(r.tl), ok=bool(ev[i] >= LEV))


def live_pred(R, c, w):
    """Latest complete minute of this window -> (p_up, mid, quote) using the exact training feature code."""
    now = time.time(); rows = [r for r in window_rows(c, {**w, "result": ""}, upto=now) if r["ts"] <= now]
    _ROWS[c] = rows
    D = kframe(pd.DataFrame(rows, columns=KCOLS)) if rows else []
    if not len(D): return None
    r = D.iloc[[-1]]; p = float(p_of(R["model"], r)[0]) if R.get("model") else float(r.mid.iloc[0])
    return p, float(r.mid.iloc[0]), dict(bid=float(r.bid.iloc[0]), ask=float(r.ask.iloc[0]), tl=float(r.tl.iloc[0]), t1=ts_of(w["close_time"]),
                                                  dmid3=float(r.dmid3.iloc[0]), dmid1=float(r.dmid1.iloc[0]))


def update9(L_, R, upd, b):
    """Second look ~9 min before the close: what changed since the board (lean, odds, BET status) and fast/trending moves."""
    if not on("board_update"): return
    pv = R.get("proven", {}); L = []; nch = nflip = 0
    for c in [x for x in SHOW if x in upd]:
        p, mid, q, flow = upd[c]; sh = L_.shown.get(q.get("tk"))
        if not sh or not on("board_update", c): continue
        up = p >= 0.5; d = "UP" if up else "DOWN"; ps = p if up else 1 - p; ask = q["ask"] if up else 1 - q["bid"]
        e = ps - ask - fee(min(max(ask, 0.01), 0.99)); go = e >= EDGE and 0.03 < ask <= KMAX
        b_up = sh["p"] >= 0.5; side = lambda x: x if up else 1 - x            # show everything on the current lean's side
        flip = b_up != up; dp, dk = (side(p) - side(sh["p"])) * 100, (side(mid) - side(sh["mid"])) * 100
        L.append((f"🟢 BET {c} {d} ≤ {cents(ask)}" if go else f"🔴 NO BET {c}")
                 + (f" · ⚡ FLIPPED to {d}" if flip else "") + (" · now BET" if go and not sh["go"] else " · BET dropped" if sh["go"] and not go else "")
                 + f" · settles {d}: model {side(sh['p']):.0%}→{ps:.0%} vs Kalshi {side(sh['mid']):.0%}→{side(mid):.0%} · edge {e * 100:+.0f} pts")
        tags = []
        if abs(q.get("dmid3", 0)) >= 0.08: tags.append(f"📈 Kalshi moved {q['dmid3'] * 100:+.0f} pts in 3 min (fast)")
        elif abs(dk) >= 5: tags.append(f"trending {'toward' if dk > 0 else 'against'} {d}: Kalshi {dk:+.0f} pts since the board")
        if not flip and abs(dp) < 3 and abs(dk) < 3 and not tags: tags.append("no real change")
        L.append("   " + " · ".join(tags) + (" ✅ tested" if go and pv.get(c) else " ⚠️ untested" if go else ""))
        nch += int(flip or abs(dp) >= 3 or abs(dk) >= 3 or go != sh["go"]); nflip += int(flip)
        L_.shown[q["tk"]].update(p9=round(p, 4), mid9=round(mid, 4), go9=bool(go), ask9=round(ask, 3))
    if not L: return
    L.append("\nArrows = board (~11 min left) → now (~9 min left). Results grade the board and this update separately.")
    notify(f"🔄 9-min update · closes {et(b)} ET · {nch} changed" + (f", {nflip} flipped" if nflip else ""), "\n".join(L), 2)


def board(L_, R, preds, b, closed=()):
    if not on("board"): return
    pv = R.get("proven", {}); L = []
    for c in [x for x in SHOW if x in preds]:
        p, mid, q, flow = preds[c]
        if not on("board", c): continue
        up = p >= 0.5; ps = p if up else 1 - p; ask = q["ask"] if up else 1 - q["bid"]; e = ps - ask - fee(min(max(ask, 0.01), 0.99))
        go = e >= EDGE and 0.03 < ask <= KMAX; d = "UP" if up else "DOWN"
        if q.get("tk"): L_.shown[q["tk"]] = dict(c=c, t1=q["t1"], p=round(p, 4), mid=round(mid, 4), go=bool(go), ask=round(ask, 3), left=round(q["tl"]))
        L.append((f"🟢 BET {c} {d} ≤ {cents(ask)}" if go else f"🔴 NO BET {c}") +
                 f" · settles {d}: model {ps:.0%} vs Kalshi {(mid if up else 1 - mid):.0%} · edge {e * 100:+.0f} pts after fees"
                 + ("" if not go else " · ✅ tested" if pv.get(c) else " · ⚠️ untested on this market")
                 + f" · last 15 {last_dot(L_, c)}" + (f" · leans today {t}" if (t := wl_txt(L_, c)) else ""))
        lw = q.get("low")
        if lw: L.append(f"   🚀 cheap {lw['side']} {cents(lw['ask'])}: {lw['p']:.0%} chance it trades {cents(lw['tgt'])}+ before close "
                        f"(normally {lw['base']:.0%}){' · BUY, sell at ' + cents(lw['tgt']) if lw['ok'] else ' · not worth it'}")
        L.append(f"   whales {flow}")
    rec = [x for x in L_.calls if x.get("won") is not None and x["t"] > time.time() - 86400]
    if rec: L.append(f"\nEdge calls 24h: {sum(x['won'] for x in rec)}/{len(rec)} won, {sum(x['pnl'] for x in rec) / max(sum(x['cost'] for x in rec), 1e-9):+.0%} ROI")
    off = [c for c in SHOW if not switches()["markets"].get(c, True)]
    if closed: L.append("Closed now: " + ", ".join(closed))
    if off: L.append("Switched off: " + ", ".join(off))
    if (t := wl_txt(L_)): L.append(f"\nBoard leans today: {t} · Bets today (🟢 BET only): {bets_txt(L_)}")
    L.append(f"\n🟢 = model beats Kalshi's ask by {EDGE * 100:.0f}+ pts after fees (≤{KMAX * 100:.0f}¢). % = chance it settles that way at the close. last 15 🟢/🔴 = last window's lean right/wrong (a lean is not a call; only 🟢 BET is).")
    if L: notify(f"📈 Commodities 15-min · closes {et(b)} ET", "\n".join(L), 2)


def live():
    t0, maxmin = time.time(), float(os.getenv("LIVE_MAX_MIN") or 1e9)
    meta = Meta(); st = load_json(f"{DATA}/state.json", {}); R = load_json(f"{DIR}/model.json", {})
    if not R.get("model") or time.time() - R.get("trained", 0) > 6 * 3600:
        harvest()
        for c in COMMS: kfetch(c, WEEKS_D if R.get("model") else MONTHS_D, 1 if R.get("model") else SAMPLE)
        R = train(push=False) or R
    L_ = Live(meta, st)
    warm = trades_since(t0 - 3900, 200)
    for r in warm: L_.tick(r[0], False); L_.ingest(r[0], *r[2:], alert=False)
    L_.quiet = max(st.get("last_ts", 0), warm[-1][0] if warm else 0)
    seen = set(r[1] for r in warm); last_ts = warm[-1][0] if warm else t0 - 60
    print(f"live: {len(warm)} commodity trades warmed · proven: {[c for c, v in R.get('proven', {}).items() if v] or 'none'}", flush=True)
    if not st.get("started"): notify("Kalshi commodity scanner online", "Reports only (no trading).\n" + (summary(R) if R.get("model") else "Model not built yet."), 3)
    low_sent, updated = set(), set()
    win, done_min, boarded, saved, trained, settled_t, digest_t = {}, {}, set(), time.time(), time.time(), 0, st.get("digest_t", 0)
    is_open = dict(st.get("is_open", {})); shut_t = {}; switches(force=True)
    while time.time() - t0 < maxmin * 60:
        loop0 = time.time()
        try:
            for r in trades_since(last_ts - 5):
                if r[1] in seen: continue
                seen.add(r[1]); last_ts = max(last_ts, r[0]); L_.ingest(r[0], *r[2:])
            if len(seen) > 200000: seen = set(list(seen)[-50000:])
            L_.tick(time.time()); now = time.time(); minute = int(now // 60); preds, upd = {}, {}
            for c in COMMS:  # 15-min windows: one prediction per completed minute
                if c not in win or ts_of(win[c]["close_time"]) <= now:
                    w = open_window(c); win[c] = w if w else {"close_time": datetime.fromtimestamp(now + 60, timezone.utc).isoformat()}
                    op = "ticker" in win[c]
                    if op: shut_t.pop(c, None)
                    else: shut_t.setdefault(c, now)
                    if not op and now - shut_t[c] < 1200: continue     # gaps between windows aren't closures: need 20 min with no window
                    if c in is_open and is_open[c] != op and on("open_close", c):  # market shut off / reopened
                        notify(f"{'🔔' if op else '🔕'} {c} 15-min market {'reopened' if op else 'closed'}",
                               f"{c} {'is trading again: predictions and calls resume.' if op else 'has no open 15-min window (daily break / weekend / halt). Predictions and calls paused until it reopens.'}", 2)
                    is_open[c] = op
                w = win[c]
                if "ticker" not in w or done_min.get(c) == minute or now % 60 < 4: continue
                done_min[c] = minute; out = live_pred(R, c, w)
                if not out: continue
                p, mid, q = out; tl, tk, flow = q["tl"], w["ticker"], L_.flow_txt(c)
                S = L_.snaps.setdefault(tk, {"c": c, "t1": q["t1"], "cp": {}})
                for b in CK:
                    if tl <= b and str(b) not in S["cp"] and tl > b - 2.5: S["cp"][str(b)] = [round(p, 4), round(mid, 4)]
                lw = low_live(R, c)
                if lw: q["low"] = lw
                if (lw and lw["ok"] and (R.get("low") or {}).get("proven", {}).get(c) and on("low_spikes", c)
                        and (tk, lw["up"]) not in low_sent):
                    low_sent.add((tk, lw["up"])); lb = (R["low"]["weeks"]["test_by"].get(c) or {})
                    notify(f"🚀 {c} cheap {lw['side']} {cents(lw['ask'])} · spike likely",
                           f"{lw['p']:.0%} chance it trades {cents(lw['tgt'])}+ before the {et(q['t1'])} close (normally {lw['base']:.0%}), {lw['tl']:.0f} min left\n"
                           f"Buy ≤ {cents(lw['ask'])}, sell into the spike at {cents(lw['tgt'])}. No spike → likely expires at 0¢.\n"
                           f"Expected +{lw['ev'] * 100:.0f}¢/contract after fees · backtest: {fmt_low(lb)}", 4, f"{WEB}/{K15[c].lower()}")
                q["tk"] = tk
                if 8 <= tl <= 11: preds[c] = (p, mid, q, flow)
                if 7.5 <= tl <= 9.5 and tk in L_.shown: upd[c] = (p, mid, q, flow)
                up = p >= 0.5; ps = p if up else 1 - p; ask = q["ask"] if up else 1 - q["bid"]; e = ps - ask - fee(min(max(ask, 0.01), 0.99))
                lr = [x for x in L_.calls if x["c"] == c and x.get("won") is not None][-30:]
                bad = len(lr) >= 20 and sum(x["pnl"] for x in lr) < -0.05 * sum(x["cost"] for x in lr)  # live results disproving it
                if (R.get("proven", {}).get(c) and not bad and on("edge_calls", c) and 3 <= tl <= 12 and e >= EDGE and 0.03 < ask <= KMAX
                        and not any(x["tk"] == tk for x in L_.calls)):
                    cost = ask + fee(ask); L_.calls.append(dict(t=now, c=c, tk=tk, up=bool(up), ask=ask, cost=cost, p=ps, won=None, pnl=0.0))
                    notify(f"🎯 {c} 15-min: {'YES (UP)' if up else 'NO (DOWN)'} ≤ {cents(ask)}",
                           f"Model {ps:.0%} vs Kalshi {(mid if up else 1 - mid):.0%} · edge {e * 100:+.0f} pts after fees · {tl:.0f} min left\n"
                           f"Closes {et(q['t1'])} ET · whales {flow}\nBacktest: {fmt_eval(R['weeks']['test_by'].get(c))}", 4, f"{WEB}/{K15[c].lower()}")
            b = int(now // 900 * 900) + 900
            if preds and b not in boarded: boarded.add(b); board(L_, R, preds, b, [c for c in SHOW if is_open.get(c) is False])
            if upd and b in boarded and b not in updated: updated.add(b); update9(L_, R, upd, b)
            if now - settled_t > 60: settle(L_); settled_t = now
            if now - trained > 6 * 3600:
                L_.flush()
                for c in COMMS: kfetch(c, 3)
                R = train() or R; trained = now
            if now - digest_t > 6 * 3600: digest(L_, R); digest_t = now
            if now - saved > 1800:
                L_.flush(); meta.save(); save_json(f"{DATA}/state.json", {**L_.state(), "started": True, "digest_t": digest_t, "is_open": is_open}); persist(); saved = now
        except Exception as ex:
            import traceback; traceback.print_exc(); print("loop error (continuing):", ex, flush=True); time.sleep(5)
        time.sleep(max(1.0, POLL - (time.time() - loop0)))
    L_.flush(); meta.save(); save_json(f"{DATA}/state.json", {**L_.state(), "started": True, "digest_t": digest_t, "is_open": is_open}); persist("kwhale: end of run")


def settle(L_):
    """Grade edge calls + checkpoint predictions once each 15-min window settles."""
    now = time.time(); log = []
    for tk, S in list(L_.snaps.items()):
        if now < S["t1"] + 60: continue
        if now > S["t1"] + 3600: L_.snaps.pop(tk); continue
        res = (get(f"/markets/{tk}").get("market") or {}).get("result")
        if res not in ("yes", "no"): continue
        up = res == "yes"
        for b, (p, mid) in S["cp"].items(): log.append(dict(t=S["t1"], c=S["c"], left=int(b), p=p, mid=mid, up=int(up)))
        sh = L_.shown.pop(tk, None)
        if sh:   # grade exactly what the board showed: its lean, and whether it said BET
            ok = int((sh["p"] >= 0.5) == up)
            bet = sh["go"] or sh.get("go9", False)                      # a BET shown on the board or the 9-min update
            bside = (sh["p"] if sh["go"] else sh.get("p9", sh["p"])) >= 0.5
            L_.wl.append([S["t1"], S["c"], ok, int((sh["mid"] >= 0.5) == up), int(bet), int(bside == up) if bet else None,
                          int((sh["p9"] >= 0.5) == up) if "p9" in sh else None])
            L_.res_pend.setdefault(str(int(S["t1"])), []).append(dict(sh, up=int(up)))
        for x in L_.calls:
            if x["tk"] == tk and x["won"] is None:
                x["won"] = int(x["up"] == up); x["pnl"] = round(x["won"] - x["cost"], 4)
                if not x["won"]: L_.missed.append(tk)
                if on("results", x["c"]): notify(f"{'✅' if x['won'] else '❌'} {x['c']} 15-min call {'won' if x['won'] else 'lost'}",
                       f"Called {'UP' if x['up'] else 'DOWN'} at {cents(x['ask'])}: settled {'UP' if up else 'DOWN'} · {x['pnl'] / x['cost']:+.0%} per $", 3)
        L_.snaps.pop(tk)
    for t1 in sorted(L_.res_pend):   # one results push per window, once every market in it is graded (or 10 min after close)
        if any(int(S["t1"]) == int(t1) for S in L_.snaps.values()) and now < int(t1) + 600: continue
        results(L_, int(t1), L_.res_pend.pop(t1))
    if log:
        os.makedirs(DATA, exist_ok=True); p = f"{DATA}/live_preds.csv.gz"
        pd.DataFrame(log).to_csv(p, mode="ab", index=False, header=not os.path.exists(p), compression="gzip")


def wl_txt(L_, c=None, since=None):
    """Board leans right / wrong (today in ET by default), with Kalshi's hit rate on the same windows."""
    since = since or datetime.now(ET).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    w = [x for x in L_.wl if x[0] > since and (c is None or x[1] == c)]
    if not w: return ""
    r = sum(x[2] for x in w); k = sum(x[3] for x in w)
    return f"{r}W-{len(w) - r}L ({r / len(w):.0%}) vs Kalshi {k / len(w):.0%}"


def u9_txt(L_):
    since = datetime.now(ET).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    w = [x for x in L_.wl if x[0] > since and len(x) > 6 and x[6] is not None]
    if not w: return ""
    r = sum(x[6] for x in w); return f"{r}W-{len(w) - r}L ({r / len(w):.0%})"


def bets_txt(L_, since=None):
    """Only the windows where the board said 🟢 BET."""
    since = since or datetime.now(ET).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
    b = [x for x in L_.wl if x[0] > since and len(x) > 4 and x[4]]
    if not b: return "none"
    r = sum(x[5] for x in b); return f"{r}W-{len(b) - r}L"


def last_dot(L_, c):
    """🟢 / 🔴: was the board's lean right in this market's last settled window (within 30 min)?"""
    w = [x for x in L_.wl if x[1] == c and x[0] > time.time() - 1800]
    return ("🟢" if w[-1][2] else "🔴") if w else "⚪"


def results(L_, t1, rows):
    if not on("pred_results"): return
    L = []
    for r in sorted(rows, key=lambda r: SHOW.index(r["c"]) if r["c"] in SHOW else 99):
        if not on("pred_results", r["c"]): continue
        up = r["p"] >= 0.5; d = "UP" if up else "DOWN"; ok = up == bool(r["up"]); end = "UP" if r["up"] else "DOWN"
        odds = f"{max(r['p'], 1 - r['p']):.0%} vs Kalshi {(r['mid'] if up else 1 - r['mid']):.0%}"
        if r.get("go"): L.append(f"{'🟢' if ok else '🔴'} {r['c']}: BET {d} ≤ {cents(r['ask'])} ({odds}) → settled {end} · bet {'WON' if ok else 'LOST'}")
        else: L.append(f"{'🟢' if ok else '🔴'} {r['c']}: NO BET · leaned {d} {odds} → settled {end} · lean {'right' if ok else 'wrong'}")
        if "p9" in r:
            u9 = r["p9"] >= 0.5; ok9 = u9 == bool(r["up"])
            if u9 != up or r.get("go9", False) != r.get("go", False):
                L[-1] += (f" · 9m update: {'BET' if r.get('go9') else 'lean'} {'UP' if u9 else 'DOWN'} {max(r['p9'], 1 - r['p9']):.0%}"
                          f" → {'right' if ok9 else 'wrong'}")
        L[-1] += f" · leans today {wl_txt(L_, r['c'])}"
    if not L: return
    n, k = sum(1 for x in L if x.startswith("🟢")), len(L)
    L += ["", f"Board leans today: {wl_txt(L_)} · Bets today (🟢 BET only): {bets_txt(L_)}",
          f"Leans last 7 days: {wl_txt(L_, since=time.time() - 7 * 86400)} · Bets: {bets_txt(L_, since=time.time() - 7 * 86400)}",
          (f"9-min updates today: {u9_txt(L_)} · " if u9_txt(L_) else "") +
          "Graded on exactly what the board showed (about 11 min before the close). A lean is the side the model thought more likely, "
          "not a call: only 🟢 BET rows are calls. 🟢/🔴 = right/wrong."]
    notify(f"🎯 Board results {et(t1 - 900)}–{et(t1)}: {n}/{k} leans right · bets {sum(1 for r in rows if r.get('go') or r.get('go9'))}",
           "\n".join(L), 2)


def digest(L_, R):
    if not on("digest"): L_.stats = dict(trades=0, whales=0, vol=0.0); return
    s = L_.stats; L = [f"{s['trades']:,} commodity trades · {s['whales']:,} whales · {money(s['vol'])} whale volume since last digest"]
    d = read_gz(f"{DATA}/live_preds.csv.gz")
    if len(d):
        d = d[d.t > time.time() - 86400]
        if len(d): L.append(f"Live 15-min predictions (24h, {len(d)} checkpoints): model right {((d.p >= 0.5) == (d.up == 1)).mean():.0%} vs Kalshi {((d.mid >= 0.5) == (d.up == 1)).mean():.0%}")
    rec = [x for x in L_.calls if x.get("won") is not None]
    if rec: L.append(f"Edge calls (14d): {sum(x['won'] for x in rec)}/{len(rec)} won, ROI {sum(x['pnl'] for x in rec) / sum(x['cost'] for x in rec):+.0%}")
    L += [f"{c}: whales {L_.flow_txt(c)}" for c in SHOW if L_.flow.get(c)]
    if R.get("model"): L += ["", summary(R)]
    notify("📊 Kalshi commodities digest", "\n".join(L), 2); L_.stats = dict(trades=0, whales=0, vol=0.0)


# ---------------- push + persist ----------------
_PUSHED = []


def notify(title, body, prio=3, click=None):
    print(f"\n=== {title}\n{body}", flush=True)
    t = os.getenv("KW_NTFY_TOPIC"); now = time.time(); _PUSHED[:] = [x for x in _PUSHED if x > now - 86400]
    if not t or (len(_PUSHED) >= E("KW_DAILY_PUSH", 230) and prio < 4): return
    j = {"topic": t, "title": title, "message": body[:3900], "priority": prio, **({"click": click} if click else {})}
    try: requests.post(os.getenv("KW_NTFY_SERVER", "https://ntfy.sh").rstrip("/") + "/", json=j, timeout=15).raise_for_status(); _PUSHED.append(now)
    except Exception as e: print("ntfy failed:", e, flush=True)


def persist(msg="kwhale: model"):
    if not os.getenv("GIT_PERSIST"): return
    br = os.getenv("GITHUB_REF_NAME", "main")
    subprocess.run(f'git add -A {DIR}; git diff --cached --quiet || git commit -qm "{msg}"; '
                   f'for i in 1 2 3 4; do git pull -q --rebase origin {br} && git push -q origin HEAD:{br} && break; sleep $((i*3)); done', shell=True)


# ---------------- commands ----------------
def build():
    """Combine everything: scanner's own commodity history + bot cache + fresh weeks/months pulls with order flow."""
    harvest(); end = time.time() + 60 * float(os.getenv("BUILD_FETCH_MIN", "120"))
    for i, c in enumerate(COMMS):                          # fair share of the remaining time per commodity
        kfetch(c, MONTHS_D, SAMPLE, deadline=time.time() + (end - time.time()) / (len(COMMS) - i))
    R = train(push=False)
    if R.get("model"): notify("🧠 Commodity model built", summary(R) + "\nFull table: kwhale/report.md", 3)
    persist("kwhale: commodity model build")


def doctor():
    """Delivery check for both bots' topics. Prints a fingerprint (not the name: logs are public) to compare with the app."""
    import hashlib
    srv = os.getenv("KW_NTFY_SERVER", "https://ntfy.sh").rstrip("/")
    for name in ("KW_NTFY_TOPIC", "NTFY_TOPIC"):
        t = os.getenv(name) or ""
        print(f"{name} set: {bool(t)} · length {len(t)} · uppercase: {any(c.isupper() for c in t)} · spaces: {t != t.strip()} · "
              f"fingerprint {hashlib.sha256(t.encode()).hexdigest()[:10]}")
        if not t: continue
        tag = f"doctor-{int(time.time())}"
        r = requests.post(srv + "/", json={"topic": t, "title": f"Delivery check ({name})", "message": f"If you see this, the app works. {tag}", "priority": 4}, timeout=15)
        print("  publish:", r.status_code); time.sleep(3)
        msgs = [json.loads(x) for x in requests.get(f"{srv}/{t}/json", params={"poll": 1, "since": "12h"}, timeout=15).text.splitlines() if x.strip()]
        print(f"  messages on topic (12h): {len(msgs)} · this check found: {any(tag in (m.get('message') or '') for m in msgs)}")


def selftest():
    """Offline: synthetic windows where Kalshi under-reacts to order flow -> the model must find it; live path parity."""
    global DIR, DATA, OLD_CACHE
    import tempfile; DIR = tempfile.mkdtemp(); DATA = f"{DIR}/data"; OLD_CACHE = DIR + "/old"; os.makedirs(DATA); os.makedirs(OLD_CACHE)
    rng = np.random.default_rng(3); now = time.time()
    for c in COMMS[:3]:
        rows = []
        for i in range(3000):
            t1 = int(now - i * 900 * 3 - 600) // 60 * 60; x = 0.0; tk = f"{K15[c]}-T{i}"; mids, fl = [], []
            for j in range(15):
                x += rng.normal(0, 0.35); f = rng.normal(0, 300); mids.append(x); fl.append(f)
            final = x + rng.normal(0, 0.35) + 0.0015 * sum(fl[:10])  # informed early order flow Kalshi's price hasn't absorbed
            for j, xm in enumerate(mids):
                m = float(sig(0.8 * xm)); rows.append(dict(ticker=tk, close=datetime.fromtimestamp(t1, timezone.utc).isoformat(), strike=1, up=int(final > 0),
                                                         ts=t1 - 900 + 60 * (j + 1), bid=round(m - 0.01, 2), ask=round(m + 0.01, 2), last=m, vol=float(rng.integers(0, 50)),
                                                         yf=max(fl[j], 0), nf=max(-fl[j], 0), bf=fl[j] if abs(fl[j]) > 100 else 0))
        d = pd.DataFrame(rows, columns=KCOLS); half = d.ticker.isin(d.ticker.unique()[::2])
        d[half].to_csv(kpath(c), index=False, compression="gzip")
        d[~half][KCOLS[:9]].to_csv(f"{OLD_CACHE}/k_{c}.csv.gz", index=False, compression="gzip")  # bot cache: no flow columns
    pd.DataFrame([dict(t=now - 5000, tk="KXWTID-26NOV04-T70", sd=1, usd=900, px=0.4, r15=0.02, r60=0.03),
                  dict(t=now - 5000, tk="KXNBAGAME-X", sd=1, usd=900, px=0.4, r15=0.02, r60=0.03)]).to_csv(f"{DATA}/whales_20261104.csv.gz", index=False, compression="gzip")
    harvest(); assert whale_stats().get("WTI", [0])[0] == 1, "harvest should keep only commodity whales"
    R = train(push=False); print(open(f"{DIR}/report.md").read()[:1800])
    assert R["weeks"]["test"]["ll_model"] < R["weeks"]["test"]["ll_kalshi"], "model failed to learn planted signal"
    D = kframe(load_k("WTI")); one = D[D.ticker == D.ticker.iloc[0]]
    raw = load_k("WTI"); raw = raw[raw.ticker == D.ticker.iloc[0]]
    assert np.allclose(p_of(R["model"], one), p_of(R["model"], kframe(raw))), "feature parity"
    # cheap-spike labels: YES at 10¢ whose bid later hits 25¢ is a hit (target 20¢); NO side at 1-bid is not cheap
    t1 = int(now) // 60 * 60; cl = datetime.fromtimestamp(t1, timezone.utc).isoformat()
    toy = pd.DataFrame([dict(ticker="KXGOLD15M-TOY", close=cl, strike=1, up=0, ts=t1 - 900 + 60 * (j + 1), bid=b, ask=b + 0.02, last=b, vol=5, yf=1, nf=1, bf=0)
                        for j, b in enumerate([0.08] * 5 + [0.25] + [0.05] * 9)], columns=KCOLS)
    lf = lframe(toy); first = lf[(lf.side == 1)].sort_values("ts").iloc[0]
    assert first.hit == 1 and abs(first.tgt - 0.20) < 1e-9 and first.pnl > 0, "cheap-spike label"
    assert (lf[lf.side == 1].sort_values("ts").iloc[-1].hit == 0), "no later spike = no hit"
    assert R.get("low", {}).get("weeks", {}).get("test", {}).get("rows", 0) > 0, "cheap-spike model trained"
    _ROWS["GOLD"] = toy.iloc[:4].to_dict("records"); lw = low_live(R, "GOLD"); assert lw and 0 < lw["p"] < 1, "cheap-spike live path"
    q = dict(bid=0.6, ask=0.62, tl=10, t1=now + 600, low=lw); board(Live(Meta(), {}), R, {"GOLD": (0.7, 0.61, q, "+$0")}, now + 600)
    print(summary(R)); print("selftest passed")


if __name__ == "__main__":
    a = sys.argv[1:] or ["live"]
    cmds = dict(live=live, build=build, train=lambda: (train(), persist("kwhale: retrain")), selftest=selftest, doctor=doctor,
                report=lambda: print(open(f"{DIR}/report.md").read() if os.path.exists(f"{DIR}/report.md") else "no report yet"),
                testnotify=lambda: notify("Kalshi scanner test", "KW_NTFY_TOPIC works. Separate from your commodity swing alerts.", 4))
    cmds.get(a[0], lambda: print(__doc__))()
