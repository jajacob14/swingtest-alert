"""Volatile windows vs calls (read-only). For each window's first ≥80% check-in call (≥5 min left), follow the side's
price minute by minute to the close: did the window turn wild (Kalshi price churning far more than normal)? Then compare
holding to settlement vs taking profit, and — when a sharp swing hits — holding vs selling right then."""
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
fee = lambda a: np.ceil(7 * np.clip(a, .01, .99) * (1 - np.clip(a, .01, .99)) - 1e-9) / 100
D = pd.concat([K.kcols(K.load_k(m)) for m in K.COMMS], ignore_index=True)
D = D[(D.tl >= 0.5) & (D.tl <= 14.6)].copy(); D["mkt"] = D.ticker.map(K.comm_of); D = D.sort_values(["ticker", "ts"])
D["up"] = pd.to_numeric(D.up, errors="coerce"); D = D.dropna(subset=["up"])
g = D.groupby("ticker"); D["churn3"] = g.dmid1.transform(lambda v: v.abs().rolling(3, min_periods=1).sum())
thr = D.groupby("mkt").churn3.quantile(0.90).to_dict()            # "wild" = top 10% churn for that market
D["wild"] = D.churn3 >= D.mkt.map(thr)
P(f"{K.PROFILE}: {D.ticker.nunique():,} windows · wild = 3-min churn ≥ " + ", ".join(f"{m} {v * 100:.0f}¢" for m, v in thr.items()))
D["tlr"] = D.tl.round().astype(int); D["conf"] = np.maximum(D.mid, 1 - D.mid)
C = D[D.tlr.isin([14, 11, 8, 5]) & (D.conf >= 0.80) & (D.conf < 0.99)].sort_values("tl", ascending=False).groupby("ticker").head(1)
rows, adv, fav = [], [], []
G = dict(tuple(D.groupby("ticker")))
for r in C.itertuples():
    w = G[r.ticker]; up = r.mid >= 0.5; s = 1 if up else -1
    a = w[w.tl < r.tl]
    if len(a) < 2: continue
    sb = (a.bid if up else 1 - a.ask).to_numpy(); sm = (a.mid if up else 1 - a.mid).to_numpy(); tl = a.tl.to_numpy(); d3 = (a.dmid3 * s).to_numpy()
    won = int(up == (r.up == 1)); px = min(r.ask if up else 1 - r.bid, 0.99)
    wild = bool(a.wild.any())
    rows.append(dict(mkt=r.mkt, px=px, won=won, wild=wild, tp95=sb.max() >= .95, tp90=sb.max() >= .90))
    i = np.where(d3 <= -0.15)[0]                 # first sharp swing AGAINST the call: side's price fell ≥15¢ in 3 min
    if len(i): j = i[0]; adv.append(dict(mkt=r.mkt, px=px, won=won, sm=sm[j], sb=sb[j], tl=tl[j], drop=-d3[j]))
    i = np.where((d3 >= 0.08) & (sb >= 0.90))[0]  # sharp swing FOR the call, now sellable ≥90¢
    if len(i): j = i[0]; fav.append(dict(mkt=r.mkt, px=px, won=won, sb=sb[j], tl=tl[j], wild=bool(a.wild.iloc[: j + 1].any())))
R = pd.DataFrame(rows); co = R.px + fee(R.px)
R["hold"] = R.won - co
for t in (0.90, 0.95): R[f"pl{int(t * 100)}"] = np.where(R[f"tp{int(t * 100)}"], t - fee(t), R.won) - co
P(f"\n== {len(R):,} calls (first ≥80% at the 14/11/8/5-min checks) ==")
for nm, x in (("calm windows", R[~R.wild]), ("wild windows", R[R.wild])):
    P(f"  {nm:13s} n={len(x):6,} ({len(x) / len(R):.0%}) · won {x.won.mean():.1%} · reached 95¢ {x.tp95.mean():.0%} · "
      f"won if it reached 95¢ {x[x.tp95].won.mean():.1%} · P&L per contract: hold {x.hold.mean() * 100:+.2f}¢ · sell at 95¢ {x.pl95.mean() * 100:+.2f}¢ · sell at 90¢ {x.pl90.mean() * 100:+.2f}¢")
A = pd.DataFrame(adv)
if len(A):
    A["sell"] = A.sb - fee(A.sb); A["edge"] = A.won - A.sell        # holding vs selling right at the swing (per contract)
    P(f"\n== sharp swing AGAINST the call (fell ≥15¢ in 3 min): {len(A):,} cases ({len(A) / len(R):.0%} of calls) ==")
    A["band"] = pd.cut(A.sm, [0, .3, .5, .7, .85, 1.01], labels=["<30¢", "30-50¢", "50-70¢", "70-85¢", "85¢+"])
    A["tb"] = pd.cut(A.tl, [0, 2, 5, 15], labels=["<2 min", "2-5 min", "5+ min"])
    for (b, t), x in A.groupby(["band", "tb"], observed=True):
        if len(x) >= 30: P(f"  now {b:7s} {t:8s} n={len(x):5,} · still won {x.won.mean():.0%} · sell now gets {x.sell.mean() * 100:.0f}¢ · "
                           f"{'HOLD' if x.edge.mean() > 0.01 else 'SELL' if x.edge.mean() < -0.01 else 'even'} ({x.edge.mean() * 100:+.1f}¢ hold vs sell)")
F = pd.DataFrame(fav)
if len(F):
    F["sell"] = F.sb - fee(F.sb); F["edge"] = F.won - F.sell
    P(f"\n== sharp swing FOR the call, sellable ≥90¢: {len(F):,} cases ==")
    for nm, x in (("calm so far", F[~F.wild]), ("wild so far", F[F.wild])):
        for t, y in x.groupby(pd.cut(x.tl, [0, 3, 6, 15], labels=["<3 min", "3-6 min", "6+ min"]), observed=True):
            if len(y) >= 30: P(f"  {nm:11s} {t:7s} n={len(y):5,} · went on to win {y.won.mean():.1%} · TP now {y.sell.mean() * 100:.0f}¢ · "
                               f"{'HOLD' if y.edge.mean() > 0.005 else 'TP' if y.edge.mean() < -0.005 else 'even'} ({y.edge.mean() * 100:+.1f}¢ hold vs TP)")

# calls made while the market was ALREADY wild (known at call time — no look-ahead)
C2 = C.assign(px=np.minimum(np.where(C.mid >= .5, C.ask, 1 - C.bid), .99), won=((C.mid >= .5) == (C.up == 1)).astype(int))
C2["co"] = C2.px + fee(C2.px); C2["pl"] = C2.won - C2.co
P("\n== wild AT CALL TIME (3-min churn already in the top 10%) vs calm ==")
for nm, x in (("calm at call", C2[~C2.wild]), ("wild at call", C2[C2.wild])):
    P(f"  {nm:12s} n={len(x):6,} ({len(x) / len(C2):.0%}) · won {x.won.mean():.1%} · paid {x.px.mean() * 100:.0f}¢ · P&L {x.pl.mean() * 100:+.2f}¢/contract")
    for b, y in x.groupby(pd.cut(x.px, [0, .85, .9, .95, 1]), observed=True):
        if len(y) >= 50: P(f"      paid {b}: n={len(y):5,} won {y.won.mean():.1%} · P&L {y.pl.mean() * 100:+.2f}¢")
