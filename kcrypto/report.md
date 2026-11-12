# Kalshi crypto 15-min model report
Trained 2026-11-12 04:14 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 84927

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 75% vs Kalshi 75% · logloss 0.4981 vs 0.4973 · edge bets 41: won 66%, ROI +14% | 2387 windows · right 75% vs Kalshi 75% · logloss 0.4961 vs 0.496 · edge bets 15: won 67%, ROI +9% | — |
| ETH | 598 windows · right 75% vs Kalshi 76% · logloss 0.5022 vs 0.5012 · edge bets 10: won 30%, ROI -46% | 2233 windows · right 78% vs Kalshi 78% · logloss 0.464 vs 0.4637 · edge bets 1: won 0%, ROI -100% | — |
| SOL | 599 windows · right 75% vs Kalshi 74% · logloss 0.505 vs 0.5056 · edge bets 25: won 52%, ROI -1% | 2233 windows · right 77% vs Kalshi 77% · logloss 0.4811 vs 0.481 · edge bets 3: won 0%, ROI -100% | — |
| XRP | 599 windows · right 74% vs Kalshi 74% · logloss 0.5228 vs 0.5195 · edge bets 19: won 68%, ROI +25% | 2230 windows · right 77% vs Kalshi 77% · logloss 0.4689 vs 0.4697 · edge bets 16: won 44%, ROI -20% | — |
| DOGE | 599 windows · right 77% vs Kalshi 77% · logloss 0.4761 vs 0.4752 · edge bets 33: won 64%, ROI +23% | 2231 windows · right 77% vs Kalshi 77% · logloss 0.4679 vs 0.4691 · edge bets 3: won 100%, ROI +84% | — |

**All weeks:** 2993 windows · right 75% vs Kalshi 75% · logloss 0.5008 vs 0.4997 · edge bets 128: won 60%, ROI +10%

**All months:** 11314 windows · right 77% vs Kalshi 77% · logloss 0.476 vs 0.4763 · edge bets 38: won 53%, ROI -8%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4636 vs 0.4642 · edge bets 6: won 50%, ROI -7% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4715 vs 0.4719 · edge bets 20: won 55%, ROI -4% |
| 2026-10 | 4955 windows · right 76% vs Kalshi 76% · logloss 0.4846 vs 0.4846 · edge bets 12: won 50%, ROI -16% |

Strongest signals: `sgap` +0.061, `s_EU` +0.033, `dmid5` +0.027, `tleft` -0.026, `sr1` +0.023

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,424, target reached normally 23% | setups 9,675, target reached normally 19% | — |
| ETH | setups 2,495, target reached normally 23% | setups 9,611, target reached normally 19% | — |
| SOL | setups 2,527, target reached normally 22% | setups 9,719, target reached normally 21% | — |
| XRP | setups 2,526, target reached normally 23% | setups 9,874, target reached normally 20% | — |
| DOGE | setups 2,674, target reached normally 21% | setups 9,708, target reached normally 20% | — |

**All weeks:** setups 12,646, target reached normally 23%

**All months:** setups 48,587, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,943, target reached normally 56% | setups 24,645, target reached normally 55% | — |
| ETH | setups 5,828, target reached normally 55% | setups 21,448, target reached normally 54% | — |
| SOL | setups 5,716, target reached normally 57% | setups 21,398, target reached normally 56% | — |
| XRP | setups 5,584, target reached normally 55% | setups 21,532, target reached normally 55% | — |
| DOGE | setups 5,605, target reached normally 53% | setups 21,181, target reached normally 55% | — |
