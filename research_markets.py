"""Per-market call rules for the scanner's profile (commodity or crypto): how sure is Kalshi's price at each check-in,
which ⭐ threshold gives the best FIRST-call accuracy, at what price, and the payoff after fees. Read-only."""
import os
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
D = pd.concat([K.kframe(K.load_k(m), 14.6, True) for m in K.COMMS], ignore_index=True)
D["conf"] = np.maximum(D.mid, 1 - D.mid); D["side"] = D.mid >= 0.5; D["tlr"] = D.tl.round().astype(int)
D["ask_s"] = np.where(D.side, D.ask, 1 - D.bid); D["won"] = (D.side == (D.up == 1)).astype(float)
D = D.sort_values(["ticker", "ts"])
P(f"profile {K.PROFILE} · windows {D.ticker.nunique():,} · {pd.to_datetime(D.cl.min(), unit='s'):%Y-%m-%d}..{pd.to_datetime(D.cl.max(), unit='s'):%Y-%m-%d}")
P(D.groupby("mkt").ticker.nunique().to_string())
P(f"\nmedian spread (ask−bid): {(D.ask - D.bid).median() * 100:.0f}¢ · rows with spread ≥5¢: {((D.ask - D.bid) >= 0.05).mean():.0%}")
P("spread by market (median ¢): " + ", ".join(f"{m} {(g.ask - g.bid).median() * 100:.0f}" for m, g in D.groupby("mkt")))
CK = [14, 11, 8, 5, 3]; C = D[D.tlr.isin(CK)].drop_duplicates(["ticker", "tlr"])
P("\n== favourite wins, by price at each check-in (calibration) ==")
for k in CK:
    c = C[C.tlr == k]; row = []
    for a, b in ((.5, .65), (.65, .8), (.8, .9), (.9, 1.01)):
        m = (c.conf >= a) & (c.conf < b)
        if m.sum() >= 30: row.append(f"{a:.0%}-{min(b, 1):.0%}: {c.won[m].mean():.0%} (n{m.sum()})")
    P(f"  {k:2d}m left · " + " · ".join(row))
def first(c, thr, cks=CK):
    x = c[c.tlr.isin(cks) & (c.conf >= thr)].sort_values("tl", ascending=False).groupby("ticker").head(1)
    return x
P("\n== first ⭐ call rules (graded on the first call; buy at ask + fee, hold) ==")
for thr in (0.70, 0.75, 0.80, 0.85, 0.90):
    x = first(C, thr); cost = x.ask_s + K.fees(x.ask_s)
    at = x.tlr.value_counts(normalize=True).reindex(CK).fillna(0)
    P(f"  ≥{thr:.0%}: right {x.won.mean():.1%} · calls on {len(x) / C.ticker.nunique():.0%} of windows · avg price {x.ask_s.mean() * 100:.0f}¢ · ROI {(x.won - cost).sum() / cost.sum():+.1%} · made at "
      + " ".join(f"{k}m:{v:.0%}" for k, v in at.items()))
P("\n== per market at ≥80% (and the best threshold for each) ==")
for m, g in C.groupby("mkt"):
    res = []
    for thr in (0.75, 0.80, 0.85, 0.90):
        x = first(g, thr)
        if len(x) >= 30: res.append((thr, x.won.mean(), len(x) / g.ticker.nunique(), x.ask_s.mean()))
    if res: P(f"  {m:9s} " + " · ".join(f"≥{t:.0%}: {r:.0%} right on {cv:.0%} at {pr * 100:.0f}¢" for t, r, cv, pr in res))
P("\n== how often a ⭐ (≥80%) call made at each check-in later flips (any later check-in) ==")
for k in (14, 11, 8, 5):
    c = C[(C.tlr == k) & (C.conf >= 0.80)][["ticker", "side"]]
    later = C[C.tlr < k][["ticker", "side"]].merge(c, on="ticker", suffixes=("", "0"))
    P(f"  at {k:2d}m: {len(c):,} calls · flipped later {later[later.side != later.side0].ticker.nunique() / max(len(c), 1):.0%}")
P("\n== by session (ET hour of the window) at ≥80% ==")
x = first(C, 0.80); x = x.assign(h=pd.to_datetime(x.cl, unit="s", utc=True).dt.tz_convert("America/New_York").dt.hour)
print(x.groupby(x.h // 3 * 3).won.agg(["mean", "size"]).rename(columns={"mean": "right", "size": "n"}).round(3).to_string())
