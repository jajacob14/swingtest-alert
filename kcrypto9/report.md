# Kalshi crypto 15-min model report
Trained 2026-11-25 20:23 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 36940

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 598 windows · right 74% vs Kalshi 74% · logloss 0.5156 vs 0.5157 · edge bets 17: won 53%, ROI -2% | 1315 windows · right 76% vs Kalshi 76% · logloss 0.4789 vs 0.4813 · edge bets 24: won 71%, ROI +32% | — |
| XRP | 597 windows · right 75% vs Kalshi 74% · logloss 0.5134 vs 0.5134 · edge bets 8: won 50%, ROI -4% | 1316 windows · right 77% vs Kalshi 77% · logloss 0.4815 vs 0.4818 · edge bets 1: won 100%, ROI +56% | — |
| ETH | 598 windows · right 72% vs Kalshi 72% · logloss 0.5378 vs 0.537 · edge bets 10: won 80%, ROI +43% | 1320 windows · right 76% vs Kalshi 76% · logloss 0.4938 vs 0.4925 · edge bets 2: won 100%, ROI +106% | — |
| BTC | 598 windows · right 73% vs Kalshi 73% · logloss 0.5212 vs 0.5207 · edge bets 11: won 55%, ROI -2% | 1319 windows · right 74% vs Kalshi 73% · logloss 0.522 vs 0.5232 · edge bets 30: won 57%, ROI -3% | — |
| SOL | 597 windows · right 76% vs Kalshi 76% · logloss 0.4928 vs 0.4932 · edge bets 9: won 56%, ROI -0% | 1320 windows · right 76% vs Kalshi 76% · logloss 0.4898 vs 0.4894 · edge bets 2: won 50%, ROI -4% | — |
| NEAR | 597 windows · right 76% vs Kalshi 76% · logloss 0.4924 vs 0.4941 · edge bets 5: won 80%, ROI +52% | 1317 windows · right 75% vs Kalshi 74% · logloss 0.5032 vs 0.5047 · edge bets 8: won 88%, ROI +53% | — |
| HYPE | 598 windows · right 74% vs Kalshi 74% · logloss 0.5166 vs 0.519 · edge bets 15: won 53%, ROI -3% | 1317 windows · right 75% vs Kalshi 75% · logloss 0.5064 vs 0.5087 · edge bets 11: won 73%, ROI +32% | — |
| BNB | 598 windows · right 74% vs Kalshi 74% · logloss 0.5132 vs 0.5162 · edge bets 27: won 67%, ROI +19% | 1314 windows · right 76% vs Kalshi 76% · logloss 0.4867 vs 0.4894 · edge bets 60: won 67%, ROI +24% | ✅ |
| ZEC | 597 windows · right 74% vs Kalshi 74% · logloss 0.5017 vs 0.5015 · edge bets 13: won 62%, ROI +14% | 1163 windows · right 75% vs Kalshi 75% · logloss 0.5024 vs 0.5033 · edge bets 5: won 60%, ROI +11% | — |

**All weeks:** 5378 windows · right 74% vs Kalshi 74% · logloss 0.5116 vs 0.5123 · edge bets 115: won 61%, ROI +11%

**All months:** 11701 windows · right 76% vs Kalshi 75% · logloss 0.4961 vs 0.4972 · edge bets 143: won 67%, ROI +22%

| Month | Result |
|---|---|
| 2026-09 | 822 windows · right 76% vs Kalshi 76% · logloss 0.4796 vs 0.4813 · edge bets 9: won 67%, ROI +31% |
| 2026-10 | 8744 windows · right 76% vs Kalshi 75% · logloss 0.4947 vs 0.4954 · edge bets 113: won 66%, ROI +21% |
| 2026-11 | 2135 windows · right 75% vs Kalshi 75% · logloss 0.5083 vs 0.5106 · edge bets 21: won 71%, ROI +24% |

Strongest signals: `sgap` +0.092, `sr1` +0.040, `s_EU` +0.034, `s_US` -0.030, `dmid5` +0.030

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,403, target reached normally 23% | setups 5,952, target reached normally 22% | — |
| XRP | setups 2,533, target reached normally 25% | setups 5,932, target reached normally 21% | — |
| ETH | setups 2,406, target reached normally 26% | setups 5,437, target reached normally 23% | — |
| BTC | setups 2,384, target reached normally 22% | setups 5,293, target reached normally 21% | — |
| SOL | setups 2,448, target reached normally 21% | setups 5,685, target reached normally 22% | — |
| NEAR | setups 2,492, target reached normally 24% | setups 5,580, target reached normally 22% | — |
| HYPE | setups 2,385, target reached normally 22% | setups 5,582, target reached normally 24% | — |
| BNB | setups 2,431, target reached normally 23% | setups 5,518, target reached normally 22% | — |
| ZEC | setups 2,351, target reached normally 20% | setups 5,140, target reached normally 21% | — |

**All weeks:** setups 21,833, target reached normally 23%

**All months:** setups 50,119, target reached normally 22%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,017, target reached normally 58% | setups 12,236, target reached normally 55% | — |
| XRP | setups 5,713, target reached normally 57% | setups 12,412, target reached normally 55% | — |
| ETH | setups 5,987, target reached normally 58% | setups 12,809, target reached normally 56% | — |
| BTC | setups 5,980, target reached normally 58% | setups 13,261, target reached normally 57% | — |
| SOL | setups 5,923, target reached normally 56% | setups 12,464, target reached normally 56% | — |
| NEAR | setups 5,834, target reached normally 58% | setups 12,483, target reached normally 55% | — |
| HYPE | setups 5,919, target reached normally 57% | setups 12,377, target reached normally 56% | — |
| BNB | setups 5,717, target reached normally 57% | setups 12,375, target reached normally 54% | — |
| ZEC | setups 5,939, target reached normally 57% | setups 10,817, target reached normally 56% | — |
