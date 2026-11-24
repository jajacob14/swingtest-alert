"""Path table: a side trading at price p with t minutes left — how high does its BID go before the close?
Half of the time it reaches at least hi50, a quarter of the time hi75; median minutes to the high; how often it wins.
Minute closes (lower bound on highs). Prints JSON for the live bot. Read-only."""
import os, json
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
kd = K.kcols(pd.concat([K.load_k(m) for m in K.COMMS], ignore_index=True)).sort_values(["ticker", "ts"]).reset_index(drop=True)
kd = kd[(kd.tl >= 2) & (kd.tl <= 14.6)]
out = []
for up in (True, False):
    bid = kd.bid if up else 1 - kd.ask; ask = kd.ask if up else 1 - kd.bid
    d = pd.DataFrame(dict(tk=kd.ticker, ts=kd.ts, tl=kd.tl, ask=ask, bid=bid, win=(pd.to_numeric(kd.up, errors="coerce") == (1 if up else 0)).astype(float)))
    rev = d.iloc[::-1]; d["hi"] = rev.groupby("tk").bid.transform(lambda v: v.cummax().shift(1)).iloc[::-1]
    out.append(d.dropna(subset=["hi"]))
D = pd.concat(out); D = D[(D.ask >= 0.02) & (D.ask <= 0.98)]
D["pb"] = (D.ask.clip(0.01, 0.99) * 20).astype(int) * 5; D["tb"] = np.select([D.tl >= 11.5, D.tl >= 8.5, D.tl >= 5.5], [13, 10, 7], 4)
T = {}
for (tb, pb), x in D.groupby(["tb", "pb"]):
    if len(x) < 300: continue
    T[f"{tb}|{pb}"] = [round(float(x.hi.quantile(.5)), 2), round(float(x.hi.quantile(.75)), 2), round(float(x.win.mean()), 2), len(x)]
for k in ("13|5", "13|50", "10|10", "10|50", "10|70", "7|80", "4|10"):
    if k in T: P(f"  {k}: half reach {T[k][0]}, quarter reach {T[k][1]}, wins {T[k][2]:.0%} (n={T[k][3]})")
P("PATH_JSON " + json.dumps(T, separators=(",", ":")))
