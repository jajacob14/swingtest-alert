"""When is the 15-min crypto board reliable? Accuracy vs market sessions / opens, weekends, volatility, and
whether the 5 coins move together (read-only)."""
import os, time; os.environ.setdefault("KW_PROFILE", "crypto")
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
D = pd.concat([K.kframe(K.load_k(m)) for m in K.COMMS], ignore_index=True)
D["et"] = pd.to_datetime(D.ts, unit="s", utc=True).dt.tz_convert("America/New_York")
D["ok"] = ((D.mid >= 0.5) == (D.up == 1)).astype(float); D["conf"] = np.maximum(D.mid, 1 - D.mid)
D["win_start"] = pd.to_datetime(D.cl - 900, unit="s", utc=True).dt.tz_convert("America/New_York")
B = D[(D.tl >= 10) & (D.tl <= 11.5)].copy()            # board-time rows
B["dow"] = B.et.dt.dayofweek; B["hm"] = B.win_start.dt.hour * 60 + B.win_start.dt.minute
B["wkend"] = (B.dow >= 5) | ((B.dow == 4) & (B.et.dt.hour >= 17)) | ((B.dow == 6) & (B.et.dt.hour < 18))
def ev(m):
    m = m.astype(bool)
    if m.sum() < 30: return "n/a"
    b = B[m]; return f"right {b.ok.mean():.1%} (avg price says {b.conf.mean():.1%}) · {m.sum():,} rows"
P(f"board rows {len(B):,}  {B.et.min():%Y-%m-%d} .. {B.et.max():%Y-%m-%d}")
P("\n== weekday vs weekend =="); P("  weekday:", ev(~B.wkend)); P("  weekend:", ev(B.wkend))
EV = {"Asia open (Tokyo 7-8pm ET, Sun-Thu)": lambda b: (b.hm >= 19 * 60) & (b.hm < 20 * 60) & b.dow.isin([6, 0, 1, 2, 3]),
      "London open (3-4am ET, Mon-Fri)": lambda b: (b.hm >= 3 * 60) & (b.hm < 4 * 60) & (b.dow < 5),
      "US data releases (8:30-9:00am ET, Mon-Fri)": lambda b: (b.hm >= 8 * 60 + 30) & (b.hm < 9 * 60) & (b.dow < 5),
      "US stock open (9:30-10:30am ET, Mon-Fri)": lambda b: (b.hm >= 9 * 60 + 30) & (b.hm < 10 * 60 + 30) & (b.dow < 5),
      "US stock close (3:30-4:30pm ET, Mon-Fri)": lambda b: (b.hm >= 15 * 60 + 30) & (b.hm < 16 * 60 + 30) & (b.dow < 5),
      "top-of-hour windows (:00 start)": lambda b: b.win_start.dt.minute == 0,
      "Sat/Sun overnight (12-6am ET)": lambda b: (b.dow >= 5) & (b.hm < 6 * 60)}
P("\n== around market opens / events (board ~11 min left) ==")
for k, f in EV.items(): P(f"  {k:44s}", ev(f(B)))
P("  everything else:", ev(~np.logical_or.reduce([f(B) for f in EV.values()])))
P("\n== by volatility (spot σ, terciles) ==")
q = B.svz.quantile([1 / 3, 2 / 3]).values
for nm, m in (("calm", B.svz <= q[0]), ("normal", (B.svz > q[0]) & (B.svz <= q[1])), ("volatile", B.svz > q[1])): P(f"  {nm:9s}", ev(m))
P("\n== by confidence × volatility ==")
for nm, m in (("calm", B.svz <= q[0]), ("volatile", B.svz > q[1])):
    for a, bb in ((0.5, 0.65), (0.65, 0.8), (0.8, 1.01)): P(f"  {nm:9s} {a:.0%}-{min(bb, 1):.0%}:", ev(m & (B.conf >= a) & (B.conf < bb)))
P("\n== do the 5 coins move together? ==")
W = B.sort_values("tl").groupby(["cl", "mkt"]).first().reset_index()
g = W.groupby("cl").agg(n=("up", "size"), ups=("up", "sum"))
g = g[g.n == 5]; P(f"  windows with all 5: {len(g):,} · all 5 same direction: {((g.ups == 0) | (g.ups == 5)).mean():.0%} · 4+ same: {((g.ups <= 1) | (g.ups >= 4)).mean():.0%}")
P("\n== hour of week heat (board accuracy, ET), worst 12 hours ==")
B["how"] = B.dow * 24 + B.win_start.dt.hour
h = B.groupby("how").agg(ok=("ok", "mean"), n=("ok", "size")); h = h[h.n >= 60].sort_values("ok")
days = "Mon Tue Wed Thu Fri Sat Sun".split()
for i, r in h.head(12).iterrows(): P(f"  {days[i // 24]} {i % 24:02d}:00  right {r.ok:.1%} ({int(r.n)} rows)")
P(f"  best: {', '.join(f'{days[i // 24]} {i % 24:02d}:00 {r.ok:.0%}' for i, r in h.tail(5).iterrows())}")
