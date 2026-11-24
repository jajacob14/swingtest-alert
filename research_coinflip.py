"""Coin-flip windows: Kalshi at 40-60¢ with 2-6 min left. Can a model call the winner better than the price?
Train older 70% of windows, test newest 30%. Accuracy, calibration, ROI buying the model's side at the ask (+fee)."""
import os, math
import numpy as np, pandas as pd, kalshi_whale as K
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
P = lambda *a: print(*a, flush=True)
kd = K.kcols(pd.concat([K.load_k(m) for m in K.COMMS], ignore_index=True)).sort_values(["ticker", "ts"]).reset_index(drop=True)
h = np.sqrt((kd.tl - 0.5).clip(lower=0.25)); Kst = pd.to_numeric(kd.strike, errors="coerce")
kd["zd"] = (np.log(kd.spx.astype(float) / Kst) / (kd.ssv.astype(float).clip(lower=1e-5) * h)).replace([np.inf, -np.inf], np.nan)
D = kd[(kd.tl >= 2) & (kd.tl <= 6) & (kd.mid >= 0.40) & (kd.mid <= 0.60)].dropna(subset=["zd"]).copy()
D["y"] = pd.to_numeric(D.up, errors="coerce"); D = D.dropna(subset=["y"])
F = ["mid", "tl", "dmid1", "dmid3", "dmid5", "spread", "kvol", "sr1", "sr3", "sr5", "svz", "sgap", "zd"]
D[F] = D[F].astype(float).fillna(0)
wins = D.sort_values("cl").ticker.drop_duplicates().tolist(); cut = set(wins[int(len(wins) * .7):])
TR, TE = D[~D.ticker.isin(cut)], D[D.ticker.isin(cut)]
P(f"{K.PROFILE}: coin-flip rows {len(D):,} (train {len(TR):,} / test {len(TE):,}) · windows {D.ticker.nunique():,}")
k_acc = ((TE.mid >= .5) == (TE.y == 1)).mean()
z_acc = ((TE.zd >= 0) == (TE.y == 1)).mean()
P(f"Kalshi favourite right: {k_acc:.1%} · 'spot above target' right: {z_acc:.1%}")
m = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.04, max_leaf_nodes=15, min_samples_leaf=200, random_state=0).fit(TR[F], TR.y)
p = m.predict_proba(TE[F])[:, 1]
P(f"model right: {((p >= .5) == (TE.y == 1)).mean():.1%} · AUC model {roc_auc_score(TE.y, p):.3f} vs Kalshi price {roc_auc_score(TE.y, TE.mid):.3f}")
fee = lambda a: np.ceil(7 * np.clip(a, .01, .99) * (1 - np.clip(a, .01, .99)) - 1e-9) / 100
up = p >= .5; conf = np.maximum(p, 1 - p); ask = np.where(up, TE.ask, 1 - TE.bid); won = (up == (TE.y == 1)).astype(float); cost = ask + fee(ask)
T = TE.assign(conf=conf, won=won, cost=cost, ask_s=ask).sort_values("ts").groupby("ticker").head(1)   # one bet per window
for thr in (0.5, 0.6, 0.65, 0.7, 0.75):
    x = T[T.conf >= thr]
    if len(x) >= 50: P(f"  model ≥{thr:.0%} sure: {len(x):,} windows · right {x.won.mean():.1%} · avg price {x.ask_s.mean() * 100:.0f}¢ · ROI {(x.won - x.cost).sum() / x.cost.sum():+.1%}")
P("calibration (model says → actual): " + " · ".join(f"{a:.0%}-{b:.0%}: {T.won[(T.conf >= a) & (T.conf < b)].mean():.0%} (n{((T.conf >= a) & (T.conf < b)).sum()})" for a, b in ((.5, .55), (.55, .6), (.6, .7), (.7, 1.01))))
