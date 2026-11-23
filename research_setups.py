"""Setup gate test: describe each ≥80% check-in call by its setup (price, minutes left, Kalshi trend, spot trend, volume
influx), learn each setup's hit rate on the OLDER 70% of windows, then on the NEWEST 30% send only calls whose setup was
≥ the gate. Does gating raise accuracy out of sample? Read-only."""
import os
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
D = pd.concat([K.kframe(K.load_k(m), 14.6, True) for m in K.COMMS], ignore_index=True).sort_values(["ticker", "ts"])
D["tlr"] = D.tl.round().astype(int); D["conf"] = np.maximum(D.mid, 1 - D.mid); D["side"] = D.mid >= 0.5
s = np.where(D.side, 1, -1); D["kt"] = D.dmid3 * s; D["st"] = D.sr3 * s; D["sg"] = D.sgap * s
D["vz"] = D.groupby("mkt").kvol.transform(lambda v: (v - v.median()) / (v.std() + 1e-9))
C = D[D.tlr.isin([14, 11, 8, 5, 3]) & (D.conf >= 0.80)].sort_values("tl", ascending=False).groupby("ticker").head(1).copy()
C["ask_s"] = np.where(C.side, C.ask, 1 - C.bid); C["won"] = (C.side == (C.up == 1)).astype(float)
C["pb"] = pd.cut(C.ask_s, [0, .85, .90, .95, 1.01], labels=["≤85", "85-90", "90-95", "95+"]).astype(str)
C["tb"] = np.select([C.tl >= 9.5, C.tl >= 5.5], ["9+", "6-9"], "3-5")
C["ktb"] = np.select([C.kt >= .05, C.kt <= -.05], ["K↑", "K↓"], "K→")
C["stb"] = np.select([C.st >= 1, C.st <= -1], ["S↑", "S↓"], "S→")
C["vb"] = np.select([C.vz >= 1, C.vz <= -0.5], ["vol↑", "vol↓"], "vol~")
C["sgb"] = np.select([C.sg >= .3, C.sg <= -.3], ["spot ahead", "spot behind"], "spot even")
wins = C.sort_values("cl").ticker.tolist(); cut = set(wins[int(len(wins) * .7):])
TR, TE = C[~C.ticker.isin(cut)], C[C.ticker.isin(cut)]
cost = lambda x: x.ask_s + K.fees(x.ask_s)
def rep(nm, x):
    if len(x): P(f"  {nm:44s} calls {len(x):6,} ({len(x) / len(TE):4.0%}) · right {x.won.mean():5.1%} · avg price {x.ask_s.mean() * 100:3.0f}¢ · ROI {(x.won - cost(x)).sum() / cost(x).sum():+5.1%}")
P(f"{K.PROFILE}: calls {len(C):,} · train {len(TR):,} · test {len(TE):,}")
rep("ALL ≥80% calls (test)", TE)
for keys in (["pb", "tb"], ["pb", "tb", "ktb"], ["pb", "tb", "ktb", "stb"], ["pb", "tb", "ktb", "stb", "vb"], ["pb", "tb", "ktb", "stb", "vb", "sgb"]):
    g = TR.groupby(keys).won.agg(["mean", "size"]); prior, k = TR.won.mean(), 50
    g["rate"] = (g["mean"] * g["size"] + prior * k) / (g["size"] + k)     # shrink small setups toward the average
    x = TE.merge(g[["rate", "size"]].reset_index(), on=keys, how="left"); x["rate"] = x.rate.fillna(prior)
    P(f"\nsetup = {' + '.join(keys)}  ({len(g)} setups)")
    for gate in (0.85, 0.88, 0.90, 0.92):
        rep(f"send only if setup backtest ≥ {gate:.0%}", x[x.rate >= gate])
    P(f"  calibration (setup rate → actual on test): " + " · ".join(f"{a:.0%}-{b:.0%}: {x.won[(x.rate >= a) & (x.rate < b)].mean():.0%} (n{((x.rate >= a) & (x.rate < b)).sum()})"
                                                         for a, b in ((.75, .85), (.85, .9), (.9, .95), (.95, 1.01)) if ((x.rate >= a) & (x.rate < b)).sum() >= 30))
