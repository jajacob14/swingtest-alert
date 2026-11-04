#!/usr/bin/env python3
"""Kalshi Whale Scanner + 15-minute outlook. REPORTS ONLY: never places orders, needs no Kalshi key.

Every ~8s it reads Kalshi's public trade feed and:
  🐋 whale alerts   big money (sliced orders merged into one), with how past whales like it did afterwards
  ⚡ spike alerts   fast price jumps, with how often that kind of spike kept going vs snapped back
  📈 15-min outlook at :00/:15/:30/:45: UP/DOWN odds for the most active markets for the next 15 min + trends
  📊 digest        every 6h: live accuracy, biggest misses, what the model learned
Every prediction is graded 15 min later and saved. Every 6h the model is retrained on the newest data (recent
rows and its own confident misses weigh more), trained on the older 70% and only marked PROVEN if it beats
both a coin flip and a simple momentum rule on the newest 30% it never saw.

Commands: live | backfill [days] | train | report | settle | testnotify | selftest
Env: KW_NTFY_TOPIC (own ntfy topic, separate from the commodity bot), KW_MIN_WHALE, KW_ALERT_WHALE, KW_POLL ...
"""
import glob, gzip, json, math, os, subprocess, sys, time
from collections import defaultdict, deque
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import numpy as np, pandas as pd, requests

for _k, _v in list(os.environ.items()):  # tolerate secrets pasted with stray spaces/newlines
    if _v != _v.strip(): os.environ[_k] = _v.strip()


def E(k, d): return type(d)(os.getenv(k) or d)


API = "https://api.elections.kalshi.com/trade-api/v2"
WEB = "https://kalshi.com/markets"
DIR = E("KW_DIR", "kwhale"); DATA = f"{DIR}/data"  # data/ = Actions cache (big, changes often); only model.json goes in git
MIN_WHALE = E("KW_MIN_WHALE", 1000.0)      # $ per merged order to count as a whale (logged + learned from)
ALERT_WHALE = E("KW_ALERT_WHALE", 5000.0)  # $ to push a phone alert
POLL = E("KW_POLL", 8)                     # seconds between feed polls
TOPN = E("KW_TOPN", 6)                     # predictions per 15-min outlook
CONF = E("KW_CONF", 0.60)                  # min UP/DOWN probability to list a market in the outlook
SPIKE_C = E("KW_SPIKE_C", 0.05)            # 5¢ in 2 min = spike
MOVE_C = 0.02                              # 15-min moves under 2¢ count as "flat"
CLUSTER_GAP = 30                           # same market + side within 30s = one sliced order
ACTIVE_MAX = E("KW_ACTIVE_MAX", 150)       # markets tracked per 15-min snapshot
SKIP = tuple(x for x in os.getenv("KW_SKIP", "KXMVE").split(",") if x)  # multi-leg parlays: illiquid, noisy
RPS = E("KW_RPS", 8.0)                     # Kalshi basic tier allows ~20 reads/s; stay well under
HOURLY_CAP = dict(whale=E("KW_WHALES_PER_H", 6), spike=E("KW_SPIKES_PER_H", 4))
DAILY_PUSH = E("KW_DAILY_PUSH", 200)       # ntfy.sh free tier caps messages/day; keep headroom
ET = ZoneInfo("America/New_York")
CATS = ("SPORTS", "CRYPTO", "MACRO", "POLITICS", "OTHER")
FEATS = ("mom15", "mom60", "wf15", "wf60", "ofi15", "burst", "pxc", "px2", "spread", "tleft") + tuple(f"c_{c}" for c in CATS)
COLS = dict(marks=["t", "tk", "cat", *FEATS, "m0", "m1", "dm", "p_up", "p_mv", "mv"],
            whales=["t", "tk", "cat", "sd", "usd", "n", "px", "rel", "pre", "tleft", "m0", "m1", "r15", "r60", "d15", "d60"],
            spikes=["t", "tk", "cat", "dir", "size", "m0", "m1", "m15", "usd2", "whale", "out"])


# ---------------- small utils ----------------
def ts_of(s): return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
def fnum(x, d=0.0):
    try: return float(x)
    except (TypeError, ValueError): return d
def sig(z): return 1 / (1 + np.exp(-np.clip(z, -30, 30)))
def fee(p): return math.ceil(7 * p * (1 - p) - 1e-9) / 100  # Kalshi taker fee per contract ($)
def slog(v): return math.copysign(math.log1p(abs(v) / 1000), v)
def et(t, f="%-I:%M%p"): return datetime.fromtimestamp(t, ET).strftime(f).lower().replace(":00", "")
def money(x): return f"${x:,.0f}"
def cents(p): return f"{p * 100:.0f}¢"
def slug(s): return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-").replace("--", "-")
def load_json(p, d):
    try: return json.load(open(p))
    except Exception: return d
def save_json(p, o):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=float); os.replace(tmp, p)
def cat_of(c):
    c = (c or "").lower()
    if "sport" in c: return "SPORTS"
    if "crypto" in c: return "CRYPTO"
    if any(k in c for k in ("econ", "financ", "compan", "rate", "inflation")): return "MACRO"
    if any(k in c for k in ("polit", "elect", "world", "gov")): return "POLITICS"
    return "OTHER"
def left_txt(sec):
    if sec <= 0: return "closed"
    return f"{sec / 60:.0f}m" if sec < 5400 else (f"{sec / 3600:.0f}h" if sec < 172800 else f"{sec / 86400:.0f}d")


# ---------------- Kalshi public API (rate limited, retried) ----------------
SES = requests.Session(); SES.headers["User-Agent"] = "kalshi-whale-scanner/1.0"
_LAST = [0.0]


def get(path, **params):
    for i in range(5):
        w = 1 / RPS - (time.time() - _LAST[0])
        if w > 0: time.sleep(w)
        _LAST[0] = time.time()
        try:
            r = SES.get(API + path, params=params, timeout=20)
            if r.status_code == 429: time.sleep(2 ** i); continue
            if r.status_code == 404: return {}
            r.raise_for_status(); return r.json()
        except (requests.RequestException, ValueError) as e:
            if i == 4: print("GET failed", path, e, flush=True); return {}
            time.sleep(2 ** i)
    return {}


def parse(t):
    """Trade -> (ts, id, ticker, side +1 YES / -1 NO, yes_price 0-1, contracts, $ paid by taker). Fixed-point fields first."""
    yp = fnum(t.get("yes_price_dollars"), None)
    if yp is None: yp = fnum(t.get("yes_price")) / 100
    npx = fnum(t.get("no_price_dollars"), None)
    if npx is None: npx = 1 - yp
    n = fnum(t.get("count_fp"), None)
    if n is None: n = fnum(t.get("count"))
    sd = 1 if (t.get("taker_side") or "").lower() == "yes" else -1
    return ts_of(t["created_time"]), t.get("trade_id", ""), t.get("ticker", ""), sd, yp, n, n * (yp if sd > 0 else npx)


def trades_between(t0, t1=None, max_pages=60):
    """Trades with ts >= t0 (and < t1), oldest first. Kalshi pages newest-first by cursor."""
    out, cur = [], None
    for _ in range(max_pages):
        q = {"limit": 1000, "min_ts": int(t0), **({"max_ts": int(t1)} if t1 else {}), **({"cursor": cur} if cur else {})}
        j = get("/markets/trades", **q); tr = j.get("trades") or []
        for x in tr:
            try: out.append(parse(x))
            except Exception: pass
        cur = j.get("cursor")
        if not cur or not tr: break
    out.sort(key=lambda r: r[0])
    return out


class Meta:
    """ticker -> title / category / close time / link (+ result once settled). Cached on disk."""
    def __init__(self):
        self.m = load_json(f"{DATA}/meta.json", {}); self.ev, self.se, self.bad = {}, {}, set()

    def get(self, tk, fresh=False):
        m = self.m.get(tk)
        if (m and not fresh) or (tk in self.bad and not m): return m
        mk = get(f"/markets/{tk}").get("market")
        if not mk: self.bad.add(tk); return m
        e = mk.get("event_ticker", ""); ev = self.ev.get(e)
        if ev is None: ev = self.ev[e] = get(f"/events/{e}").get("event") or {}
        s = ev.get("series_ticker") or e.split("-")[0]; se = self.se.get(s)
        if se is None: se = self.se[s] = get(f"/series/{s}").get("series") or {}
        title = mk.get("title") or tk; sub = mk.get("yes_sub_title") or ""
        if sub and sub.lower() not in title.lower(): title = f"{title} [{sub}]"
        link = f"{WEB}/{s.lower()}/{slug(se['title'])}/{e.lower()}" if se.get("title") else f"{WEB}/{s.lower()}"
        m = self.m[tk] = dict(title=title[:90], cat=cat_of(ev.get("category") or se.get("category")), link=link,
                              close=ts_of(mk["close_time"]) if mk.get("close_time") else 0, result=mk.get("result") or "")
        return m

    def save(self):
        now = time.time()
        self.m = {k: v for k, v in self.m.items() if v and (not v.get("close") or v["close"] > now - 7 * 86400)}
        save_json(f"{DATA}/meta.json", self.m)


# ---------------- per-market live state ----------------
class Tk:
    __slots__ = ("tr", "mids", "bid", "bid_t", "ask", "ask_t", "last", "cl", "wh", "spike_t", "chk")

    def __init__(self):
        self.tr, self.mids, self.wh = deque(), deque(), deque()
        self.bid = self.ask = self.last = None; self.bid_t = self.ask_t = 0; self.cl = {}; self.spike_t = self.chk = 0

    def fresh(self, now): return self.bid is not None and self.ask is not None and now - self.bid_t < 600 and now - self.ask_t < 600 and self.ask >= self.bid

    def mid(self, now):
        """YES-taker prints hit the ask, NO-taker prints hit the bid -> live quote midpoint (else last price)."""
        return (self.bid + self.ask) / 2 if self.fresh(now) else self.last

    def spread(self, now): return (self.ask - self.bid) if self.fresh(now) else 0.06

    def mid_at(self, t):
        for ts, m in reversed(self.mids):
            if ts <= t: return m
        return self.mids[0][1] if self.mids else None


class Engine:
    """Same code path live and in backfill replay, so training data matches what the live bot sees."""
    def __init__(self, meta, st=None, live=False, notify=None):
        st = st or {}
        self.meta, self.live, self.push = meta, live, notify or (lambda *a, **k: None)
        self.T = defaultdict(Tk); self.now = 0.0; self.open_cl = set()
        self.pend_m, self.pend_w, self.pend_s = st.get("pend_m", []), st.get("pend_w", []), st.get("pend_s", [])
        self.last_mark = st.get("last_mark", 0); self.quiet_until = st.get("last_ts", 0)
        self.flow = st.get("flow", {})        # ticker -> {hour: net whale $ (+YES / -NO)}  (24h trends)
        self.unw = st.get("unw", {})          # cat -> [whales, opposite-whale unwinds, minutes sum, gain sum]
        self.recent = st.get("recent", {})    # ticker -> [[t, sd, usd, px]] whales of last 3h (cash-out detection)
        self.livebook = st.get("live", [])    # graded live calls [t, ok, cat, conf]
        self.unsettled = st.get("unsettled", {})
        self.lastcalls = st.get("lastcalls", [])
        self.stats = st.get("stats", dict(trades=0, whales=0, vol=0.0)); self.model = load_json(f"{DIR}/model.json", {})
        self.rows = defaultdict(list); self.hour_sent = defaultdict(int); self.skipped = defaultdict(int)
        self.cool = {}; self.lag = 20 if live else 0; self.graded = 0

    # ----- ingest -----
    def ingest(self, ts, tk, sd, yp, n, usd):
        self.now = max(self.now, ts); self.stats["trades"] += 1
        k = self.T[tk]; m_prev = k.mid(ts)
        if sd > 0: k.ask, k.ask_t = yp, ts
        else: k.bid, k.bid_t = yp, ts
        k.last = yp; m = k.mid(ts)
        k.mids.append((ts, m)); k.tr.append((ts, sd, usd))
        while k.tr and k.tr[0][0] < ts - 3900: k.tr.popleft()
        while len(k.mids) > 1 and k.mids[1][0] < ts - 3900: k.mids.popleft()
        c = k.cl.get(sd)
        if c and ts - c[1] <= CLUSTER_GAP:
            c[1] = ts; c[2] += usd; c[3] += 1; c[4] += n
        else:
            if c: self._close(tk, sd, c)
            k.cl[sd] = [ts, ts, usd, 1, n, m_prev if m_prev is not None else m]; self.open_cl.add(tk)
        if ts - k.spike_t > 900 and ts - k.chk >= 5 and k.fresh(ts) and not tk.startswith(SKIP):
            k.chk = ts; m0 = k.mid_at(ts - 120)
            if m0 is not None and abs(m - m0) >= SPIKE_C:
                rec = [x for x in k.tr if x[0] >= ts - 120]
                if len(rec) >= 4 and sum(x[2] for x in rec) >= 500:
                    k.spike_t = ts; self._spike(tk, k, ts, m0, m, rec)

    # ----- clock -----
    def tick(self, now):
        self.now = max(self.now, now)
        for tk in list(self.open_cl):
            k = self.T.get(tk)
            if not k: self.open_cl.discard(tk); continue
            for sd, c in list(k.cl.items()):
                if now - c[1] > CLUSTER_GAP: self._close(tk, sd, c); k.cl.pop(sd)
            if not k.cl: self.open_cl.discard(tk)
        b = int(now // 900 * 900)
        if b > self.last_mark and now >= b + self.lag:
            self.last_mark = b; self._grade(now); self._marker(b); self._prune(now)
        elif now - self.graded >= 30: self._grade(now)

    def _prune(self, now):
        for tk in [t for t, k in self.T.items() if not k.tr and not k.cl and (not k.mids or k.mids[-1][0] < now - 7200)]:
            self.T.pop(tk, None)
        hcut = int(now // 3600) - 24
        self.flow = {tk: {h: v for h, v in f.items() if int(h) > hcut} for tk, f in self.flow.items()}
        self.flow = {tk: f for tk, f in self.flow.items() if f}
        self.recent = {tk: [w for w in ws if w[0] > now - 10800] for tk, ws in self.recent.items()}
        self.recent = {tk: ws for tk, ws in self.recent.items() if ws}
        self.livebook = [x for x in self.livebook if x[0] > now - 7 * 86400]

    # ----- whales -----
    def _close(self, tk, sd, c):
        t0, t1, usd, n_prints, contracts, m_before = c
        if usd < MIN_WHALE or t0 <= self.quiet_until or tk.startswith(SKIP): return
        k = self.T[tk]; px = usd / max(contracts, 1e-9); m_after = k.mid(t1)
        meta = self.meta.get(tk) or {}; cat = meta.get("cat", "OTHER"); close = meta.get("close", 0)
        flow15 = sum(x[2] for x in k.tr if t0 - 900 <= x[0] < t0)
        pre = ((k.mid_at(t0 - 1) or m_before) - (k.mid_at(t0 - 600) or m_before)) * sd
        self.stats["whales"] += 1; self.stats["vol"] += usd
        k.wh.append((t1, sd, usd))
        while k.wh and k.wh[0][0] < t1 - 3900: k.wh.popleft()
        h = str(int(t1 // 3600)); f = self.flow.setdefault(tk, {}); f[h] = f.get(h, 0) + sd * usd
        u = self.unw.setdefault(cat, [0, 0, 0.0, 0.0]); u[0] += 1
        for w in self.recent.get(tk, []):  # an opposite-side whale after a whale = likely cash-out / unwind
            if w[1] == -sd and len(w) == 4 and usd >= 0.5 * w[2]:
                gain = (1 - px) - w[3]  # first whale's side now worth ~ 1 - price paid by the opposite whale
                u[1] += 1; u[2] += (t0 - w[0]) / 60; u[3] += gain; w.append(1)
        self.recent.setdefault(tk, []).append([t0, sd, usd, px])
        if close: self.unsettled[tk] = close
        ev = dict(t=t0, tk=tk, cat=cat, sd=sd, usd=round(usd, 2), n=n_prints, px=round(px, 4), rel=round(usd / (flow15 + 200), 3),
                  pre=round(pre, 4), tleft=round(math.log1p(max(close - t0, 0) / 3600), 3) if close else 3.0,
                  m0=m_before, m1=m_after)
        self.pend_w.append(ev)
        line = f"WHALE {money(usd):>9} {'YES' if sd > 0 else 'NO ':<3} @{cents(px):>4} x{n_prints:<3} {meta.get('title', tk)[:60]}"
        if self.live: print(line, flush=True)
        if self.live and usd >= ALERT_WHALE: self._whale_alert(tk, k, ev, meta)

    def _whale_alert(self, tk, k, ev, meta):
        if not self._allow("whale", tk, 600): return
        side = "YES" if ev["sd"] > 0 else "NO"; cat = ev["cat"]
        L = [meta.get("title", tk), f"{side} @ {cents(ev['px'])} · {ev['n']} prints merged · {ev['rel']:.1f}× this market's last-15m flow"]
        if ev["pre"] * 100 >= 3: L.append(f"Chasing: price already moved {ev['pre'] * 100:+.0f}¢ their way in the last 10m")
        elif ev["pre"] * 100 <= -3: L.append(f"Against the move: price went {ev['pre'] * 100:+.0f}¢ against them in the last 10m")
        cell = (self.model.get("cells") or {}).get(f"{cat}|{min(int(ev['px'] * 5), 4)}")
        if cell and cell["n"] >= 20:
            s = f"Past {cat} whales at {cell['band']}: {cell['r15']:+.1f}¢ after 15m, {cell['r60']:+.1f}¢ after 1h (n={cell['n']})"
            if cell.get("sn", 0) >= 20: s += f"; won {cell['win']:.0%} vs {cell['px']:.0%} paid ({cell['edge'] * 100:+.1f} pts after fees)"
            L.append(s)
        u = self.unw.get(cat)
        if u and u[0] >= 30 and u[1]:
            L.append(f"{u[1] / u[0]:.0%} of {cat} whales see an opposite whale (likely cash-out) ~{u[2] / u[1]:.0f}m later, avg {u[3] / u[1] * 100:+.1f}¢")
        o = self.outlook_now(tk, k, meta)
        if o: L.append(o)
        if meta.get("close"): L.append(f"Closes in {left_txt(meta['close'] - ev['t'])}")
        self.push(f"🐋 {money(ev['usd'])} {side} whale", "\n".join(L), 4 if ev["usd"] >= 4 * ALERT_WHALE else 3, meta.get("link"), "whale")

    # ----- spikes -----
    def _spike(self, tk, k, ts, m0, m1, rec):
        if ts <= self.quiet_until: return
        meta = self.meta.get(tk) or {}; cat = meta.get("cat", "OTHER"); d = 1 if m1 > m0 else -1
        wsum = sum(w[2] for w in k.wh if w[0] >= ts - 180 and w[1] == d)
        usd2 = sum(x[2] for x in rec)
        self.pend_s.append(dict(t=ts, tk=tk, cat=cat, dir=d, size=round(abs(m1 - m0), 4), m0=m0, m1=m1, usd2=round(usd2, 2), whale=int(wsum >= MIN_WHALE)))
        if not self.live or not self._allow("spike", tk, 900): return
        L = [meta.get("title", tk), f"YES {cents(m0)} → {cents(m1)} in 2m · {money(usd2)} traded · {'whale-driven' if wsum >= MIN_WHALE else 'no whale behind it'}"]
        sp = (self.model.get("spikes") or {}).get(cat)
        if sp and sp["n"] >= 20: L.append(f"Past {cat} spikes: kept going {sp['cont']:.0%} · snapped back {sp['rev']:.0%} next 15m (n={sp['n']})")
        o = self.outlook_now(tk, k, meta)
        if o: L.append(o)
        self.push(f"⚡ SPIKE {'UP' if d > 0 else 'DOWN'} {abs(m1 - m0) * 100:.0f}¢", "\n".join(L), 4, meta.get("link"), "zap")

    def _allow(self, kind, tk, cool):
        hr = int(self.now // 3600)
        if self.now - self.cool.get((kind, tk), 0) < cool: return False
        if self.hour_sent[(kind, hr)] >= HOURLY_CAP[kind]: self.skipped[kind] += 1; return False
        self.cool[(kind, tk)] = self.now; self.hour_sent[(kind, hr)] += 1; return True

    # ----- 15-min snapshots -----
    def feats(self, k, b, meta):
        m = k.mid_at(b); m15 = k.mid_at(b - 900); m60 = k.mid_at(b - 3600)
        m15 = m if m15 is None else m15; m60 = m15 if m60 is None else m60
        ofi = tot = 0.0; n15 = n60 = 0
        for ts, sd, usd in k.tr:
            if ts > b or ts <= b - 3600: continue
            n60 += 1
            if ts > b - 900: n15 += 1; ofi += sd * usd; tot += usd
        wf15 = sum(sd * u for ts, sd, u in k.wh if b - 900 < ts <= b); wf60 = sum(sd * u for ts, sd, u in k.wh if b - 3600 < ts <= b)
        close = meta.get("close", 0) if meta else 0; cat = meta.get("cat", "OTHER") if meta else "OTHER"
        x = [m - m15, m15 - m60, slog(wf15), slog(wf60), ofi / (tot + 1), math.log((n15 + 1) / (n60 / 4 + 1)), m - 0.5, (m - 0.5) ** 2,
             k.spread(b), math.log1p(max(close - b, 0) / 3600) if close else 3.0] + [1.0 if cat == c else 0.0 for c in CATS]
        return [round(v, 5) for v in x], m, n60

    def predict(self, x):
        """-> (P(YES price higher in 15m | it moves 2¢+), P(moves 2¢+)) or (None, None) before the first model."""
        M = self.model
        if not M.get("dr"): return None, None
        def pr(mm):
            z = (np.asarray(x) - np.asarray(mm["mu"])) / np.asarray(mm["sd"]); return float(sig(mm["w"][0] + z @ np.asarray(mm["w"][1:])))
        return pr(M["dr"]), pr(M["mv"])

    def outlook_now(self, tk, k, meta):
        x, m, _ = self.feats(k, self.now, meta); pu, pm = self.predict(x)
        if pu is None: return None
        tag = "" if self.model.get("ok") else " (model still unproven)"
        return f"15-min outlook: {'UP' if pu >= 0.5 else 'DOWN'} {max(pu, 1 - pu):.0%} if it moves · move chance {pm:.0%}{tag}"

    def _marker(self, b):
        cand = []
        for tk, k in self.T.items():
            if tk.startswith(SKIP) or not k.mids: continue
            n60 = sum(1 for x in k.tr if b - 3600 < x[0] <= b); w60 = sum(u for ts, _, u in k.wh if ts > b - 3600)
            if n60 < 5 and w60 < MIN_WHALE: continue
            m = k.mid_at(b)
            if m is None or not 0.03 <= m <= 0.97 or k.spread(b) > 0.10: continue
            cand.append((n60 + w60 / 500, tk))
        preds = []
        for _, tk in sorted(cand, reverse=True)[:ACTIVE_MAX]:
            meta = self.meta.get(tk) or {}
            if meta.get("close") and meta["close"] < b + 900: continue
            k = self.T[tk]; x, m, n60 = self.feats(k, b, meta); pu, pm = self.predict(x)
            self.pend_m.append([b, tk, meta.get("cat", "OTHER"), x, m, pu, pm])
            preds.append(dict(tk=tk, x=x, m=m, pu=pu, pm=pm, meta=meta, n60=n60))
        if self.live: self._report(b, preds)

    def _report(self, b, preds):
        M = self.model; ok = bool(M.get("ok")); thr = CONF + (0.05 if self.probation() else 0)
        L = []
        last = [c for c in self.lastcalls if c[0] == b - 900]
        if last:
            r, w = sum(c[1] == 1 for c in last), sum(c[1] == 0 for c in last)
            L.append(f"Last 15m calls: {r} right, {w} wrong, {len(last) - r - w} flat")
        lb = [x for x in self.livebook if x[0] > b - 86400]
        if len(lb) >= 10: L.append(f"24h live record: {np.mean([x[1] for x in lb]):.0%} right ({len(lb)} calls)")
        if M.get("test"): L.append(f"Model test: {M['test']['acc_conf']:.0%} vs momentum {M['test']['mom_conf']:.0%} ({'PROVEN' if ok else 'not proven yet'})"
                                   + (" · on probation: stricter" if self.probation() else ""))
        calls = []
        if M.get("dr"):
            for p in preds:
                c = max(p["pu"], 1 - p["pu"])
                if c >= thr and p["pm"] >= 0.25: calls.append((c * p["pm"], p))
            calls = [p for _, p in sorted(calls, key=lambda z: -z[0])[:TOPN]]
        self.lastcalls = [[b, None, p["tk"], p["pu"]] for p in calls]
        if calls:
            L.append("")
            for p in calls:
                up = p["pu"] >= 0.5; mt = p["meta"]
                L.append(f"{'🟢 UP' if up else '🔴 DOWN'} {max(p['pu'], 1 - p['pu']):.0%} · move {p['pm']:.0%} · YES {cents(p['m'])} · {mt.get('title', p['tk'])[:55]}"
                         f" ({mt.get('cat', '?')}, closes {left_txt(mt.get('close', 0) - b) if mt.get('close') else '?'})")
                if mt.get("link"): L.append("   " + mt["link"])
        elif not M.get("dr"):
            need = max(0, 600 - M.get("rows", 0))
            L.append(f"Learning: collecting graded snapshots before predicting ({need} more needed)." if need else "Learning: first model trains at the next 6h retrain.")
        tr = self.trends(b)
        if tr: L += ["", "Trends (24h whale flow):"] + tr
        if self.skipped:
            L.append("Muted alerts last hour (caps): " + ", ".join(f"{v} {k}" for k, v in self.skipped.items())); self.skipped.clear()
        if not calls and not tr: return
        self.push(f"📈 Kalshi 15-min outlook {et(b)}–{et(b + 900)} ET", "\n".join(L), 3, None, "chart_with_upwards_trend")

    def trends(self, b, n=4):
        out = []
        for tk, f in self.flow.items():
            net = sum(f.values()); k = self.T.get(tk)
            if abs(net) < 5 * MIN_WHALE or not k or not k.mids or k.mids[-1][0] < b - 3600: continue
            m, m60 = k.mid_at(b), k.mid_at(b - 3600)
            if not 0.03 <= m <= 0.97: continue
            out.append((abs(net), tk, net, m, (m - m60) if m60 is not None else 0))
        L = []
        for _, tk, net, m, d1 in sorted(out, reverse=True)[:n]:
            mt = self.meta.get(tk) or {}
            lag = "price flat: flow not priced in yet" if abs(d1) < 0.01 else ("price moving AGAINST the flow" if net * d1 < 0 else "price following")
            L.append(f"{'🟢' if net > 0 else '🔴'} {money(abs(net))} net {'YES' if net > 0 else 'NO'} · YES {cents(m)} ({d1 * 100:+.0f}¢ 1h, {lag}) · {mt.get('title', tk)[:50]}")
        return L

    def probation(self):
        lb = [x[1] for x in self.livebook if x[0] > self.now - 3 * 86400]
        return len(lb) >= 60 and np.mean(lb) < 0.52

    # ----- grading (learning labels) -----
    def _m(self, tk, t, fb):
        k = self.T.get(tk); m = k.mid_at(t) if k and k.mids else None
        return fb if m is None else m

    def _grade(self, now):
        self.graded = now; due = now - self.lag
        keep = []
        for r in self.pend_m:
            b, tk, cat, x, m0, pu, pm = r
            if b + 900 > due: keep.append(r); continue
            if b + 900 < due - 3600: continue
            m1 = self._m(tk, b + 900, m0); dm = m1 - m0; mv = int(abs(dm) >= MOVE_C)
            self.rows["marks"].append([b, tk, cat, *x, m0, m1, round(dm, 4), pu, pm, mv])
            for c in self.lastcalls:
                if c[0] == b and c[2] == tk and c[1] is None:
                    c[1] = int((dm > 0) == (pu >= 0.5)) if mv else -1  # 1 right, 0 wrong, -1 stayed flat
                    if mv: self.livebook.append([b, c[1], cat, round(max(pu, 1 - pu), 3), tk])
        self.pend_m = keep
        keep = []
        for e in self.pend_w:
            if e["t"] + 3600 > due: keep.append(e); continue
            if e["t"] + 3600 < due - 3600: continue
            s = lambda m: m if e["sd"] > 0 else 1 - m
            m15, m60 = self._m(e["tk"], e["t"] + 900, e["m1"]), self._m(e["tk"], e["t"] + 3600, e["m1"])
            r15, r60 = s(m15) - e["px"], s(m60) - e["px"]; d15, d60 = (m15 - e["m1"]) * e["sd"], (m60 - e["m1"]) * e["sd"]
            self.rows["whales"].append([e["t"], e["tk"], e["cat"], e["sd"], e["usd"], e["n"], e["px"], e["rel"], e["pre"], e["tleft"],
                                        e["m0"], e["m1"], round(r15, 4), round(r60, 4), round(d15, 4), round(d60, 4)])
        self.pend_w = keep
        keep = []
        for s_ in self.pend_s:
            if s_["t"] + 900 > due: keep.append(s_); continue
            if s_["t"] + 900 < due - 3600: continue
            m15 = self._m(s_["tk"], s_["t"] + 900, s_["m1"]); g = (m15 - s_["m1"]) * s_["dir"]
            out = "cont" if g >= 0.01 else ("rev" if g <= -0.01 else "flat")
            self.rows["spikes"].append([s_["t"], s_["tk"], s_["cat"], s_["dir"], s_["size"], s_["m0"], s_["m1"], m15, s_["usd2"], s_["whale"], out])
        self.pend_s = keep

    def flush(self):
        day = datetime.now(timezone.utc).strftime("%Y%m%d") if self.live else datetime.fromtimestamp(self.now or time.time(), timezone.utc).strftime("%Y%m%d")
        os.makedirs(DATA, exist_ok=True)
        for kind, rows in self.rows.items():
            if not rows: continue
            p = f"{DATA}/{kind}_{day}.csv.gz"; new = not os.path.exists(p)
            pd.DataFrame(rows, columns=COLS[kind]).to_csv(p, mode="ab", index=False, header=new, compression="gzip")
        self.rows.clear()

    def state(self):
        return dict(pend_m=self.pend_m, pend_w=self.pend_w, pend_s=self.pend_s, last_mark=self.last_mark, last_ts=self.now,
                    flow=self.flow, unw=self.unw, recent=self.recent, live=self.livebook, unsettled=self.unsettled,
                    lastcalls=self.lastcalls, stats=self.stats)


# ---------------- learning ----------------
def read_rows(kind, days=30):
    fs = sorted(glob.glob(f"{DATA}/{kind}_*.csv.gz"))[-days - 1:]
    ds = []
    for f in fs:
        try: ds.append(pd.read_csv(f))
        except Exception as e: print("read", f, e)
    if not ds: return pd.DataFrame(columns=COLS[kind])
    d = pd.concat(ds, ignore_index=True)
    return d[d.t >= time.time() - days * 86400] if len(d) and d.t.max() > time.time() - 2 * 86400 else d


def fit_logit(X, y, w8, lam=0.01, iters=700, lr=0.5):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1]); w8 = w8 / w8.sum()
    for _ in range(iters):
        p = sig(Xb @ w); w -= lr * (Xb.T @ ((p - y) * w8) + lam * np.r_[0, w[1:]])
    return w


def fit(X, y, w8):
    mu, sd = X.mean(0), X.std(0) + 1e-6
    return dict(w=[round(float(v), 5) for v in fit_logit((X - mu) / sd, y, w8)], mu=[round(float(v), 6) for v in mu], sd=[round(float(v), 6) for v in sd])


def apply(mm, X): return sig(mm["w"][0] + ((X - np.asarray(mm["mu"])) / np.asarray(mm["sd"])) @ np.asarray(mm["w"][1:]))


def weights(d):
    """Newer rows count more (7-day half-life); rows the deployed model got confidently wrong count 1.5x."""
    w = 0.5 ** ((d.t.max() - d.t) / (7 * 86400))
    if "p_up" in d:
        pu = d.p_up.astype(float)
        wrong = pu.notna() & (abs(pu - 0.5) >= 0.1) & (d.mv == 1) & ((d.dm > 0) != (pu >= 0.5))
        w = w * np.where(wrong, 1.5, 1.0)
    return np.asarray(w, float)


def train(quiet=False):
    d = read_rows("marks").dropna(subset=list(FEATS) + ["dm"]).sort_values("t")
    old = load_json(f"{DIR}/model.json", {}); M = dict(rows=int(len(d)), trained=int(time.time()))
    M["cells"], M["spikes"] = whale_cells(), spike_table()
    if len(d) < 600:
        M.update({k: old[k] for k in ("dr", "mv", "test", "ok") if k in old}); save_json(f"{DIR}/model.json", M)
        print(f"train: only {len(d)} graded snapshots (need 600)"); return M
    cut = d.t.quantile(0.7); tr, te = d[d.t < cut], d[d.t >= cut + 900]  # +15m purge gap: no overlapping labels
    X, Xt = tr[list(FEATS)].to_numpy(float), te[list(FEATS)].to_numpy(float)
    mv_m = fit(X, tr.mv.to_numpy(float), weights(tr))
    trm = tr[tr.mv == 1]; dr_m = fit(trm[list(FEATS)].to_numpy(float), (trm.dm > 0).to_numpy(float), weights(trm))
    tem = te[te.mv == 1]; pu = apply(dr_m, tem[list(FEATS)].to_numpy(float)); up = (tem.dm > 0).to_numpy()
    conf = np.abs(pu - 0.5) >= CONF - 0.5; mom = tem.mom15.to_numpy()
    acc = float(((pu >= 0.5) == up).mean()) if len(tem) else 0
    acc_c = float(((pu >= 0.5) == up)[conf].mean()) if conf.sum() else 0
    mc = conf & (mom != 0); mom_c = float(((mom > 0) == up)[mc].mean()) if mc.sum() >= 20 else 0.5
    pm = apply(mv_m, Xt); base = te.mv.mean()
    by = {}
    for c in CATS:
        s = conf & (tem[f"c_{c}"].to_numpy() == 1)
        if s.sum() >= 20: by[c] = dict(n=int(s.sum()), acc=round(float(((pu >= 0.5) == up)[s].mean()), 3))
    T = dict(n=int(len(te)), n_moved=int(len(tem)), acc=round(acc, 3), n_conf=int(conf.sum()), acc_conf=round(acc_c, 3), mom_conf=round(mom_c, 3),
             brier_mv=round(float(((pm - te.mv) ** 2).mean()), 4), brier_base=round(float(((base - te.mv) ** 2).mean()), 4), by_cat=by)
    ok = T["n_conf"] >= 100 and acc_c >= 0.56 and acc_c >= mom_c + 0.02
    W = weights(d); dm_ = d[d.mv == 1]
    M.update(test=T, ok=bool(ok), mv=fit(d[list(FEATS)].to_numpy(float), d.mv.to_numpy(float), W),
             dr=fit(dm_[list(FEATS)].to_numpy(float), (dm_.dm > 0).to_numpy(float), weights(dm_)))
    M["top_feats"] = sorted(((FEATS[i], M["dr"]["w"][i + 1]) for i in range(len(FEATS))), key=lambda z: -abs(z[1]))[:4]
    save_json(f"{DIR}/model.json", M)
    msg = (f"Model retrained on {len(d)} graded 15-min snapshots. Unseen-data test: {acc_c:.0%} right on confident calls "
           f"(n={T['n_conf']}) vs momentum rule {mom_c:.0%}, all moved {acc:.0%}. Status: {'PROVEN ✅' if ok else 'NOT proven yet (reports say so)'}\n"
           f"Strongest signals: " + ", ".join(f"{k} {'+' if v > 0 else '−'}" for k, v in M["top_feats"]))
    if by: msg += "\nBy category: " + ", ".join(f"{c} {v['acc']:.0%} ({v['n']})" for c, v in by.items())
    print(msg, flush=True)
    if not quiet and "ok" in old and old["ok"] != M["ok"]: notify("🧠 Kalshi model " + ("PROVEN" if ok else "lost its edge: predictions marked unproven"), msg)
    return M


def whale_cells():
    w = read_rows("whales"); res = load_json(f"{DATA}/results.json", {})
    if not len(w): return {}
    w["pb"] = np.minimum((w.px * 5).astype(int), 4)
    r = w.tk.map(res); w["won"] = np.where(r.isin(["yes", "no"]), ((r == "yes") == (w.sd > 0)).astype(float), np.nan)
    out = {}
    for (c, b), g in w.groupby(["cat", "pb"]):
        s = g.dropna(subset=["won"])
        out[f"{c}|{b}"] = dict(band=f"{b * 20}-{b * 20 + 20}¢", n=int(len(g)), r15=round(float(g.r15.mean() * 100), 2), r60=round(float(g.r60.mean() * 100), 2),
                               sn=int(len(s)), win=round(float(s.won.mean()), 3) if len(s) else None, px=round(float(s.px.mean()), 3) if len(s) else None,
                               edge=round(float((s.won - s.px - s.px.map(fee)).mean()), 4) if len(s) else None)
    return out


def spike_table():
    s = read_rows("spikes")
    return {c: dict(n=int(len(g)), cont=round(float((g.out == "cont").mean()), 3), rev=round(float((g.out == "rev").mean()), 3))
            for c, g in s.groupby("cat")} if len(s) else {}


def settle(meta, eng_or_state, cap=150):
    """Record results of settled whale markets (for 'did whales like this win' stats)."""
    un = eng_or_state.unsettled if hasattr(eng_or_state, "unsettled") else eng_or_state.setdefault("unsettled", {})
    res = load_json(f"{DATA}/results.json", {}); now = time.time(); n = 0
    for tk, close in sorted(un.items(), key=lambda z: z[1]):
        if close > now - 300 or n >= cap: continue
        n += 1; m = meta.get(tk, fresh=True) or {}
        if m.get("result") in ("yes", "no"): res[tk] = m["result"]; un.pop(tk, None)
        elif close < now - 14 * 86400: un.pop(tk, None)
    if len(res) > 60000: res = dict(list(res.items())[-40000:])
    save_json(f"{DATA}/results.json", res)


# ---------------- push + persist ----------------
_PUSHED = []


def notify(title, body, prio=3, click=None, tags=None):
    print(f"\n=== {title}\n{body}", flush=True)
    t = os.getenv("KW_NTFY_TOPIC")
    now = time.time(); _PUSHED[:] = [x for x in _PUSHED if x > now - 86400]
    if not t or (len(_PUSHED) >= DAILY_PUSH and prio < 5): return
    j = {"topic": t, "title": title, "message": body[:3900], "priority": prio, **({"click": click} if click else {}), **({"tags": [tags]} if tags else {})}
    try:
        requests.post(os.getenv("KW_NTFY_SERVER", "https://ntfy.sh").rstrip("/") + "/", json=j, timeout=15).raise_for_status(); _PUSHED.append(now)
    except Exception as e: print("ntfy failed:", e, flush=True)


def persist(msg="kwhale: state"):
    if not os.getenv("GIT_PERSIST"): return
    br = os.getenv("GITHUB_REF_NAME", "main")
    subprocess.run(f'git add -A {DIR}; git diff --cached --quiet || git commit -qm "{msg}"; '
                   f'for i in 1 2 3 4; do git pull -q --rebase origin {br} && git push -q origin HEAD:{br} && break; sleep $((i*3)); done', shell=True)


# ---------------- commands ----------------
def digest(eng):
    st = eng.stats; M = eng.model; lb = [x for x in eng.livebook if x[0] > time.time() - 86400]
    L = [f"Scanned {st['trades']:,} trades · {st['whales']:,} whales · {money(st['vol'])} whale volume (since last digest)"]
    if lb: L.append(f"Live 15-min calls (24h): {np.mean([x[1] for x in lb]):.0%} right of {len(lb)}")
    miss = sorted([x for x in lb if not x[1]], key=lambda z: -z[3])[:3]
    if miss: L.append("Most confident misses: " + "; ".join(f"{(eng.meta.m.get(x[4]) or {}).get('title', x[4])[:40]} ({x[3]:.0%})" for x in miss if len(x) > 4))
    if M.get("test"): L.append(f"Model: {'PROVEN' if M.get('ok') else 'unproven'} · test {M['test']['acc_conf']:.0%} vs momentum {M['test']['mom_conf']:.0%} · {M.get('rows', 0):,} snapshots")
    if M.get("top_feats"): L.append("Leaning on: " + ", ".join(k for k, _ in M["top_feats"]))
    best = sorted(((v["edge"], k, v) for k, v in (M.get("cells") or {}).items() if v.get("sn", 0) >= 30 and v.get("edge") is not None), reverse=True)
    if best: L.append("Best whale-follow cells (settled): " + ", ".join(f"{k.split('|')[0]} {v['band']} {e * 100:+.1f}pts n={v['sn']}" for e, k, v in best[:3]))
    tr = eng.trends(time.time())
    if tr: L += ["Trends:"] + tr
    notify("📊 Kalshi scanner digest", "\n".join(L), 2)
    eng.stats = dict(trades=0, whales=0, vol=0.0)


def live():
    t0, maxmin = time.time(), float(os.getenv("LIVE_MAX_MIN") or 1e9)
    meta = Meta(); st = load_json(f"{DATA}/state.json", {})
    for k in ("pend_m", "pend_w", "pend_s"):  # can't grade what happened while we were offline
        st[k] = [r for r in st.get(k, []) if (r[0] if isinstance(r, list) else r["t"]) > t0 - 3000]
    M = load_json(f"{DIR}/model.json", {})
    if time.time() - M.get("trained", 0) > 6 * 3600: train()
    eng = Engine(meta, st, live=False, notify=notify)
    eng.last_mark = max(eng.last_mark, int(t0 // 900 * 900))
    warm = trades_between(t0 - 3900, max_pages=200)  # rebuild the last hour of prices/flow (no alerts, no duplicates)
    for r in warm: eng.tick(r[0]); eng.ingest(r[0], *r[2:])
    eng.live, eng.lag = True, 20; eng.quiet_until = max(eng.quiet_until, warm[-1][0] if warm else 0)
    seen = deque(maxlen=200000); seen_s = set(r[1] for r in warm[-50000:]); seen.extend(seen_s)
    last_ts = warm[-1][0] if warm else t0 - 60
    print(f"live: warmed with {len(warm)} trades · {len(eng.T)} markets · whale ≥ {money(MIN_WHALE)} · alert ≥ {money(ALERT_WHALE)} · poll {POLL}s", flush=True)
    if os.getenv("KW_START_PUSH", "1") == "1" and not st.get("started_once"):
        notify("Kalshi whale scanner online", f"Reports only (no trading). Whale alerts ≥ {money(ALERT_WHALE)}, spike alerts, 15-min outlook every quarter hour.", 3)
    st_flags = dict(started_once=True)
    saved = trained = t_settle = time.time(); last_digest = st.get("last_digest", 0)
    while time.time() - t0 < maxmin * 60:
        loop0 = time.time()
        try:
            tr = trades_between(last_ts - 5, max_pages=30)
            for r in tr:
                if r[1] in seen_s: continue
                seen.append(r[1]); seen_s.add(r[1]); eng.ingest(r[0], *r[2:]); last_ts = max(last_ts, r[0])
            if len(seen_s) > 250000: seen_s = set(seen)
            eng.tick(time.time())
            if time.time() - t_settle > 1800: settle(meta, eng); t_settle = time.time()
            if time.time() - trained > 6 * 3600:
                eng.flush(); eng.model = train(); trained = time.time()
            if time.time() - last_digest > 6 * 3600 and eng.stats["trades"]: digest(eng); last_digest = time.time()
            if time.time() - saved > 1800:
                eng.flush(); meta.save(); save_json(f"{DATA}/state.json", {**eng.state(), **st_flags, "last_digest": last_digest}); persist(); saved = time.time()
        except Exception as e:
            import traceback; traceback.print_exc(); print("loop error (continuing):", e, flush=True); time.sleep(5)
        time.sleep(max(1.0, POLL - (time.time() - loop0)))
    eng.flush(); meta.save(); save_json(f"{DATA}/state.json", {**eng.state(), **st_flags, "last_digest": last_digest}); persist("kwhale: end of run")


def backfill(days=None):
    """Replay past days of the public trade feed through the same engine to bootstrap the model."""
    days = float(days or os.getenv("KW_BACKFILL_DAYS") or 3); now = time.time(); meta = Meta()
    eng = Engine(meta, dict(unw={}, flow={}), live=False); n = 0
    start = int((now - days * 86400) // 3600 * 3600)
    for w in range(start, int(now - 120), 3600):
        tr = trades_between(w, min(w + 3600, now - 120), max_pages=400)
        for r in tr: eng.tick(r[0]); eng.ingest(r[0], *r[2:])
        n += len(tr); eng.tick(min(w + 3600, now - 120)); eng.flush()
        print(f"backfill {et(w, '%m-%d %H:%M')} ET: {len(tr):,} trades (total {n:,}) · {eng.stats['whales']:,} whales · {len(eng.T)} live markets", flush=True)
        if len(tr) >= 400000: print("  page cap hit: hour truncated", flush=True)
    st = load_json(f"{DATA}/state.json", {})
    for k in ("unw",):  # keep cash-out statistics from history
        for c, v in eng.unw.items():
            o = st.setdefault(k, {}).setdefault(c, [0, 0, 0.0, 0.0]); st[k][c] = [a + b for a, b in zip(o, v)]
    st.setdefault("unsettled", {}).update(eng.unsettled); st["flow"] = {**eng.flow, **st.get("flow", {})}
    settle(meta, st, cap=3000); meta.save(); save_json(f"{DATA}/state.json", st); train(quiet=True); persist("kwhale: backfill")


def doctor():
    """Checks ntfy delivery without printing the topic (Actions logs on a public repo are public)."""
    t = os.getenv("KW_NTFY_TOPIC") or ""; srv = os.getenv("KW_NTFY_SERVER", "https://ntfy.sh").rstrip("/")
    print(f"KW_NTFY_TOPIC set: {bool(t)} · length {len(t)} · has '/', ':' or spaces: {any(c in t for c in '/: ')} · "
          f"uppercase letters: {any(c.isupper() for c in t)} (topics are case-sensitive) · server {srv}")
    if not t: return
    tag = f"doctor-{int(time.time())}"
    r = requests.post(srv + "/", json={"topic": t, "title": "Kalshi scanner doctor", "message": f"Delivery check {tag}", "priority": 4}, timeout=15)
    print("publish:", r.status_code, r.text[:200].replace(t, "<topic>"))
    time.sleep(3)
    q = requests.get(f"{srv}/{t}/json", params={"poll": 1, "since": "2h"}, timeout=15)
    msgs = [json.loads(x) for x in q.text.splitlines() if x.strip()]
    print(f"messages on this topic in last 2h: {len(msgs)} · this check found: {any(tag in (m.get('message') or '') for m in msgs)}")
    print("If found=True but your phone shows nothing, the app is subscribed to a different topic name/server than the secret.")


def report():
    M = load_json(f"{DIR}/model.json", {}); print(json.dumps({k: v for k, v in M.items() if k not in ("dr", "mv")}, indent=1, default=float))


def selftest():
    """Offline: synthetic trade stream with persistent order-flow -> engine -> grading -> training."""
    global DIR, DATA
    import tempfile; DIR = tempfile.mkdtemp(); DATA = f"{DIR}/data"
    rng = np.random.default_rng(7)
    class FakeMeta(Meta):
        def __init__(self): self.m = {}
        def get(self, tk, fresh=False):
            return self.m.setdefault(tk, dict(title=f"Test market {tk}", cat=CATS[hash(tk) % 5], link=f"{WEB}/x/{tk.lower()}", close=2e9, result=""))
    eng = Engine(FakeMeta(), live=False)
    tks = [f"KXTEST-{i}" for i in range(40)]; p = {t: rng.uniform(0.2, 0.8) for t in tks}; drift = {t: 0.0 for t in tks}
    t = 1.75e9; end = t + 4 * 86400
    while t < end:
        t += rng.exponential(2.0); tk = tks[rng.integers(40)]
        if rng.random() < 0.002: drift[tk] = rng.normal(0, 0.00025)
        sd = 1 if rng.random() < 0.5 + 400 * drift[tk] else -1  # informed flow leans the way price will drift
        p[tk] = float(np.clip(p[tk] + drift[tk] * 60 + rng.normal(0, 0.002), 0.05, 0.95))
        yp = round(p[tk] + (0.01 if sd > 0 else -0.01), 2); n = float(rng.choice([5, 20, 100, 3000], p=[0.5, 0.3, 0.18, 0.02]))
        eng.tick(t); eng.ingest(t, tk, sd, yp, n, n * (yp if sd > 0 else 1 - yp))
        if len(eng.rows["marks"]) > 5000: eng.flush()
    eng.flush()
    for k in ("marks", "whales", "spikes"): print(k, len(read_rows(k, 10_000)))
    M = train(quiet=True); print("ok:", M.get("ok"), "test:", M.get("test"))
    eng.model = M; eng.live = True; eng.push = notify; eng._report(eng.last_mark + 900, [])
    print("selftest passed")


if __name__ == "__main__":
    a = sys.argv[1:] or ["live"]
    cmds = dict(live=live, backfill=lambda: backfill(a[1] if len(a) > 1 else None), train=train, report=report, selftest=selftest, doctor=doctor,
                settle=lambda: (lambda m, s: (settle(m, s, 3000), save_json(f"{DATA}/state.json", s)))(Meta(), load_json(f"{DATA}/state.json", {})),
                testnotify=lambda: notify("Kalshi scanner test", "If you see this, KW_NTFY_TOPIC works. Separate from your commodity alerts.", 4))
    cmds.get(a[0], lambda: print(__doc__))()
