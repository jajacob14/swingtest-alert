"""Late-window pops at SECOND resolution (read-only), from the order-book ticks the live bots log (~2-3 s).
With 0.5-4 min left: how often a 3-35¢ side's bid rises +10¢ before the close; wild vs calm (3-min churn of minute mids
≥ the bot's WILD_THR); P&L buying at the ask + fee, selling at the target if reached, else what it settles at."""
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
fee = lambda a: np.ceil(7 * np.clip(a, .01, .99) * (1 - np.clip(a, .01, .99)) - 1e-9) / 100
T = K.read_gz(f"{K.DATA}/ticks.csv.gz", ["ts", "c", "tk", "yb", "ya", "qb", "qa", "spot"])
for c in ("ts", "yb", "ya"): T[c] = pd.to_numeric(T[c], errors="coerce")
T = T.dropna(subset=["ts", "yb", "ya"]).sort_values(["tk", "ts"])
P(f"{K.PROFILE}: {len(T):,} ticks" + (f" · {pd.to_datetime(T.ts.min(), unit='s'):%m-%d %H:%M} → {pd.to_datetime(T.ts.max(), unit='s'):%m-%d %H:%M} UTC" if len(T) else ""))
if not len(T): raise SystemExit
res = {}                                                   # official results, from the scanner's stored windows
for m in K.COMMS:
    d = K.load_k(m)
    if len(d): res.update(d.dropna(subset=["up"]).groupby("ticker").agg(up=("up", "first"), close=("close", "first")).to_dict("index"))
T = T[T.tk.isin(res)].copy()
T["up"] = pd.to_numeric(T.tk.map(lambda t: res[t]["up"]), errors="coerce"); T["cl"] = T.tk.map(lambda t: K.ts_of(res[t]["close"]))
T["tl"] = (T.cl - T.ts) / 60; T = T[(T.tl > 0) & (T.tl <= 15)].dropna(subset=["up"])
P(f"ticks on settled windows: {len(T):,} · windows {T.tk.nunique():,}")
rows = []
for tk, g in T.groupby("tk"):
    g = g.sort_values("ts"); mid = (g.yb + g.ya) / 2
    mm = mid.groupby((g.ts // 60).to_numpy()).last()      # minute mids → 3-min churn (same as the live 🌪️ test)
    ch = mm.diff().abs().rolling(3, min_periods=1).sum(); chm = dict(zip(mm.index, ch))
    churn = (g.ts // 60).map(chm).fillna(0).to_numpy()
    for up in (True, False):
        ask = (g.ya if up else 1 - g.yb).to_numpy(); bid = (g.yb if up else 1 - g.ya).to_numpy()
        fut = np.maximum.accumulate(bid[::-1])[::-1]; fut = np.r_[fut[1:], -1]   # best LATER bid
        won = float(g.up.iloc[0] == (1 if up else 0))
        sel = (g.tl.to_numpy() >= 0.5) & (g.tl.to_numpy() <= 4) & (ask >= 0.03) & (ask <= 0.35)
        idx = np.where(sel)[0][::10]                        # thin to ~every 20-30 s so one window doesn't dominate
        for i in idx: rows.append((g.c.iloc[0], g.tl.iloc[i], ask[i], fut[i], won, churn[i] >= K.WILD_THR))
X = pd.DataFrame(rows, columns=["c", "tl", "ask", "hi", "won", "wild"])
if not len(X): P("no late cheap-side ticks yet"); raise SystemExit
X["p10"] = X.hi >= X.ask + 0.10 - 1e-9; X["p15"] = X.hi >= X.ask + 0.15 - 1e-9
co = X.ask + fee(X.ask); tg = (X.ask + .10).clip(upper=.99); X["pl"] = np.where(X.p10, tg - fee(tg), X.won) - co; X["co"] = co
P(f"late cheap-side samples: {len(X):,}")
for a, b in ((0.5, 1), (1, 2), (2, 3), (3, 4)):
    x = X[(X.tl >= a) & (X.tl < b)]
    f = lambda y: f"+10¢ {y.p10.mean():4.0%} · +15¢ {y.p15.mean():4.0%} · P&L {y.pl.sum() / y.co.sum():+5.0%} (n {len(y):,})" if len(y) else "n 0"
    if len(x): P(f"  {a}-{b} min  all: {f(x)} | wild: {f(x[x.wild])} | calm: {f(x[~x.wild])}")
x = X[(X.tl >= 2) & (X.tl <= 4.5) & (X.ask >= .2) & X.wild]
P(f"\nlate-pop watch setup (wild, 2-4 min, 20-35¢): " + (f"+10¢ {x.p10.mean():.0%} · P&L {x.pl.sum() / x.co.sum():+.0%} (n {len(x):,})" if len(x) else "none yet"))
