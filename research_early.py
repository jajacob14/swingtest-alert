"""Early calls at tradeable prices: at the 11 / 8 / 5 min check-ins, buy the favoured side at ≤ a price cap and hold to
settlement (ask + Kalshi fee). Which trend/spot filters, if any, make it pay? Train = older 70% of windows, test = newest 30%."""
import os; os.environ.setdefault("KW_PROFILE", "crypto")
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
D = pd.concat([K.kframe(K.load_k(m), 14.6, True) for m in K.COMMS], ignore_index=True)
D["tlr"] = D.tl.round().astype(int); D = D[D.tlr.isin([11, 8, 5])].drop_duplicates(["ticker", "tlr"])
up = D.mid >= 0.5; D["side_up"] = up
D["ask_s"] = np.where(up, D.ask, 1 - D.bid); D["conf"] = np.where(up, D.mid, 1 - D.mid)
D["won"] = (up == (D.up == 1)).astype(float)
s = np.where(up, 1, -1); D["kmom3"] = D.dmid3 * s; D["kmom1"] = D.dmid1 * s; D["smom3"] = D.sr3 * s; D["smom1"] = D.sr1 * s; D["sg"] = D.sgap * s
D["cost"] = D.ask_s + K.fees(D.ask_s); D["pnl"] = D.won - D.cost
wins = D.sort_values("cl").ticker.drop_duplicates().tolist(); cut = set(wins[int(len(wins) * 0.7):])
TR, TE = D[~D.ticker.isin(cut)], D[D.ticker.isin(cut)]
def ev(X, m):
    x = X[m(X)].sort_values("tl", ascending=False).groupby("ticker").head(1)     # first check-in that qualifies
    if len(x) < 40: return None
    return len(x), x.won.mean(), x.ask_s.mean(), x.pnl.sum() / x.cost.sum()
R = {}
for lo, hi in ((0.55, 0.65), (0.65, 0.75), (0.75, 0.85), (0.85, 0.95)):
    R[f"price {lo:.0%}-{hi:.0%}, any"] = lambda x, lo=lo, hi=hi: (x.ask_s >= lo) & (x.ask_s < hi)
    R[f"price {lo:.0%}-{hi:.0%} + Kalshi trending its way (3m ≥ +5)"] = lambda x, lo=lo, hi=hi: (x.ask_s >= lo) & (x.ask_s < hi) & (x.kmom3 >= 0.05)
    R[f"price {lo:.0%}-{hi:.0%} + spot trending its way (3m ≥ 1σ)"] = lambda x, lo=lo, hi=hi: (x.ask_s >= lo) & (x.ask_s < hi) & (x.smom3 >= 1)
    R[f"price {lo:.0%}-{hi:.0%} + spot ahead of Kalshi (gap ≥ 0.3)"] = lambda x, lo=lo, hi=hi: (x.ask_s >= lo) & (x.ask_s < hi) & (x.sg >= 0.3)
    R[f"price {lo:.0%}-{hi:.0%} + Kalshi AND spot trending its way"] = lambda x, lo=lo, hi=hi: (x.ask_s >= lo) & (x.ask_s < hi) & (x.kmom3 >= 0.05) & (x.smom3 >= 1)
    R[f"price {lo:.0%}-{hi:.0%} + spot ahead + trending"] = lambda x, lo=lo, hi=hi: (x.ask_s >= lo) & (x.ask_s < hi) & (x.sg >= 0.3) & (x.smom1 > 0)
R["fading: price 55-75% but Kalshi moving against (3m ≤ −5)"] = lambda x: (x.ask_s >= .55) & (x.ask_s < .75) & (x.kmom3 <= -0.05)
P(f"{'rule':58s} | TRAIN calls won  paid  ROI | TEST calls won  paid  ROI")
good = []
for nm, f in R.items():
    a, b = ev(TR, f), ev(TE, f)
    if not (a and b): continue
    P(f"{nm:58s} | {a[0]:6,} {a[1]:4.0%} {a[2] * 100:4.0f}¢ {a[3]:+5.1%} | {b[0]:6,} {b[1]:4.0%} {b[2] * 100:4.0f}¢ {b[3]:+5.1%}")
    if a[3] > 0 and b[3] > 0: good.append((nm, a, b))
P("\nprofitable on both:"); [P(f"  ✅ {n} · test {b[0]} calls, won {b[1]:.0%} at avg {b[2] * 100:.0f}¢, ROI {b[3]:+.1%}") for n, a, b in good] or P("  none")
P("\n== swing instead of hold: buy at 11m (60-80¢), sell at the 5m check-in bid ==")
a = D[(D.tlr == 11) & (D.ask_s >= .6) & (D.ask_s < .8)][["ticker", "side_up", "ask_s", "kmom3", "smom3"]]
b = D[D.tlr == 5][["ticker", "bid", "ask"]]
m = a.merge(b, on="ticker"); m["sell"] = np.where(m.side_up, m.bid, 1 - m.ask)
m["pnl"] = m.sell - K.fees(m.sell) - m.ask_s - K.fees(m.ask_s)
for nm, f in (("all", m.ask_s > 0), ("Kalshi trending its way", m.kmom3 >= .05), ("spot trending its way", m.smom3 >= 1)):
    x = m[f]; P(f"  {nm:26s} {len(x):6,} trades · avg {x.pnl.mean() * 100:+.1f}¢ · ROI {x.pnl.sum() / (x.ask_s + K.fees(x.ask_s)).sum():+.1%}")
