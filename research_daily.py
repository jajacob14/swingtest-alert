"""Daily live-log review (read-only): ⭐ buy calls and 💸 scalp calls graded separately, scalp shadow pops, Coinbase→Kalshi lead."""
import time
import numpy as np, pandas as pd, kalshi_whale as K
P = lambda *a: print(*a, flush=True)
fee = lambda a: np.ceil(7 * np.clip(a, .01, .99) * (1 - np.clip(a, .01, .99)) - 1e-9) / 100
now = time.time(); D1, D7 = now - 86400, now - 7 * 86400
num = lambda d, cs: [d.__setitem__(c, pd.to_numeric(d[c], errors="coerce")) for c in cs if c in d]
day = lambda t: pd.to_datetime(t, unit="s").dt.tz_localize("UTC").dt.tz_convert("America/New_York").dt.strftime("%m-%d")


def rec(x, col):
    return f"{int(x[col].sum())}-{int((1 - x[col]).sum())} ({x[col].mean():.0%})" if len(x) else "none"


# ticks first: the scalp calls are re-graded on them (time to pop, price at the deadline)
tk_ = K.read_gz(f"{K.DATA}/ticks.csv.gz"); num(tk_, ["ts", "yb", "ya", "qb", "qa", "spot"])
tk_ = tk_.dropna(subset=["ts", "yb", "ya"]).sort_values("ts")
P(f"ticks: {len(tk_):,} book snapshots" + (f" · {pd.to_datetime(tk_.ts.min(), unit='s'):%m-%d %H:%M} → {pd.to_datetime(tk_.ts.max(), unit='s'):%m-%d %H:%M} UTC" if len(tk_) else ""))
TB = {k: g for k, g in tk_.groupby("tk")} if len(tk_) else {}

# ───── ⭐ buy calls ─────
P("\n━━ ⭐ BUY CALLS (calls_log) ━━")
c = K.read_gz(f"{K.DATA}/calls_log.csv.gz"); num(c, ["t1", "up", "won", "ps", "px", "best", "tl", "setup", "setup_n", "rev"])
c = c.dropna(subset=["t1", "won"]).drop_duplicates(["t1", "c"])
if len(c):
    P(f"24h {rec(c[c.t1 >= D1], 'won')} · 7d {rec(c[c.t1 >= D7], 'won')} · all {rec(c, 'won')}")
    c["day"] = day(c.t1)
    P("by day: " + " · ".join(f"{d_} {int(g.won.sum())}-{int((1 - g.won).sum())}" for d_, g in c[c.t1 >= D7].groupby("day")))
    P("by coin (7d): " + " · ".join(f"{k} {int(g.won.sum())}-{int((1 - g.won).sum())}" for k, g in c[c.t1 >= D7].groupby("c")))
    s = c.dropna(subset=["setup"])
    if len(s):
        s["b"] = pd.cut(s.setup, [0, .8, .88, .92, .96, 1.01])
        P("setup score vs actual: " + " · ".join(f"{b} n={len(g)} said {g.setup.mean():.0%} got {g.won.mean():.0%}" for b, g in s.groupby("b", observed=True)))
    x = c.dropna(subset=["px"]).copy()
    if len(x):
        x["px"] = x.px.clip(.01, .99); cost = x.px + fee(x.px)
        hold = x.won - cost
        tp = x.best >= .95 - 1e-9
        tpp = np.where(tp, .95 - fee(.95), x.won) - cost
        P(f"95¢ take-profit reached {tp.mean():.0%} (n={len(x)}, {int(x.best.notna().sum())} with tracked best price)")
        P(f"P&L per contract: held {hold.sum() * 100:+.0f}¢ ({hold.sum() / cost.sum():+.1%}) · sell at 95¢ {tpp.sum() * 100:+.0f}¢ ({tpp.sum() / cost.sum():+.1%})")
        for nm, g in (("px ≤85¢", x.px <= .85), ("px 86-90¢", (x.px > .85) & (x.px <= .90)), ("px >90¢", x.px > .90), ("≥8 min left", x.tl >= 8), ("<8 min left", x.tl < 8)):
            y = x[g]
            if len(y): co = y.px + fee(y.px); P(f"  {nm:12s} n={len(y):3d} won {y.won.mean():.0%} · held {(y.won - co).sum() * 100:+.0f}¢")
    P(f"reversals 🚨 shown on {int(c.rev.fillna(0).sum())} calls")
else: P("no calls logged yet")

# ───── 💸 scalp calls ─────
P("\n━━ 💸 SCALP CALLS (scalp_calls) ━━")
s = K.read_gz(f"{K.DATA}/scalp_calls.csv.gz"); num(s, ["t", "up", "entry", "tgt", "p", "t1", "until", "best", "hit"])
s = s.dropna(subset=["t", "hit"]).drop_duplicates(["tk", "up", "t"])
if len(s):
    s["up"] = s.up.astype(bool)
    def regrade(r):
        g = TB.get(r.tk)
        if g is None: return pd.Series(dict(tpop=np.nan, exitpx=np.nan))
        w = g[(g.ts >= r.t) & (g.ts <= r.until + 3)]
        sb = w.yb if r.up else 1 - w.ya
        hit = w.ts[sb >= r.tgt - 1e-9]
        last = sb[w.ts <= r.until]
        return pd.Series(dict(tpop=(hit.iloc[0] - r.t) / 60 if len(hit) else np.nan, exitpx=last.iloc[-1] if len(last) else np.nan))
    s = pd.concat([s.reset_index(drop=True), s.reset_index(drop=True).apply(regrade, axis=1)], axis=1)
    P(f"24h {rec(s[s.t >= D1], 'hit')} · 7d {rec(s[s.t >= D7], 'hit')} · all {rec(s, 'hit')}  (popped +10¢ within the deadline)")
    s["day"] = day(s.t)
    P("by day (said → got): " + " · ".join(f"{d_} {int(g.hit.sum())}/{len(g)} said {g.p.mean():.0%} got {g.hit.mean():.0%}" for d_, g in s[s.t >= D7].groupby("day")))
    s["b"] = pd.cut(s.p, [0, .5, .55, .6, .7, 1.01])
    P("calibration: " + " · ".join(f"{b} n={len(g)} got {g.hit.mean():.0%}" for b, g in s.groupby("b", observed=True)))
    P(f"best bounce: median {(s.best - s.entry).median() * 100:+.0f}¢ · time to pop median {s.tpop.median():.1f} min (n={int(s.tpop.notna().sum())})")
    P("by coin: " + " · ".join(f"{k} {int(g.hit.sum())}-{int((1 - g.hit).sum())}" for k, g in s.groupby("c")))
    ex = np.where(s.hit == 1, s.tgt, s.exitpx.fillna(s.entry))   # no tick at the deadline → assume flat
    pnl = ex - fee(ex) - s.entry - fee(s.entry); co = s.entry + fee(s.entry)
    P(f"P&L sell at target else at the deadline: {pnl.sum() * 100:+.0f}¢ on {len(s)} calls ({pnl.sum() / co.sum():+.1%} per $) · 7d {pnl[s.t >= D7].sum() * 100:+.0f}¢")
else: P("no scalp calls logged yet")

# ───── scalp shadow ─────
P("\n━━ scalp shadow (scalp_log, silent) ━━")
d = K.read_gz(f"{K.DATA}/scalp_log.csv.gz"); num(d, ["t", "entry", "best", "won", "t_hit", "tl"])
d = d.dropna(subset=["entry", "best"]).drop_duplicates(["tk", "up"])
d = d[d.entry <= .35]
if len(d):
    j = d.best - d.entry
    P(f"≤35¢ sides: {len(d)} · +10¢ {(j >= .10 - 1e-9).mean():.0%} · +15¢ {(j >= .15 - 1e-9).mean():.0%} · held to close won {d.won.mean():.0%}"
      + (f" · reached target median {d.t_hit.median() / 60:.1f} min" if d.t_hit.notna().any() else ""))
    for nm, g in (("≤15¢", d.entry <= .15), ("16-35¢", d.entry > .15)):
        y = d[g]; jj = y.best - y.entry
        if len(y): P(f"  {nm:7s} n={len(y):4d} +10¢ {(jj >= .1 - 1e-9).mean():.0%} · +15¢ {(jj >= .15 - 1e-9).mean():.0%}")
else: P("no shadow setups yet")

# ───── Coinbase → Kalshi lead ─────
P("\n━━ does Coinbase move first? (ticks) ━━")
if len(tk_) and tk_.spot.notna().any():
    for coin, g in tk_.dropna(subset=["spot"]).groupby("c"):
        ev, n = [], 0
        for _, w in g.groupby("tk"):
            w = w.set_index(pd.to_datetime(w.ts, unit="s"))[["yb", "ya", "spot"]].resample("2s").last().ffill()
            if len(w) < 60: continue
            w["mid"] = (w.yb + w.ya) / 2; r = np.log(w.spot).diff(3)          # 6-s spot move
            thr = r.abs().quantile(.995)
            for i in np.where(r.abs() >= thr)[0]:
                if i + 15 >= len(w) or i < 3: continue
                sg = np.sign(r.iloc[i]); m0 = w.mid.iloc[i - 3]
                ev.append([sg * (w.mid.iloc[i] - m0), sg * (w.mid.iloc[i + 2] - m0), sg * (w.mid.iloc[i + 5] - m0), sg * (w.mid.iloc[i + 15] - m0)])
            n += 1
        if ev:
            e = np.array(ev) * 100
            P(f"  {coin}: {len(e)} sharp spot moves over {n} windows · Kalshi had already moved {np.median(e[:, 0]):+.1f}¢ in the same 6 s → "
              f"+4 s {np.median(e[:, 1]):+.1f}¢ · +10 s {np.median(e[:, 2]):+.1f}¢ · +30 s {np.median(e[:, 3]):+.1f}¢ (median, toward the move)")
else: P("no spot-tagged ticks")
