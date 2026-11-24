"""Scalp spike model: P(the cheap side's BID rises +10¢ within the next 5 minutes) from everything we have at that minute.
Trained on the older 70% of windows, tested on the newest 30%. Also: realistic scalp P&L (buy at ask+fee; sell at
target if hit, else sell at the bid 5 min later). Prints LR weights for the live bot. Read-only."""
import os, json, math
import numpy as np, pandas as pd, kalshi_whale as K
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
P = lambda *a: print(*a, flush=True)
kd = K.kcols(pd.concat([K.load_k(m) for m in K.COMMS], ignore_index=True)).sort_values(["ticker", "ts"]).reset_index(drop=True)
kd = kd[(kd.tl >= 1.5) & (kd.tl <= 14.6)].copy()
kd["kvz"] = kd.groupby(kd.ticker.map(K.comm_of)).kvol.transform(lambda v: (v - v.median()) / (v.std() + 1e-9))
h = np.sqrt((kd.tl - 0.5).clip(lower=0.25)); Kst = pd.to_numeric(kd.strike, errors="coerce")
kd["zd"] = (np.log(kd.spx.astype(float) / Kst) / (kd.ssv.astype(float).clip(lower=1e-5) * h)).replace([np.inf, -np.inf], np.nan)
out = []
for up in (True, False):
    s = 1 if up else -1; g = kd.groupby("ticker")
    bid = kd.bid if up else 1 - kd.ask; ask = kd.ask if up else 1 - kd.bid
    fb = pd.concat([(g.bid.shift(-k) if up else 1 - g.ask.shift(-k)) for k in range(1, 6)], axis=1)
    d = pd.DataFrame(dict(tk=kd.ticker, cl=kd.cl, tl=kd.tl, ask=ask, bid=bid, hi5=fb.max(axis=1), ex5=fb.ffill(axis=1).iloc[:, -1],
                          win=(pd.to_numeric(kd.up, errors="coerce") == (1 if up else 0)).astype(float),
                          m1=kd.dmid1 * s, m3=kd.dmid3 * s, m5=kd.dmid5 * s, am3=kd.dmid3.abs(), am5=kd.dmid5.abs(), spread=kd.ask - kd.bid,
                          kvz=kd.kvz, s1=kd.sr1 * s, s3=kd.sr3 * s, s5=kd.sr5 * s, svz=kd.svz, sg=kd.sgap * s, az=kd.zd.abs(), sz=kd.zd * s))
    out.append(d[(d.ask >= 0.03) & (d.ask <= 0.35)])
D = pd.concat(out).dropna(subset=["hi5", "az"]).reset_index(drop=True)
D["hit"] = (D.hi5 >= D.ask + 0.10 - 1e-9).astype(int)
F = ["ask", "tl", "m1", "m3", "m5", "am3", "am5", "spread", "kvz", "s1", "s3", "s5", "svz", "sg", "az", "sz"]
D[F] = D[F].astype(float).fillna(0)
wins = D.sort_values("cl").tk.drop_duplicates().tolist(); cut = set(wins[int(len(wins) * .7):])
TR, TE = D[~D.tk.isin(cut)], D[D.tk.isin(cut)]
P(f"{K.PROFILE}: rows {len(D):,} · base pop rate +10¢/5m {D.hit.mean():.1%} · test rows {len(TE):,}")
mu, sd = TR[F].mean().to_numpy(), TR[F].std().replace(0, 1).to_numpy()
Z = lambda X: np.clip((X[F].to_numpy() - mu) / sd, -6, 6)
w = np.zeros(len(F) + 1); Xt = np.column_stack([np.ones(len(TR)), Z(TR)]); y = TR.hit.to_numpy()
for _ in range(30):
    p = 1 / (1 + np.exp(-Xt @ w)); Wt = p * (1 - p) + 1e-9
    w -= np.linalg.solve((Xt * Wt[:, None]).T @ Xt + 1.0 * np.eye(len(w)), Xt.T @ (p - y))
plr = 1 / (1 + np.exp(-np.column_stack([np.ones(len(TE)), Z(TE)]) @ w))
hgb = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=300, random_state=0).fit(TR[F], TR.hit)
phg = hgb.predict_proba(TE[F])[:, 1]
fee = lambda a: np.ceil(7 * np.clip(a, .01, .99) * (1 - np.clip(a, .01, .99)) - 1e-9) / 100
cost = TE.ask + fee(TE.ask); tg = (TE.ask + .10).clip(upper=.99)
pnl = np.where(TE.hit == 1, tg - fee(tg), TE.ex5.fillna(TE.bid) - fee(TE.ex5.fillna(TE.bid))) - cost
TE = TE.assign(plr=plr, phg=phg, pnl=pnl, cost=cost)
P(f"AUC: logistic {roc_auc_score(TE.hit, plr):.3f} · boosted trees {roc_auc_score(TE.hit, phg):.3f} (0.5 = no skill)")
for nm in ("plr", "phg"):
    P(f"\n== {nm}: test by predicted decile (actual pop rate · scalp P&L per $) ==")
    q = pd.qcut(TE[nm], 10, labels=False, duplicates="drop")
    for k_, g_ in TE.groupby(q): P(f"  decile {k_ + 1}: predicted {g_[nm].mean():5.1%} → popped {g_.hit.mean():5.1%} · P&L {g_.pnl.sum() / g_.cost.sum():+6.1%} · n {len(g_):,}")
    for thr in (0.35, 0.45, 0.55, 0.65):
        g_ = TE[TE[nm] >= thr]
        if len(g_) >= 100: P(f"  alert if ≥{thr:.0%}: n {len(g_):,} ({len(g_) / len(TE):.1%}) · popped {g_.hit.mean():.1%} · P&L {g_.pnl.sum() / g_.cost.sum():+.1%}")
P("\n== by minutes left (logistic ≥45%) ==")
for a, b in ((10, 15), (6, 10), (4, 6), (1.5, 4)):
    g_ = TE[(TE.tl >= a) & (TE.tl < b)]; h_ = g_[g_.plr >= .45]
    P(f"  {a}-{b} min: base pop {g_.hit.mean():.1%} · alerts {len(h_):,} popped {h_.hit.mean() if len(h_) else float('nan'):.1%}")
P("\nfeature weights (logistic, standardized): " + ", ".join(f"{f} {v:+.2f}" for f, v in sorted(zip(F, w[1:]), key=lambda z: -abs(z[1]))))
P("SCALP_MODEL " + json.dumps(dict(F=F, mu=[round(float(x), 6) for x in mu], sd=[round(float(x), 6) for x in sd], w=[round(float(x), 5) for x in w]), separators=(",", ":")))
