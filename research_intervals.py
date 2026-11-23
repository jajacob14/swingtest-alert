"""Walk-forward: for each of the last 28 days, build the setup table only from windows BEFORE that day (lookback L days),
then grade that day's calls (first ≥80% at the 3-min check-ins, with ≥M min left, sent if setup ≥ G). Also: how often
the 95¢ take-profit was reached after the call (side's bid, minute closes = lower bound). Read-only."""
import os
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
D = pd.concat([K.kframe(K.load_k(m), 14.6, True) for m in K.COMMS], ignore_index=True).sort_values(["ticker", "ts"]).reset_index(drop=True)
for c in ("sr3", "sgap"):
    if c not in D: D[c] = 0.0
g = D.groupby("ticker"); later_max = lambda v: v.iloc[::-1].cummax().iloc[::-1].shift(-1)
D["fyb"] = g.bid.transform(later_max); D["nb"] = 1 - D.ask; D["fnb"] = D.groupby("ticker").nb.transform(later_max)
D["tlr"] = D.tl.round().astype(int); D["conf"] = np.maximum(D.mid, 1 - D.mid); D["side"] = D.mid >= 0.5
vs = {m: (float(x.kvol.median()), float(x.kvol.std() or 1.0)) for m, x in D.groupby("mkt")}
s_ = np.where(D.side, 1, -1)
D = D.assign(kt=D.dmid3 * s_, st=D.sr3.fillna(0) * s_, sg=D.sgap.fillna(0) * s_, vz=[(v - vs[m][0]) / (vs[m][1] + 1e-9) for v, m in zip(D.kvol, D.mkt)])
D["px"] = np.where(D.side, D.ask, 1 - D.bid); D["won"] = (D.side == (D.up == 1)).astype(float); D["tp95"] = np.where(D.side, D.fyb, D.fnb) >= 0.95
D["day"] = pd.to_datetime(D.cl, unit="s", utc=True).dt.tz_convert("America/New_York").dt.normalize()
C0 = D[D.tlr.isin([14, 11, 8, 5, 3]) & (D.conf >= 0.80)].copy()
C0["key"] = ["|".join(K.setup_cols(r)) for r in C0[["px", "tl", "kt", "st", "vz", "sg"]].to_dict("records")]
days = sorted(C0.day.unique())[-28:]
P(f"{K.PROFILE}: candidate check-in rows {len(C0):,} · walk-forward days {len(days)} ({days[0]:%m-%d}..{days[-1]:%m-%d})")
def first_calls(C, M):
    return C[C.tl >= M].sort_values("tl", ascending=False).groupby("ticker").head(1)
res = []
for L in (3, 7, 14, 30, 999):
    for M in (3, 5, 6, 8):
        for G in (0.0, 0.80, 0.85, 0.88, 0.90):
            out = []
            for d in days:
                hist = first_calls(C0[(C0.day < d) & (C0.day >= d - pd.Timedelta(days=L))], 3)
                if len(hist) < 200: continue
                prior = hist.won.mean(); t = hist.groupby("key").won.agg(["sum", "size"])
                rate = ((t["sum"] + prior * 50) / (t["size"] + 50)).to_dict()
                day = C0[C0.day == d].copy(); day["rate"] = day.key.map(rate).fillna(prior)
                f = first_calls(day[day.rate >= G], M)           # first check-in that passes the gate (time ≥ M)
                out.append(f.assign(nwin=day.ticker.nunique()))
            if not out: continue
            x = pd.concat(out); nw = sum(o.nwin.iloc[0] for o in out if len(o)); cost = x.px + K.fees(x.px)
            res.append(dict(L=L, M=M, G=G, calls=len(x), cov=len(x) / max(nw, 1), right=x.won.mean(), px=x.px.mean(), mins=x.tl.median(),
                            tp=x.tp95[x.px < .95].mean(), roi=(x.won - cost).sum() / cost.sum(),
                            worst=x.groupby("day").won.mean().min()))
R = pd.DataFrame(res)
P("\nL=history days (999=all) · M=min minutes left · G=setup gate · cov=share of coin-windows with a call · tp=reached 95¢ after the call · worst=worst day's accuracy")
P(R.round(3).to_string(index=False))
P("\n== best accuracy with ≥5 min left and calls on ≥40% of coin-windows ==")
ok = R[(R.M >= 5) & (R.cov >= 0.40)].sort_values(["right", "cov"], ascending=False).head(8)
P(ok.round(3).to_string(index=False))
