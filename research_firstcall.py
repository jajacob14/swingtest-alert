"""Which rule for MAKING a ⭐ call gives the best first-call accuracy (graded on the first call, never on a switch)?
Checkpoints as pushed: ~14 (open), 11, 8, 5, 3 min left. Read-only."""
import os; os.environ.setdefault("KW_PROFILE", "crypto")
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
D = pd.concat([K.kframe(K.load_k(m), 14.6, True) for m in K.COMMS], ignore_index=True)
D["conf"] = np.maximum(D.mid, 1 - D.mid); D["side"] = D.mid >= 0.5; D["tlr"] = D.tl.round().astype(int)
D = D.sort_values(["ticker", "ts"])
D["prev_conf"] = D.groupby("ticker").conf.shift(1); D["prev_side"] = D.groupby("ticker").side.shift(1)
D["mom"] = D.groupby("ticker").mid.diff(3).fillna(0)
P(f"windows {D.ticker.nunique():,}")
CK = [14, 11, 8, 5, 3]
C = D[D.tlr.isin(CK)].drop_duplicates(["ticker", "tlr"])
def run(name, ok_fn, cks=CK):
    c = C[C.tlr.isin(cks)].copy(); c = c[ok_fn(c)]
    f = c.sort_values("tl", ascending=False).groupby("ticker").head(1)       # first checkpoint that qualifies
    if not len(f): P(f"{name:58s} no calls"); return
    right = (f.side == (f.up == 1)).mean(); cov = len(f) / C.ticker.nunique()
    at = f.tlr.value_counts(normalize=True).reindex(cks).fillna(0)
    P(f"{name:58s} first-call right {right:.1%} · calls on {cov:.0%} of coin-windows · made at " + " ".join(f"{k}m:{v:.0%}" for k, v in at.items()))
P("\n== rules (graded on the FIRST call only) ==")
for thr in (0.80, 0.85, 0.90, 0.93):
    run(f"≥{thr:.0%} at any check-in", lambda c, t=thr: c.conf >= t)
for thr in (0.80, 0.85, 0.90):
    run(f"≥{thr:.0%} and the minute before ≥{thr:.0%} same side (stable)", lambda c, t=thr: (c.conf >= t) & (c.prev_conf >= t) & (c.prev_side == c.side))
for thr in (0.80, 0.85):
    run(f"≥{thr:.0%} stable, and not moving against it (3-min)", lambda c, t=thr: (c.conf >= t) & (c.prev_conf >= t) & (c.prev_side == c.side) & (np.where(c.side, c.mom, -c.mom) >= -0.02))
run("≥80% only from 8 min left on", lambda c: c.conf >= 0.80, [8, 5, 3])
run("≥85% only from 8 min left on", lambda c: c.conf >= 0.85, [8, 5, 3])
run("≥85% stable, from 8 min on", lambda c: (c.conf >= 0.85) & (c.prev_conf >= 0.85) & (c.prev_side == c.side), [8, 5, 3])
run("≥90% from 8 min on", lambda c: c.conf >= 0.90, [8, 5, 3])
run("≥80% at 5 or 3 min only", lambda c: c.conf >= 0.80, [5, 3])
run("≥85% at 5 or 3 min only", lambda c: c.conf >= 0.85, [5, 3])
P("\n== how often a ⭐ call made at each check-in later flips below 50% (any later check-in) ==")
for k in (14, 11, 8, 5):
    c = C[(C.tlr == k) & (C.conf >= 0.80)][["ticker", "side"]]
    later = C[C.tlr < k][["ticker", "side", "conf"]].merge(c, on="ticker", suffixes=("", "0"))
    fl = later[later.side != later.side0].ticker.nunique() / max(len(c), 1)
    P(f"  ⭐ at {k:2d} min left: {len(c):,} calls · flipped later {fl:.0%}")
