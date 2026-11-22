"""Scalp test: buy a side at ≤15¢, sell when its bid bounces to the target before the close (else hold to settlement).
Buy at the ask + Kalshi fee, sell at the target bid − fee. One alert per window-side (first minute that qualifies).
Picked on the older 70% of windows, judged on the newest 30%. Minute closes only (intraminute highs not seen: conservative)."""
import os; os.environ.setdefault("KW_PROFILE", "crypto")
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
kd = K.kcols(pd.concat([K.load_k(m) for m in K.COMMS], ignore_index=True))
kd = kd.sort_values(["ticker", "ts"]); g = kd.groupby("ticker")
later_max = lambda v: v.iloc[::-1].cummax().iloc[::-1].shift(-1)
kd["fyb"] = g.bid.transform(later_max); kd["nb"] = 1 - kd.ask; kd["fnb"] = kd.groupby("ticker").nb.transform(later_max)
kd["fair"] = np.where(kd.sok > 0, K.sig(kd.sgap + K.logit(kd.mid)), np.nan)
out = []
for sgn in (1, -1):
    d = kd.assign(side=sgn, lask=kd.ask if sgn > 0 else 1 - kd.bid, fb=kd.fyb if sgn > 0 else kd.fnb,
                  win=(pd.to_numeric(kd.up, errors="coerce") == (1 if sgn > 0 else 0)).astype(float),
                  sfair=kd.fair if sgn > 0 else 1 - kd.fair, mom1=kd.dmid1 * sgn, mom3=kd.dmid3 * sgn, smom=kd.sr1 * sgn, smom3=kd.sr3 * sgn)
    out.append(d[(d.lask >= 0.01) & (d.lask <= 0.15) & (d.tl >= 1) & (d.tl <= 13)])
D = pd.concat(out).dropna(subset=["fb", "lask"]); D["edge"] = D.sfair - D.lask
wins = D.sort_values("cl").ticker.drop_duplicates().tolist(); cut = set(wins[int(len(wins) * 0.7):])
TR, TE = D[~D.ticker.isin(cut)], D[D.ticker.isin(cut)]
P(f"cheap rows {len(D):,} · windows {D.ticker.nunique():,} · test = newest {len(cut):,} windows")
TG = {"+5¢": lambda a: a + 0.05, "+10¢": lambda a: a + 0.10, "2x": lambda a: np.maximum(2 * a, a + 0.03)}
def sim(X, cond, tg):
    x = X[cond(X)].sort_values("ts").groupby(["ticker", "side"]).head(1)
    if len(x) < 15: return None
    t = np.minimum(TG[tg](x.lask), 0.99); hit = x.fb >= t - 1e-9; cost = x.lask + K.feev(x.lask)
    pnl = np.where(hit, t - K.feev(t), x.win) - cost
    return len(x), hit.mean(), pnl.mean(), pnl.sum() / cost.sum()
C = {"any ≤15¢": lambda x: x.lask > 0}
for tl in ((1, 4), (4, 8), (8, 13)): C[f"{tl[0]}-{tl[1]} min left"] = lambda x, a=tl: (x.tl >= a[0]) & (x.tl < a[1])
for e in (0.0, 0.03, 0.05, 0.10): C[f"spot says underpriced by ≥{e * 100:.0f}¢"] = lambda x, e=e: x.edge >= e
C["spot moving its way (1m)"] = lambda x: x.smom > 0.5
C["Kalshi bouncing its way (1m ≥ +2¢)"] = lambda x: x.mom1 >= 0.02
C["underpriced ≥5¢ + spot moving its way"] = lambda x: (x.edge >= 0.05) & (x.smom > 0.5)
C["underpriced ≥5¢ + 4-13 min left"] = lambda x: (x.edge >= 0.05) & (x.tl >= 4)
C["underpriced ≥10¢ + 4-13 min left"] = lambda x: (x.edge >= 0.10) & (x.tl >= 4)
C["5-15¢ + underpriced ≥5¢ + 4-13 min"] = lambda x: (x.lask >= 0.05) & (x.edge >= 0.05) & (x.tl >= 4)
C["5-15¢ + spot moving its way + 4-13 min"] = lambda x: (x.lask >= 0.05) & (x.smom > 0.5) & (x.tl >= 4)
C["dropped fast (3m ≤ −15¢) — mean reversion"] = lambda x: x.mom3 <= -0.15
C["dropped fast + spot now turning its way"] = lambda x: (x.mom3 <= -0.15) & (x.smom > 0)
R = []
for nm, cf in C.items():
    for tg in TG:
        a, b = sim(TR, cf, tg), sim(TE, cf, tg)
        if a and b: R.append((nm, tg, a, b))
P(f"\n{'rule':46s} {'tgt':5s} | TRAIN alerts hit  avg/contract ROI | TEST alerts hit  avg/contract ROI")
for nm, tg, a, b in R:
    P(f"{nm:46s} {tg:5s} | {a[0]:6,} {a[1]:5.0%} {a[2] * 100:+6.1f}¢ {a[3]:+6.0%} | {b[0]:6,} {b[1]:5.0%} {b[2] * 100:+6.1f}¢ {b[3]:+6.0%}")
P("\nprofitable on BOTH train and test (ROI > 0, ≥30 test alerts):")
good = [r for r in R if r[2][3] > 0 and r[3][3] > 0 and r[3][0] >= 30]
for nm, tg, a, b in sorted(good, key=lambda r: -r[3][3]): P(f"  ✅ {nm} · sell at {tg} · test {b[0]} alerts, hit {b[1]:.0%}, {b[2] * 100:+.1f}¢/contract, ROI {b[3]:+.0%}")
if not good: P("  none")
