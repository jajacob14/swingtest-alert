"""Offline model shoot-out for the crypto scanner (read-only: sends nothing, saves nothing).

Same data, same walk-forward splits as the live trainer (weeks: older 70% -> newest 30%; months: weeks -> older
months). Every candidate is scored on rows it never trained on, on all rows (3-12 min left) and on the rows the board
actually uses (~11 min left), plus the edge-bet test the live bot uses.
Run: KW_PROFILE=crypto python research_crypto.py
"""
import os, sys, time, math
os.environ.setdefault("KW_PROFILE", "crypto")
import numpy as np, pandas as pd
import kalshi_whale as K
from sklearn.ensemble import HistGradientBoostingClassifier

t_start = time.time()
P = lambda *a: print(*a, flush=True)


def ll(y, q): q = np.clip(q, 1e-4, 1 - 1e-4); return float(-np.mean(y * np.log(q) + (1 - y) * np.log(1 - q)))
def lg(p): return K.logit(p)


# ---------------- data + extra spot features ----------------
D = pd.concat([K.kframe(K.load_k(m)) for m in K.COMMS], ignore_index=True)
P(f"rows {len(D):,} · windows {D.ticker.nunique():,} · {pd.to_datetime(D.cl.min(), unit='s'):%Y-%m-%d} .. {pd.to_datetime(D.cl.max(), unit='s'):%Y-%m-%d}")
P(D.groupby("mkt").ticker.nunique().to_string())

parts = []
for c, g in D.groupby("mkt"):
    S = K._SPOT.get(c) or {}
    sp = pd.DataFrame(sorted(S.items()), columns=["ts", "px"]).dropna()
    if len(sp) < 100: parts.append(g); continue
    sp["ts"] = sp.ts.astype("int64"); lr_ = np.log(sp.px).diff()
    sp["sv60"] = lr_.rolling(60, min_periods=20).std(); sp["sv240"] = lr_.rolling(240, min_periods=60).std()
    sp["svew"] = np.sqrt((lr_ ** 2).ewm(halflife=20, min_periods=10).mean())
    for n in (10, 15): sp[f"r{n}"] = np.log(sp.px).diff(n)
    g = pd.merge_asof(g.assign(ts=g.ts.astype("int64")).sort_values("ts"), sp[["ts", "px", "sv60", "sv240", "svew", "r10", "r15"]],
                      on="ts", direction="backward", tolerance=150)
    parts.append(g)
D = pd.concat(parts, ignore_index=True)
Kst = pd.to_numeric(D.strike, errors="coerce")
h = np.sqrt((D.tl - 0.5).clip(lower=0.25))
for nm in ("sv60", "sv240", "svew"):
    sv = D[nm].astype(float).clip(lower=1e-5)
    D[f"fair_{nm}"] = K.ncdf((np.log(D.px.astype(float) / Kst) / (sv * h)).fillna(0).clip(-8, 8))
D["fair_mix"] = K.ncdf((np.log(D.px.astype(float) / Kst) / (np.sqrt((D.sv60.clip(lower=1e-5) ** 2 + D.sv240.clip(lower=1e-5) ** 2) / 2) * h)).fillna(0).clip(-8, 8))
D["lgap_bps"] = (np.log(D.px.astype(float) / Kst) * 1e4).clip(-300, 300).fillna(0)
D["sr10"] = (D.r10 / (D.sv60.clip(lower=1e-5) * math.sqrt(10))).clip(-6, 6).fillna(0)
D["sr15"] = (D.r15 / (D.sv60.clip(lower=1e-5) * math.sqrt(15))).clip(-6, 6).fillna(0)
D["hour"] = pd.to_datetime(D.ts, unit="s").dt.hour
D["dow"] = pd.to_datetime(D.ts, unit="s").dt.dayofweek
D["spok"] = D.px.notna() & D.sv60.notna()
P(f"spot coverage: {D.spok.mean():.1%} of rows")
D = D[D.spok].reset_index(drop=True)
for nm in ("fair_sv60", "fair_sv240", "fair_svew", "fair_mix"): D[nm] = D[nm].astype(float).clip(0.005, 0.995)

now = time.time()
Wk, Mo = D[D.cl >= now - K.WEEKS_D * 86400], D[D.cl < now - K.WEEKS_D * 86400]
wins = Wk.sort_values("cl").ticker.drop_duplicates().tolist(); cut = set(wins[int(len(wins) * 0.7):])
SPL = {"weeks": (Wk[~Wk.ticker.isin(cut)], Wk[Wk.ticker.isin(cut)]), "months": (Wk, Mo)}
P(f"weeks: train {SPL['weeks'][0].ticker.nunique()} / test {SPL['weeks'][1].ticker.nunique()} windows · months test {Mo.ticker.nunique()} windows\n")

KF = list(K.KF)
EX = ["lgap_bps", "sr10", "sr15"]
mk = lambda X: pd.get_dummies(X.mkt).reindex(columns=list(K.COMMS), fill_value=0).to_numpy(float)


# ---------------- candidates: fit(train) -> predict(test) ----------------
def offset_lr(lam, feats, iters=1500):
    def fit(tr):
        X = tr[feats].to_numpy(float); mu, sd = X.mean(0), np.maximum(X.std(0), 1e-4)
        w = K.fit_offset(np.clip((X - mu) / sd, -6, 6), tr.up.to_numpy(float), lg(tr.mid), None, lam, iters)
        return lambda te: K.sig(lg(te.mid) + np.clip((te[feats].to_numpy(float) - mu) / sd, -6, 6) @ w)
    return fit


def logit_blend(cols):
    """Plain logistic regression on log-odds inputs (Kalshi, spot fair value...) + intercept; Newton steps."""
    def fit(tr):
        X = np.column_stack([np.ones(len(tr))] + [lg(tr[c]) for c in cols]); y = tr.up.to_numpy(float); w = np.zeros(X.shape[1])
        for _ in range(25):
            p = K.sig(X @ w); W = p * (1 - p) + 1e-9
            w -= np.linalg.solve((X * W[:, None]).T @ X + 1e-3 * np.eye(len(w)), X.T @ (p - y))
        P(f"      blend weights {dict(zip(['b'] + list(cols), np.round(w, 3)))}")
        return lambda te: K.sig(np.column_stack([np.ones(len(te))] + [lg(te[c]) for c in cols]) @ w)
    return fit


def hgb(feats, **kw):
    def fit(tr):
        m = HistGradientBoostingClassifier(max_iter=kw.get("it", 400), learning_rate=kw.get("lr", 0.04), max_leaf_nodes=kw.get("leaves", 15),
                                           min_samples_leaf=kw.get("msl", 200), l2_regularization=1.0, early_stopping=True,
                                           validation_fraction=0.15, random_state=0)
        X = lambda d: np.column_stack([lg(d.mid), d[feats].to_numpy(float)])
        m.fit(X(tr), tr.up.to_numpy(int))
        return lambda te: m.predict_proba(X(te))[:, 1]
    return fit


CANDS = {
    "kalshi price only": None,
    "LIVE now: offset-LR lam .02": offset_lr(0.02, KF),
    "offset-LR lam .005": offset_lr(0.005, KF),
    "offset-LR lam .001": offset_lr(0.001, KF),
    "offset-LR lam .001 +spot extras": offset_lr(0.001, KF + EX + ["fair_sv60", "fair_svew"]),
    "spot fair value only (sv30)": "fair_sv30",
    "spot fair value only (sv60)": "fair_sv60",
    "spot fair value only (ewma)": "fair_svew",
    "blend kalshi+fair60": logit_blend(["mid", "fair_sv60"]),
    "blend kalshi+fair60+fairew": logit_blend(["mid", "fair_sv60", "fair_svew", "fair_mix"]),
    "boosted trees (all feats)": hgb(KF + EX + ["fair_sv60", "fair_svew", "fair_mix", "hour"]),
    "boosted trees deep": hgb(KF + EX + ["fair_sv60", "fair_svew", "fair_mix", "hour"], leaves=31, msl=100, it=800, lr=0.03),
}
# sv30 fair value (what the live sgap uses) reconstructed from sgap: logit(fair) = sgap + logit(mid)
D["fair_sv30"] = np.where(D.sok > 0, K.sig(D.sgap + lg(D.mid)), D.mid)
Wk, Mo = D[D.cl >= now - K.WEEKS_D * 86400], D[D.cl < now - K.WEEKS_D * 86400]
SPL = {"weeks": (Wk[~Wk.ticker.isin(cut)], Wk[Wk.ticker.isin(cut)]), "months": (Wk, Mo)}


def bets(te, p, edge=K.EDGE, tlmin=3, tlmax=12):
    y = te.up.to_numpy(float); up = p >= 0.5; ps = np.where(up, p, 1 - p); ask = np.where(up, te.ask, 1 - te.bid)
    B = pd.DataFrame(dict(tk=te.ticker.to_numpy(), ts=te.ts.to_numpy(), up=up, y=y, ask=ask, tl=te.tl.to_numpy(), e=ps - ask - K.fees(ask)))
    B = B[(B.e >= edge) & (B.ask <= K.KMAX) & (B.ask > 0.03) & (B.tl >= tlmin) & (B.tl <= tlmax)].sort_values("ts").groupby("tk").head(1)
    if not len(B): return 0, None, None
    won = (B.up == (B.y == 1)).astype(float); cost = B.ask + K.fees(B.ask)
    return len(B), won.mean(), (won - cost).sum() / cost.sum()


def score(te, p):
    y = te.up.to_numpy(float); bd = ((te.tl >= 10) & (te.tl <= 11.5)).to_numpy()
    acc = lambda m: float(((p[m] >= 0.5) == (y[m] == 1)).mean())
    conf = np.abs(p - 0.5) >= 0.30
    n, w, roi = bets(te, p)
    return dict(acc=acc(np.ones(len(y), bool)), ll=ll(y, p), acc_bd=acc(bd), ll_bd=ll(y[bd], p[bd]),
                conf_cov=float((conf & bd).sum() / max(bd.sum(), 1)), conf_acc=acc(conf & bd) if (conf & bd).any() else float("nan"),
                n=n, win=w, roi=roi)


RES = {}
for name, f in CANDS.items():
    P(f"== {name}")
    for sp, (tr, te) in SPL.items():
        if not len(te): continue
        try:
            if f is None: p = te.mid.to_numpy(float)
            elif isinstance(f, str): p = te[f].to_numpy(float)
            else: p = np.asarray(f(tr)(te), float)
        except Exception as e: P("   failed:", e); continue
        r = score(te, p); RES[(name, sp)] = r
        P(f"   {sp:6s} all: right {r['acc']:.1%} ll {r['ll']:.4f} | board(~11m): right {r['acc_bd']:.1%} ll {r['ll_bd']:.4f} | "
          f"≥80%-sure: {r['conf_cov']:.0%} of boards, right {r['conf_acc']:.1%} | bets {r['n']}: "
          + (f"won {r['win']:.0%} ROI {r['roi']:+.1%}" if r['n'] else "none"))

P("\n==== ranking by board-time log-loss (lower = sharper, honest odds), both test periods ====")
names = [n for n in CANDS if (n, "weeks") in RES and (n, "months") in RES]
for n in sorted(names, key=lambda n: RES[(n, "weeks")]["ll_bd"] + RES[(n, "months")]["ll_bd"]):
    a, b = RES[(n, "weeks")], RES[(n, "months")]
    P(f"{n:36s} weeks right {a['acc_bd']:.1%} ll {a['ll_bd']:.4f} roi {a['roi'] if a['roi'] is not None else float('nan'):+.1%} (n{a['n']}) | "
      f"months right {b['acc_bd']:.1%} ll {b['ll_bd']:.4f} roi {b['roi'] if b['roi'] is not None else float('nan'):+.1%} (n{b['n']})")

P("\n==== how accuracy depends on minutes left (Kalshi price only, all data) ====")
for lo, hi in ((11, 12), (9, 10), (6, 7), (3, 4)):
    m = (D.tl >= lo) & (D.tl < hi)
    P(f"  {lo}-{hi} min left: Kalshi favourite wins {((D.mid[m] >= 0.5) == (D.up[m] == 1)).mean():.1%}  ({m.sum():,} rows)")
P(f"\ndone in {(time.time() - t_start) / 60:.1f} min")
