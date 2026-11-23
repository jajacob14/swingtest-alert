"""Sell plan for ⭐ calls (≥80% at the 3-min check-ins): after the call, how often does the side's BID reach a take-profit
price before the close, and how many minutes does it take? By entry price and minutes left. Minute closes (lower bound)."""
import os
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
D = pd.concat([K.kframe(K.load_k(m), 14.6, True) for m in K.COMMS], ignore_index=True).sort_values(["ticker", "ts"])
D["tlr"] = D.tl.round().astype(int); D["conf"] = np.maximum(D.mid, 1 - D.mid); D["side"] = D.mid >= 0.5
C = D[D.tlr.isin([14, 11, 8, 5, 3]) & (D.conf >= 0.80)].sort_values("tl", ascending=False).groupby("ticker").head(1)
C = C.assign(ask_s=np.where(C.side, C.ask, 1 - C.bid), won=(C.side == (C.up == 1)).astype(float))
B = D[["ticker", "ts", "tl", "bid", "ask"]]
rows = []
for r in C.itertuples():
    f = B[(B.ticker == r.ticker) & (B.ts > r.ts)]
    sb = (f.bid if r.side else 1 - f.ask).to_numpy(); tl = f.tl.to_numpy()
    out = dict(tlr=r.tlr, px=r.ask_s, won=r.won)
    for tg in (0.92, 0.95, 0.97):
        k = np.argmax(sb >= tg) if (sb >= tg).any() else -1
        out[f"h{int(tg * 100)}"] = k >= 0; out[f"m{int(tg * 100)}"] = (r.tl - tl[k]) if k >= 0 else np.nan
    rows.append(out)
    if len(rows) >= 12000: break
R = pd.DataFrame(rows); R["pb"] = pd.cut(R.px, [0, .85, .90, .95, 1.0], labels=["≤85¢", "85-90¢", "90-95¢", "95¢+"])
P(f"calls sampled: {len(R):,} · right {R.won.mean():.1%}")
for tg in (92, 95, 97):
    P(f"\n== take profit at {tg}¢ (side's bid reaches it before the close) ==")
    g = R[R.px < tg / 100].groupby(["tlr", "pb"], observed=True).agg(n=("won", "size"), reach=(f"h{tg}", "mean"), mins=(f"m{tg}", "median"), won=("won", "mean"))
    print(g[g.n >= 40].round(3).to_string(), flush=True)
