# Kalshi crypto 15-min model report
Trained 2026-11-10 06:07 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 50167

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 75% vs Kalshi 75% · logloss 0.4982 vs 0.4989 · edge bets 33: won 76%, ROI +29% | 2211 windows · right 76% vs Kalshi 76% · logloss 0.4927 vs 0.4925 · edge bets 28: won 61%, ROI -1% | — |
| ETH | 597 windows · right 75% vs Kalshi 75% · logloss 0.4994 vs 0.4991 · edge bets 16: won 50%, ROI -11% | 2057 windows · right 78% vs Kalshi 78% · logloss 0.4601 vs 0.4594 · edge bets 3: won 33%, ROI -43% | — |
| SOL | 598 windows · right 74% vs Kalshi 74% · logloss 0.5239 vs 0.5236 · edge bets 24: won 54%, ROI +2% | 2057 windows · right 77% vs Kalshi 77% · logloss 0.4779 vs 0.4777 · edge bets 5: won 40%, ROI -33% | — |
| XRP | 598 windows · right 74% vs Kalshi 74% · logloss 0.5262 vs 0.5239 · edge bets 14: won 50%, ROI -10% | 2054 windows · right 77% vs Kalshi 77% · logloss 0.4674 vs 0.4681 · edge bets 32: won 56%, ROI +6% | — |
| DOGE | 597 windows · right 76% vs Kalshi 76% · logloss 0.4921 vs 0.4919 · edge bets 48: won 62%, ROI +16% | 2055 windows · right 78% vs Kalshi 78% · logloss 0.461 vs 0.4622 · edge bets 15: won 60%, ROI +12% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.5078 vs 0.5074 · edge bets 135: won 62%, ROI +11%

**All months:** 10434 windows · right 77% vs Kalshi 77% · logloss 0.4723 vs 0.4724 · edge bets 83: won 57%, ROI +0%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4634 vs 0.4642 · edge bets 13: won 54%, ROI -1% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4714 vs 0.4719 · edge bets 34: won 65%, ROI +13% |
| 2026-10 | 4075 windows · right 77% vs Kalshi 77% · logloss 0.4768 vs 0.4763 · edge bets 36: won 50%, ROI -12% |

Strongest signals: `sgap` +0.060, `s_EU` +0.028, `dmid1` -0.027, `dmid5` +0.026, `m_XRP` +0.026

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,427, target reached normally 22% | setups 8,982, target reached normally 19% | — |
| ETH | setups 2,499, target reached normally 22% | setups 8,883, target reached normally 18% | — |
| SOL | setups 2,535, target reached normally 24% | setups 9,044, target reached normally 20% | — |
| XRP | setups 2,505, target reached normally 24% | setups 9,137, target reached normally 19% | — |
| DOGE | setups 2,637, target reached normally 21% | setups 8,987, target reached normally 19% | — |

**All weeks:** setups 12,603, target reached normally 23%

**All months:** setups 45,033, target reached normally 19%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 6,005, target reached normally 56% | setups 22,860, target reached normally 55% | — |
| ETH | setups 5,820, target reached normally 56% | setups 19,750, target reached normally 53% | — |
| SOL | setups 5,715, target reached normally 57% | setups 19,612, target reached normally 55% | — |
| XRP | setups 5,575, target reached normally 56% | setups 19,816, target reached normally 54% | — |
| DOGE | setups 5,699, target reached normally 55% | setups 19,431, target reached normally 55% | — |
