# Kalshi crypto 15-min model report
Trained 2026-11-16 23:24 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 191706

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 75% vs Kalshi 75% · logloss 0.503 vs 0.5038 · edge bets 2: won 0%, ROI -100% | 2848 windows · right 75% vs Kalshi 75% · logloss 0.4992 vs 0.4993 · edge bets 8: won 38%, ROI -36% | — |
| ETH | 598 windows · right 74% vs Kalshi 74% · logloss 0.5128 vs 0.5112 | 2694 windows · right 77% vs Kalshi 77% · logloss 0.4746 vs 0.4742 · edge bets 1: won 0%, ROI -100% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.4889 vs 0.4901 · edge bets 1: won 0%, ROI -100% | 2694 windows · right 76% vs Kalshi 76% · logloss 0.4848 vs 0.485 | — |
| XRP | 598 windows · right 77% vs Kalshi 77% · logloss 0.4824 vs 0.4805 · edge bets 22: won 41%, ROI -25% | 2691 windows · right 76% vs Kalshi 76% · logloss 0.4788 vs 0.4791 · edge bets 32: won 53%, ROI -1% | — |
| DOGE | 597 windows · right 73% vs Kalshi 73% · logloss 0.5225 vs 0.5248 · edge bets 4: won 50%, ROI -18% | 2692 windows · right 76% vs Kalshi 76% · logloss 0.4783 vs 0.4797 · edge bets 4: won 75%, ROI +40% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.5019 vs 0.5021 · edge bets 29: won 38%, ROI -32%

**All months:** 13619 windows · right 76% vs Kalshi 76% · logloss 0.4834 vs 0.4837 · edge bets 45: won 51%, ROI -6%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4629 vs 0.4642 · edge bets 6: won 50%, ROI -7% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4716 vs 0.4719 · edge bets 18: won 50%, ROI -8% |
| 2026-10 | 7260 windows · right 75% vs Kalshi 75% · logloss 0.496 vs 0.4961 · edge bets 21: won 52%, ROI -5% |

Strongest signals: `sgap` +0.060, `s_EU` +0.028, `tleft` -0.027, `m_XRP` +0.020, `sr5` +0.020

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,432, target reached normally 23% | setups 11,419, target reached normally 19% | — |
| ETH | setups 2,419, target reached normally 27% | setups 11,376, target reached normally 20% | — |
| SOL | setups 2,499, target reached normally 23% | setups 11,564, target reached normally 21% | — |
| XRP | setups 2,555, target reached normally 22% | setups 11,845, target reached normally 20% | — |
| DOGE | setups 2,565, target reached normally 24% | setups 11,571, target reached normally 20% | — |

**All weeks:** setups 12,470, target reached normally 24%

**All months:** setups 57,775, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,835, target reached normally 58% | setups 29,393, target reached normally 55% | — |
| ETH | setups 5,698, target reached normally 58% | setups 26,056, target reached normally 54% | — |
| SOL | setups 5,739, target reached normally 56% | setups 25,872, target reached normally 56% | — |
| XRP | setups 5,565, target reached normally 54% | setups 26,002, target reached normally 55% | — |
| DOGE | setups 5,558, target reached normally 58% | setups 25,761, target reached normally 56% | — |
