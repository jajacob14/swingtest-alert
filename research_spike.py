"""Calibrate the spike simulation: for cheap sides (≤15¢, 6-13 min left), simulated chance of reaching entry+12¢ vs what
the minute-close history shows (a lower bound: intraminute spikes are invisible). Read-only."""
import os, math; os.environ.setdefault("KW_PROFILE", "crypto")
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
kd = K.kcols(pd.concat([K.load_k(m) for m in K.COMMS], ignore_index=True)).sort_values(["ticker", "ts"])
g = kd.groupby("ticker"); later_max = lambda v: v.iloc[::-1].cummax().iloc[::-1].shift(-1)
kd["fyb"] = g.bid.transform(later_max); kd["nb"] = 1 - kd.ask; kd["fnb"] = kd.groupby("ticker").nb.transform(later_max)
rows = []
for up in (True, False):
    d = kd.assign(up_=up, lask=kd.ask if up else 1 - kd.bid, fb=kd.fyb if up else kd.fnb,
                  win=(pd.to_numeric(kd.up, errors="coerce") == (1 if up else 0)).astype(float))
    d = d[(d.lask >= 0.02) & (d.lask <= 0.15) & (d.tl >= 6) & (d.tl <= 13) & d.spx.notna() & d.ssv.notna()]
    rows.append(d.sort_values("ts").groupby("ticker").head(1))
D = pd.concat(rows).dropna(subset=["fb"]); D = D.sample(min(len(D), 6000), random_state=1)
D["K"] = pd.to_numeric(D.strike, errors="coerce"); D = D[D.K > 0]
JUMP = 0.12; out = []
for r in D.itertuples():
    tg = min(r.lask + JUMP, 0.99)
    p, eta, pw = K.spike_sim(r.spx, r.K, max(r.ssv, 1e-5), r.tl, r.up_, tg, n=1500, seed=1)
    out.append((p, eta, pw, float(r.fb >= tg - 1e-9), r.win, r.lask, tg))
O = pd.DataFrame(out, columns=["p", "eta", "pw", "hit", "win", "ask", "tgt"])
P(f"cheap sides tested: {len(O):,} · target = entry + {JUMP * 100:.0f}¢")
P("simulated chance  →  reached it at a minute close (lower bound) · settled a winner (sim said)")
for a, b in ((0, .1), (.1, .2), (.2, .3), (.3, .4), (.4, .5), (.5, .7), (.7, 1.01)):
    m = (O.p >= a) & (O.p < b)
    if m.sum() >= 20: P(f"  {a:.0%}-{min(b, 1):.0%}: n={m.sum():5,}  reached {O.hit[m].mean():5.1%}  · won {O.win[m].mean():5.1%} (sim {O.pw[m].mean():5.1%})")
for thr in (0.3, 0.35, 0.4, 0.5):
    m = O.p >= thr; cost = O.ask + K.feev(O.ask); pnl = np.where(O.hit == 1, O.tgt - K.feev(O.tgt), O.win) - cost
    if m.sum(): P(f"alert if sim ≥ {thr:.0%}: {m.sum():,} alerts ({m.mean():.0%} of cheap sides) · reached {O.hit[m].mean():.1%} · ROI at minute closes {pnl[m].sum() / cost[m].sum():+.0%}")
