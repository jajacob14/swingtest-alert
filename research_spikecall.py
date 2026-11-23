"""Are first-cross ≥80% calls worse when the crossing comes from a fast jump, or late in the window? (read-only)"""
import os
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
D = pd.concat([K.kframe(K.load_k(m), 14.6, True) for m in K.COMMS], ignore_index=True)
D["conf"] = np.maximum(D.mid, 1 - D.mid); D["side"] = D.mid >= 0.5
D["ask_s"] = np.where(D.side, D.ask, 1 - D.bid); D["won"] = (D.side == (D.up == 1)).astype(float)
s = np.where(D.side, 1, -1); D["j1"] = D.dmid1 * s; D["j3"] = D.dmid3 * s; D["sr3s"] = D.sr3 * s; D["sr1s"] = D.sr1 * s
D = D.sort_values(["ticker", "ts"]); D["prevconf"] = D.groupby("ticker").conf.shift(1); D["prevside"] = D.groupby("ticker").side.shift(1)
X = D[(D.conf >= 0.80) & (D.ask_s <= 0.90) & (D.tl >= 3)].sort_values("tl", ascending=False).groupby("ticker").head(1)
cost = lambda x: x.ask_s + K.fees(x.ask_s)
def show(nm, m):
    x = X[m]
    if len(x) < 50: return
    P(f"  {nm:52s} n={len(x):6,} ({len(x) / len(X):4.0%}) · right {x.won.mean():5.1%} · avg price {x.ask_s.mean() * 100:3.0f}¢ · edge vs price {(x.won.mean() - x.ask_s.mean()) * 100:+4.1f} pts · ROI {(x.won - cost(x)).sum() / cost(x).sum():+5.1%}")
P(f"{K.PROFILE}: first ≥80% crossing (≤90¢) calls: {len(X):,}")
P("\n== by how the crossing happened (Kalshi move toward the call side) ==")
show("slow: last minute < +5 pts", X.j1 < 0.05)
show("normal: last minute +5..+10", (X.j1 >= 0.05) & (X.j1 < 0.10))
show("fast: last minute +10..+20", (X.j1 >= 0.10) & (X.j1 < 0.20))
show("spike: last minute ≥ +20", X.j1 >= 0.20)
show("3-min jump ≥ +25 (⚡ big move)", X.j3 >= 0.25)
show("3-min jump < +15 (steady climb)", X.j3 < 0.15)
P("\n== by minutes left ==")
for a, b in ((12, 15), (9, 12), (6, 9), (4, 6), (3, 4)): show(f"{a}-{b} min left", (X.tl >= a) & (X.tl < b))
P("\n== spot agreement at the crossing ==")
show("spot moved WITH the call (3m ≥ +1σ)", X.sr3s >= 1)
show("spot flat (|3m| < 1σ)", X.sr3s.abs() < 1)
show("spot moved AGAINST the call", X.sr3s <= -1)
show("Kalshi spiked ≥10 but spot didn't (<0.5σ)", (X.j1 >= 0.10) & (X.sr1s < 0.5))
P("\n== candidate filters (keep the call only if ...) ==")
for nm, m in (("not a spike (1m < +10)", X.j1 < 0.10), ("≥5 min left", X.tl >= 5), ("not spike AND ≥5 min left", (X.j1 < 0.10) & (X.tl >= 5)),
              ("spot agrees or flat", X.sr3s > -1), ("not (Kalshi spike without spot)", ~((X.j1 >= 0.10) & (X.sr1s < 0.5))),
              ("not spike, ≥5 min, spot not against", (X.j1 < 0.10) & (X.tl >= 5) & (X.sr3s > -1))):
    show(nm, m)
P("\n== if a spike crossing is skipped: call it the NEXT minute if still ≥80% (confirmation) ==")
D["nconf"] = D.groupby("ticker").conf.shift(-1); D["nside"] = D.groupby("ticker").side.shift(-1); D["nask"] = D.groupby("ticker").ask_s.shift(-1)
Y = D[(D.conf >= 0.80) & (D.ask_s <= 0.90) & (D.tl >= 3)].sort_values("tl", ascending=False).groupby("ticker").head(1)
sp = Y.j1 >= 0.10; conf_next = sp & (Y.nconf >= 0.80) & (Y.nside == Y.side) & (Y.tl >= 4)
z = pd.concat([Y[~sp].assign(px=Y.ask_s), Y[conf_next].assign(px=Y.nask)])
c2 = z.px + K.fees(z.px.clip(.01, .99))
P(f"  calls {len(z):,} ({len(z) / len(Y):.0%}) · right {z.won.mean():.1%} · avg price {z.px.mean() * 100:.0f}¢ · ROI {(z.won - c2).sum() / c2.sum():+.1%}")
