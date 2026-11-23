"""Scalp shadow test so far (read-only): live ≤15¢ setups, best sellable price seen (every 4 s), target +12¢."""
import os
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
d = K.read_gz(f"{K.DATA}/scalp_log.csv.gz")
P(f"setups logged: {len(d)}")
if len(d):
    d["t"] = pd.to_numeric(d.t); d = d.drop_duplicates(["tk", "up"])
    P(f"from {pd.to_datetime(d.t.min(), unit='s'):%m-%d %H:%M} to {pd.to_datetime(d.t.max(), unit='s'):%m-%d %H:%M} UTC · unique {len(d)}")
    fee = lambda a: np.ceil(7 * np.clip(a, .01, .99) * (1 - np.clip(a, .01, .99)) - 1e-9) / 100
    d["jump"] = d.best - d.entry; cost = d.entry + fee(d.entry)
    for j in (0.05, 0.08, 0.10, 0.12, 0.15, 0.20):
        hit = d.jump >= j - 1e-9; pnl = np.where(hit, d.entry + j - fee(d.entry + j), d.won) - cost
        P(f"  sell at +{j * 100:.0f}¢: reached {hit.mean():5.1%} · result {pnl.sum() / cost.sum():+6.1%} per $ ({pnl.sum() * 100:+.0f}¢ total on 1 contract each)")
    P(f"  hold to settlement: won {d.won.mean():.1%} · result {(d.won - cost).sum() / cost.sum():+.1%}")
    P(f"  best bounce: median {d.jump.median() * 100:+.0f}¢ · 75th pct {d.jump.quantile(.75) * 100:+.0f}¢ · 90th {d.jump.quantile(.9) * 100:+.0f}¢")
    if "t_hit" in d: th = pd.to_numeric(d.t_hit, errors="coerce").dropna(); P(f"  when +12¢ was reached: median {th.median() / 60:.1f} min after the setup (n={len(th)})")
    for nm, g in (("entry ≤8¢", d.entry <= .08), ("entry 9-15¢", d.entry > .08), ("≥9 min left", d.tl >= 9), ("6-9 min left", d.tl < 9),
                  ("sim ≥40%", d.sim >= .4), ("sim <40%", d.sim < .4), ("spot agrees (spot ≥ price)", d.spot >= d.entry), ("spot against", d.spot < d.entry)):
        x = d[g]
        if len(x) >= 10:
            h = (x.jump >= .12 - 1e-9); c_ = x.entry + fee(x.entry); pn = np.where(h, x.entry + .12 - fee(x.entry + .12), x.won) - c_
            P(f"  {nm:28s} n={len(x):4d} · reached +12¢ {h.mean():5.1%} · result {pn.sum() / c_.sum():+6.1%}")
