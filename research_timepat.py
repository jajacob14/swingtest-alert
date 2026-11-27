"""Time-of-day / interval patterns (read-only). Over every stored 15-min window: does UP/DOWN depend on the hour, the
quarter-hour slot, the weekday, or what the previous window(s) did — and, crucially, does any of it beat KALSHI'S PRICE
(not just 50/50)? Each pattern is checked on the older 70% of days and again on the newer 30%; it only counts if the
edge vs price has the same sign, is ≥3 pts in both, and has enough windows. Also: ⭐-style calls' accuracy by hour."""
import numpy as np, pandas as pd, kalshi_whale as K
from datetime import datetime
P = lambda *a: print(*a, flush=True)
fee = lambda a: np.ceil(7 * np.clip(a, .01, .99) * (1 - np.clip(a, .01, .99)) - 1e-9) / 100
D = pd.concat([K.kcols(K.load_k(m)) for m in K.COMMS], ignore_index=True)
D = D[(D.tl >= 0.5) & (D.tl <= 15)].copy(); D["mkt"] = D.ticker.map(K.comm_of)
D["up"] = pd.to_numeric(D.up, errors="coerce"); D = D.dropna(subset=["up"])
D["tlr"] = D.tl.round().astype(int)
def at(t):  # Kalshi mid at ~t min left, per window
    x = D[D.tlr == t].sort_values("tl").groupby("ticker").mid.first(); return x
W = D.groupby("ticker").agg(mkt=("mkt", "first"), cl=("cl", "first"), up=("up", "first"))
for t in (14, 12, 9, 6): W[f"m{t}"] = at(t)
W = W.dropna(subset=["m12"]).sort_values(["mkt", "cl"])
st = pd.to_datetime(W.cl - 900, unit="s", utc=True).dt.tz_convert("America/New_York")
W["hour"], W["slot"], W["dow"] = st.dt.hour, st.dt.minute, st.dt.day_name().str[:3]
W["sess"] = W.cl.map(lambda t: K.session(t - 900))
g = W.groupby("mkt"); W["prev"] = g.up.shift(1); W["prev2"] = g.up.shift(2)
W["gapok"] = (W.cl - g.cl.shift(1)) == 900                                   # previous window really was the one before
W["streak"] = np.where(W.gapok & (W.prev == W.prev2), W.prev.map({1.0: "2 UP", 0.0: "2 DOWN"}), "mixed")
W["prevs"] = np.where(W.gapok, W.prev.map({1.0: "prev UP", 0.0: "prev DOWN"}), None)
days = np.sort(W.cl.map(lambda t: datetime.fromtimestamp(t).date()).unique()); cut = days[int(len(days) * 0.7)]
W["half"] = np.where(W.cl.map(lambda t: datetime.fromtimestamp(t).date()) < cut, "old", "new")
P(f"{K.PROFILE}: {len(W):,} windows · {len(days)} days ({days[0]} → {days[-1]}) · split at {cut}")
P(f"overall UP {W.up.mean():.1%} · Kalshi's average 12-min-left price {W.m12.mean():.1%}")

def scan(col, label, minn=150):
    out = []
    for (k, h), x in W.dropna(subset=[col]).groupby([col, "half"]):
        out.append(dict(k=k, half=h, n=len(x), up=x.up.mean(), px=x.m12.mean(), edge=x.up.mean() - x.m12.mean()))
    R = pd.DataFrame(out)
    if not len(R): return []
    R = R.pivot(index="k", columns="half", values=["n", "up", "px", "edge"])
    hits = []
    for k, r in R.iterrows():
        try: n0, n1, e0, e1, u0, u1 = r[("n", "old")], r[("n", "new")], r[("edge", "old")], r[("edge", "new")], r[("up", "old")], r[("up", "new")]
        except KeyError: continue
        if any(pd.isna(v) for v in (n0, n1, e0, e1)) or min(n0, n1) < minn: continue
        z0, z1 = e0 / np.sqrt(max(u0 * (1 - u0), .01) / n0), e1 / np.sqrt(max(u1 * (1 - u1), .01) / n1)
        CELLS[0] += 1
        flag = "✅" if np.sign(e0) == np.sign(e1) and min(abs(e0), abs(e1)) >= 0.03 and min(abs(z0), abs(z1)) >= 1.5 else ""
        hits.append((k, n0, n1, u0, u1, e0, e1, flag))
    P(f"\n== {label}: UP rate old→new · edge vs Kalshi's 12-min price old→new (✅ = ≥3 pts same sign both halves) ==")
    for k, n0, n1, u0, u1, e0, e1, f in hits:
        P(f"  {str(k):10s} n {int(n0):5,}/{int(n1):5,} · UP {u0:.0%}→{u1:.0%} · edge {e0 * 100:+5.1f}→{e1 * 100:+5.1f} pts {f}")
    return [h for h in hits if h[-1]]

found = []; CELLS = [0]
found += [("hour", h) for h in scan("hour", "hour of day (ET, window start)")]
found += [("slot", h) for h in scan("slot", "quarter-hour slot (:00 :15 :30 :45)")]
found += [("dow", h) for h in scan("dow", "weekday")]
found += [("prev", h) for h in scan("prevs", "previous window's result (same market)")]
found += [("streak", h) for h in scan("streak", "last two windows")]
W["mh"] = W.mkt + " " + W.hour.astype(str).str.zfill(2)
found += [("mkt×hour", h) for h in scan("mh", "market × hour", minn=60)]
W["ms"] = W.mkt + " " + W.prevs.fillna("?")
found += [("mkt×prev", h) for h in scan("ms", "market × previous result", minn=100)]

# ⭐-style calls by hour: first check-in (14/11/8/5) where Kalshi ≥80%, won vs price, both halves
C = D[D.tlr.isin([14, 11, 8, 5]) & (np.maximum(D.mid, 1 - D.mid) >= 0.80) & (np.maximum(D.mid, 1 - D.mid) < 0.99)]
C = C.sort_values("tl", ascending=False).groupby("ticker").head(1).copy()
C["won"] = ((C.mid >= .5) == (C.up == 1)).astype(int); C["px"] = np.minimum(np.where(C.mid >= .5, C.ask, 1 - C.bid), .99)
C = C.join(W[["hour", "half", "sess"]], on="ticker", how="inner"); C["pl"] = C.won - C.px - fee(C.px)
P("\n== ⭐-style calls (Kalshi ≥80% at the 14/11/8/5 checks) by hour: won old→new · P&L per contract old→new ==")
bad = []
for h, x in C.groupby("hour"):
    a, b = x[x.half == "old"], x[x.half == "new"]
    if min(len(a), len(b)) < 100: continue
    flag = "⚠️" if a.pl.mean() < -0.02 and b.pl.mean() < -0.02 else ""
    if flag: bad.append(h)
    P(f"  {h:02d}:00  n {len(a):5,}/{len(b):5,} · won {a.won.mean():.1%}→{b.won.mean():.1%} · P&L {a.pl.mean() * 100:+.1f}→{b.pl.mean() * 100:+.1f}¢ {flag}")
P(f"\nSUMMARY {K.PROFILE}: {CELLS[0]} pattern cells tested · expected to pass by pure chance ≈ {CELLS[0] * 2 * 0.0668 ** 2:.1f}"
  f"\npatterns beating Kalshi's price ≥3 pts AND z≥1.5 in BOTH halves: {len(found)}"
  + "".join(f"\n  {t}: {h[0]} (UP {h[3]:.0%}/{h[4]:.0%}, edge {h[5] * 100:+.1f}/{h[6] * 100:+.1f} pts, n {int(h[1])}/{int(h[2])})" for t, h in found)
  + f"\n  hours where ⭐-style calls lost >2¢ in both halves: {bad or 'none'}")
