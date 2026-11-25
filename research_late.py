"""Late-window scalps (read-only): with 0.5-4 min left, how often does a cheap side (3-35¢) pop +10¢ / +15¢ before the
close? By minutes left, price, and whether the market is wild right then (3-min churn in the market's top 10%).
Minute closes → a lower bound on pops. P&L: buy at ask + fee, sell at the target if reached, else it settles."""
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
fee = lambda a: np.ceil(7 * np.clip(a, .01, .99) * (1 - np.clip(a, .01, .99)) - 1e-9) / 100
D = pd.concat([K.kcols(K.load_k(m)) for m in K.COMMS], ignore_index=True)
D = D[(D.tl >= 0) & (D.tl <= 14.6)].copy(); D["mkt"] = D.ticker.map(K.comm_of); D = D.sort_values(["ticker", "ts"])
D["up"] = pd.to_numeric(D.up, errors="coerce"); D = D.dropna(subset=["up"])
g = D.groupby("ticker"); D["churn3"] = g.dmid1.transform(lambda v: v.abs().rolling(3, min_periods=1).sum())
thr = D.groupby("mkt").churn3.quantile(0.90).to_dict(); D["wild"] = D.churn3 >= D.mkt.map(thr)
rev = lambda s: s.iloc[::-1].cummax().iloc[::-1].shift(-1)          # best LATER value in the window
D["fyb"] = g.bid.transform(rev); D["nb"] = 1 - D.ask; D["fnb"] = D.groupby("ticker").nb.transform(rev)
rows = []
for up in (True, False):
    ask = D.ask if up else 1 - D.bid; hi = D.fyb if up else D.fnb; won = (D.up == (1 if up else 0)).astype(float)
    rows.append(pd.DataFrame(dict(mkt=D.mkt, tl=D.tl, ask=ask, hi=hi, won=won, wild=D.wild)))
X = pd.concat(rows); X = X[(X.ask >= 0.03) & (X.ask <= 0.35)].dropna(subset=["hi"])
for j in (0.10, 0.15): X[f"p{int(j * 100)}"] = X.hi >= X.ask + j - 1e-9
co = X.ask + fee(X.ask); tg = (X.ask + .10).clip(upper=.99)
X["pl"] = np.where(X.p10, tg - fee(tg), X.won) - co; X["co"] = co
P(f"{K.PROFILE}: cheap-side minutes {len(X):,}")
P("\n== pop chance by minutes left (all · wild right then · calm) ==")
for a, b in ((0.5, 1), (1, 2), (2, 3), (3, 4), (4, 6), (6, 10)):
    x = X[(X.tl >= a) & (X.tl < b)]
    if not len(x): continue
    w, c = x[x.wild], x[~x.wild]
    f = lambda y: f"+10¢ {y.p10.mean():4.0%} · +15¢ {y.p15.mean():4.0%} · P&L {y.pl.sum() / y.co.sum():+5.0%} (n {len(y):,})" if len(y) else "n 0"
    P(f"  {a}-{b} min  all: {f(x)}\n             wild: {f(w)}\n             calm: {f(c)}")
P("\n== last 0.5-3 min, wild, by price ==")
x = X[(X.tl >= 0.5) & (X.tl < 3) & X.wild]
for lo, hi_ in ((0.03, 0.10), (0.10, 0.20), (0.20, 0.35)):
    y = x[(x.ask >= lo) & (x.ask < hi_ + 1e-9)]
    if len(y) >= 30: P(f"  {lo * 100:.0f}-{hi_ * 100:.0f}¢: +10¢ {y.p10.mean():.0%} · +15¢ {y.p15.mean():.0%} · P&L {y.pl.sum() / y.co.sum():+.0%} (n {len(y):,})")
P("\n== by market, last 0.5-3 min ==")
x = X[(X.tl >= 0.5) & (X.tl < 3)]
for m, y in x.groupby("mkt"):
    P(f"  {m:10s} +10¢ {y.p10.mean():.0%} (wild {y[y.wild].p10.mean():.0%}, calm {y[~y.wild].p10.mean():.0%}) · share of minutes wild {y.wild.mean():.0%}")
