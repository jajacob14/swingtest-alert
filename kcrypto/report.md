# Kalshi crypto 15-min model report
Trained 2026-11-22 22:20 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 319935

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5056 vs 0.5058 · edge bets 1: won 100%, ROI +79% | 3412 windows · right 75% vs Kalshi 75% · logloss 0.5016 vs 0.5019 · edge bets 12: won 50%, ROI -17% | — |
| ETH | 598 windows · right 74% vs Kalshi 74% · logloss 0.5089 vs 0.5073 | 3258 windows · right 77% vs Kalshi 77% · logloss 0.4776 vs 0.4771 · edge bets 1: won 0%, ROI -100% | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.506 vs 0.5047 · edge bets 17: won 53%, ROI -10% | 3258 windows · right 76% vs Kalshi 76% · logloss 0.4874 vs 0.4876 | — |
| XRP | 598 windows · right 75% vs Kalshi 75% · logloss 0.5112 vs 0.5095 · edge bets 14: won 43%, ROI -22% | 3255 windows · right 76% vs Kalshi 76% · logloss 0.4811 vs 0.4814 · edge bets 15: won 60%, ROI +10% | — |
| DOGE | 597 windows · right 77% vs Kalshi 76% · logloss 0.4848 vs 0.4846 · edge bets 15: won 67%, ROI +25% | 3256 windows · right 77% vs Kalshi 76% · logloss 0.4766 vs 0.4777 · edge bets 26: won 69%, ROI +29% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.5032 vs 0.5024 · edge bets 47: won 55%, ROI -1%

**All months:** 16439 windows · right 76% vs Kalshi 76% · logloss 0.4851 vs 0.4854 · edge bets 54: won 61%, ROI +11%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4631 vs 0.4642 · edge bets 6: won 50%, ROI -3% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4715 vs 0.4719 · edge bets 16: won 44%, ROI -22% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4968 vs 0.4969 · edge bets 29: won 72%, ROI +31% |
| 2026-11 | 550 windows · right 77% vs Kalshi 77% · logloss 0.4683 vs 0.4684 · edge bets 3: won 67%, ROI +15% |

Strongest signals: `sgap` +0.056, `dmid5` +0.033, `s_EU` +0.028, `sr1` +0.022, `tleft` -0.019

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,472, target reached normally 22% | setups 13,734, target reached normally 20% | — |
| ETH | setups 2,454, target reached normally 24% | setups 13,729, target reached normally 20% | — |
| SOL | setups 2,460, target reached normally 22% | setups 13,905, target reached normally 21% | — |
| XRP | setups 2,540, target reached normally 26% | setups 14,228, target reached normally 20% | — |
| DOGE | setups 2,450, target reached normally 21% | setups 14,044, target reached normally 20% | — |

**All weeks:** setups 12,376, target reached normally 23%

**All months:** setups 69,640, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,896, target reached normally 57% | setups 35,069, target reached normally 56% | — |
| ETH | setups 5,801, target reached normally 56% | setups 31,530, target reached normally 55% | — |
| SOL | setups 5,804, target reached normally 56% | setups 31,134, target reached normally 56% | — |
| XRP | setups 5,495, target reached normally 57% | setups 31,322, target reached normally 55% | — |
| DOGE | setups 5,729, target reached normally 55% | setups 31,081, target reached normally 56% | — |
