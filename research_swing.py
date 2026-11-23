"""Swing table: a side trading at price p with t minutes left — how high does its BID go in the next 5 minutes, how often
does it touch +10¢/+15¢, how long until the high, and how often does it end the window lower (settles 0) anyway.
Minute closes (a lower bound on highs). Prints a JSON table for the live bot. Read-only."""
import os, json
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
kd = K.kcols(pd.concat([K.load_k(m) for m in K.COMMS], ignore_index=True)).sort_values(["ticker", "ts"]).reset_index(drop=True)
kd = kd[(kd.tl >= 2) & (kd.tl <= 14.6)]
out = []
for up in (True, False):
    ask = kd.ask if up else 1 - kd.bid; bid = kd.bid if up else 1 - kd.ask
    d = pd.DataFrame(dict(tk=kd.ticker, ts=kd.ts, tl=kd.tl, ask=ask, bid=bid, win=(pd.to_numeric(kd.up, errors="coerce") == (1 if up else 0)).astype(float)))
    g = d.groupby("tk").bid
    fw = pd.concat([g.shift(-k) for k in range(1, 6)], axis=1)           # the next 5 minutes' bids
    d["hi5"] = fw.max(axis=1); d["argm"] = fw.to_numpy().argmax(axis=1) + 1
    d = d.dropna(subset=["hi5"]); out.append(d)
D = pd.concat(out); D["pb"] = (D.ask.clip(0.01, 0.99) * 20).astype(int) * 5     # 5¢ buckets
D["tb"] = np.select([D.tl >= 11.5, D.tl >= 8.5, D.tl >= 5.5], [13, 10, 7], 4)
T = {}
for (tb, pb), x in D.groupby(["tb", "pb"]):
    if len(x) < 300: continue
    j = x.hi5 - x.ask
    T[f"{tb}|{pb}"] = [round(float((j >= .05).mean()), 2), round(float((j >= .10).mean()), 2), round(float((j >= .15).mean()), 2),
                       round(float(x.hi5.median()), 2), round(float(x.hi5.quantile(.75)), 2), int(x.argm.median()), round(float(x.win.mean()), 2), len(x)]
P(f"rows {len(D):,}")
for k in ("10|10", "10|20", "10|80", "7|10", "7|85", "4|10"):
    if k in T: P(f"  {k}: touch +5/+10/+15 = {T[k][0]:.0%}/{T[k][1]:.0%}/{T[k][2]:.0%} · median high {T[k][3]} · 75th {T[k][4]} · ~{T[k][5]} min · ends winning {T[k][6]:.0%} (n={T[k][7]})")
P("SWING_JSON " + json.dumps(T, separators=(",", ":")))
