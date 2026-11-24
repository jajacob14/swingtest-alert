"""Second-level forecast test on the live tick log (Kalshi book every ~2 s + Coinbase price stream):
does a Coinbase move predict Kalshi's NEXT move, how big, and how many seconds later? Also book imbalance.
Read-only."""
import os, math
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
d = K.read_gz(f"{K.DATA}/ticks.csv.gz")
P(f"tick rows {len(d):,}")
if not len(d): raise SystemExit
d = d.dropna(subset=["spot", "yb", "ya"]).copy(); d["ts"] = pd.to_numeric(d.ts); d = d.sort_values(["tk", "ts"])
d["mid"] = (d.yb + d.ya) / 2; d["imb"] = (d.qb - d.qa) / (d.qb + d.qa + 1e-9)
P(f"usable {len(d):,} · {pd.to_datetime(d.ts.min(), unit='s'):%m-%d %H:%M} .. {pd.to_datetime(d.ts.max(), unit='s'):%m-%d %H:%M} UTC · windows {d.tk.nunique():,}")
out = []
for tk, g in d.groupby("tk"):
    g = g.set_index(pd.to_datetime(g.ts, unit="s")).sort_index()
    g = g[~g.index.duplicated()].resample("2s").last().ffill(limit=3).dropna(subset=["mid", "spot"])
    if len(g) < 60: continue
    lr = np.log(g.spot); sd = lr.diff().rolling(150, min_periods=30).std()          # ~5 min of 2-s spot volatility
    for past in (10, 30):
        k = past // 2; g[f"sp{past}"] = (lr - lr.shift(k)) / (sd * math.sqrt(k))
    for fut in (10, 30, 60, 120):
        k = fut // 2; g[f"km{fut}"] = g.mid.shift(-k) - g.mid                         # Kalshi YES mid change ahead
    g["kpast30"] = g.mid - g.mid.shift(15)
    g["mid0"] = g.mid; g["c"] = g.c.iloc[0]; out.append(g)
X = pd.concat(out).dropna(subset=["sp10", "sp30", "km30"])
X = X[(X.mid0 > 0.08) & (X.mid0 < 0.92)]                                               # where prices can still move
P(f"analysed 2-s rows {len(X):,} (prices 8-92¢)")
P("\n== does a Coinbase move predict Kalshi's next move? (avg Kalshi YES change in ¢, sign = toward the spot move) ==")
for past in (10, 30):
    for thr in (1.5, 2.5, 3.5):
        m = X[f"sp{past}"].abs() >= thr; sgn = np.sign(X.loc[m, f"sp{past}"])
        row = " · ".join(f"next {f}s {np.nanmean(X.loc[m, f'km{f}'] * sgn) * 100:+.2f}¢" for f in (10, 30, 60, 120))
        P(f"  spot moved ≥{thr}σ in last {past}s (n={m.sum():,}): {row}")
P("\n== same, but only when Kalshi had NOT moved yet (|last 30s| < 2¢) — the lag window ==")
for thr in (2.0, 3.0):
    m = (X.sp30.abs() >= thr) & (X.kpast30.abs() < 0.02); sgn = np.sign(X.loc[m, "sp30"])
    tot = [np.nanmean(X.loc[m, f'km{f}'] * sgn) * 100 for f in (10, 30, 60, 120)]
    hit = np.nanmean((X.loc[m, "km60"] * sgn) > 0.02)
    P(f"  spot ≥{thr}σ/30s, Kalshi flat (n={m.sum():,}): next 10s {tot[0]:+.2f}¢ · 30s {tot[1]:+.2f}¢ · 60s {tot[2]:+.2f}¢ · 120s {tot[3]:+.2f}¢ · Kalshi moved ≥2¢ its way within 60s: {hit:.0%}")
P("\n== how fast does Kalshi catch up? share of the 120-s move done by 10/30/60 s ==")
m = X.sp30.abs() >= 2.5; sgn = np.sign(X.loc[m, "sp30"]); t120 = np.nanmean(X.loc[m, "km120"] * sgn)
if abs(t120) > 1e-6: P("  " + " · ".join(f"{f}s: {np.nanmean(X.loc[m, f'km{f}'] * sgn) / t120:.0%}" for f in (10, 30, 60)))
P("\n== order book imbalance (YES bids vs NO side size) → next 60 s ==")
for lo, hi in ((-1, -.6), (-.6, -.2), (-.2, .2), (.2, .6), (.6, 1.01)):
    m = (X.imb >= lo) & (X.imb < hi)
    if m.sum() > 200: P(f"  imbalance {lo:+.1f}..{hi:+.1f}: next 60s YES {np.nanmean(X.loc[m, 'km60']) * 100:+.2f}¢ (n={m.sum():,})")
P("\n== by coin: spot ≥2.5σ/30s → Kalshi next 60s toward it ==")
for c, g in X.groupby("c"):
    m = g.sp30.abs() >= 2.5
    if m.sum() > 30: P(f"  {c}: {np.nanmean(g.loc[m, 'km60'] * np.sign(g.loc[m, 'sp30'])) * 100:+.2f}¢ (n={m.sum()})")
