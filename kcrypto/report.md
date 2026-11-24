# Kalshi crypto 15-min model report
Trained 2026-11-23 23:06 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 343000

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5113 vs 0.5119 · edge bets 2: won 50%, ROI -9% | 3511 windows · right 75% vs Kalshi 75% · logloss 0.5026 vs 0.503 · edge bets 6: won 50%, ROI -12% | — |
| ETH | 597 windows · right 74% vs Kalshi 74% · logloss 0.5099 vs 0.5081 | 3357 windows · right 77% vs Kalshi 77% · logloss 0.4795 vs 0.4789 | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.5088 vs 0.5087 · edge bets 12: won 33%, ROI -41% | 3357 windows · right 76% vs Kalshi 76% · logloss 0.487 vs 0.4872 | — |
| XRP | 598 windows · right 75% vs Kalshi 75% · logloss 0.5169 vs 0.5145 · edge bets 19: won 32%, ROI -39% | 3354 windows · right 76% vs Kalshi 76% · logloss 0.4834 vs 0.4838 · edge bets 7: won 57%, ROI -1% | — |
| DOGE | 598 windows · right 76% vs Kalshi 76% · logloss 0.4957 vs 0.495 · edge bets 18: won 67%, ROI +26% | 3355 windows · right 76% vs Kalshi 76% · logloss 0.4773 vs 0.4781 · edge bets 20: won 65%, ROI +22% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.5085 vs 0.5076 · edge bets 51: won 45%, ROI -16%

**All months:** 16934 windows · right 76% vs Kalshi 76% · logloss 0.4862 vs 0.4864 · edge bets 33: won 61%, ROI +11%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4636 vs 0.4642 · edge bets 3: won 67%, ROI +30% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4716 vs 0.4719 · edge bets 12: won 50%, ROI -12% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4969 vs 0.4969 · edge bets 16: won 69%, ROI +27% |
| 2026-11 | 1045 windows · right 76% vs Kalshi 75% · logloss 0.4929 vs 0.4941 · edge bets 2: won 50%, ROI -2% |

Strongest signals: `sgap` +0.058, `s_EU` +0.031, `dmid5` +0.030, `sr1` +0.021, `s_US` -0.017

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,439, target reached normally 23% | setups 14,141, target reached normally 20% | — |
| ETH | setups 2,464, target reached normally 24% | setups 14,153, target reached normally 20% | — |
| SOL | setups 2,494, target reached normally 22% | setups 14,343, target reached normally 21% | — |
| XRP | setups 2,543, target reached normally 26% | setups 14,647, target reached normally 20% | — |
| DOGE | setups 2,430, target reached normally 22% | setups 14,472, target reached normally 20% | — |

**All weeks:** setups 12,370, target reached normally 23%

**All months:** setups 71,756, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,896, target reached normally 58% | setups 36,109, target reached normally 56% | — |
| ETH | setups 5,838, target reached normally 56% | setups 32,460, target reached normally 55% | — |
| SOL | setups 5,835, target reached normally 56% | setups 32,041, target reached normally 56% | — |
| XRP | setups 5,589, target reached normally 56% | setups 32,300, target reached normally 55% | — |
| DOGE | setups 5,840, target reached normally 56% | setups 31,999, target reached normally 56% | — |
