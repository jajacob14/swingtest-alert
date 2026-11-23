"""Call the moment a side first crosses the threshold (any minute, 3-14 min left) vs only at the 3-min check-ins.
Graded on that first call; buy at the ask + fee at that minute, hold to settlement. Read-only."""
import os
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
D = pd.concat([K.kframe(K.load_k(m), 14.6, True) for m in K.COMMS], ignore_index=True)
D["conf"] = np.maximum(D.mid, 1 - D.mid); D["side"] = D.mid >= 0.5; D["tlr"] = D.tl.round().astype(int)
D["ask_s"] = np.where(D.side, D.ask, 1 - D.bid); D["won"] = (D.side == (D.up == 1)).astype(float)
D = D.sort_values(["ticker", "ts"]); N = D.ticker.nunique()
P(f"profile {K.PROFILE} · windows {N:,}")
def rule(nm, m, cks=None):
    x = D[m & (D.tl >= 3)]
    if cks: x = x[x.tlr.isin(cks)]
    x = x.sort_values("tl", ascending=False).groupby("ticker").head(1)
    cost = x.ask_s + K.fees(x.ask_s); pr = x.ask_s
    P(f"{nm:52s} right {x.won.mean():5.1%} · calls {len(x) / N:4.0%} of windows · avg price {pr.mean() * 100:3.0f}¢ · "
      f"paid ≥95¢ {(pr >= .95).mean():4.0%} · ROI {(x.won - cost).sum() / cost.sum():+5.1%} · median {x.tl.median():.0f} min left")
CK = [14, 11, 8, 5, 3]
for t in (0.80, 0.75, 0.70):
    rule(f"≥{t:.0%} at 3-min check-ins only (current)", D.conf >= t, CK)
    rule(f"≥{t:.0%} the first MINUTE it crosses", D.conf >= t)
    rule(f"≥{t:.0%} first minute, price ≤ 90¢ (skip if too late)", (D.conf >= t) & (D.ask_s <= 0.90))
    rule(f"≥{t:.0%} first minute, ≥6 min left", (D.conf >= t) & (D.tl >= 6))
P("\naccuracy by minutes left when the first ≥75% crossing happens:")
x = D[(D.conf >= .75) & (D.tl >= 3)].sort_values("tl", ascending=False).groupby("ticker").head(1)
for a, b in ((12, 15), (9, 12), (6, 9), (3, 6)):
    m = (x.tl >= a) & (x.tl < b); P(f"  {a}-{b} min left: right {x.won[m].mean():.1%} · avg price {x.ask_s[m].mean() * 100:.0f}¢ · {m.mean():.0%} of calls")
