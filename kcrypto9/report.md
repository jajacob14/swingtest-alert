# Kalshi crypto 15-min model report
Trained 2026-11-27 15:22 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 78676

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 597 windows · right 74% vs Kalshi 74% · logloss 0.5212 vs 0.5214 · edge bets 28: won 50%, ROI -7% | 1479 windows · right 76% vs Kalshi 76% · logloss 0.4818 vs 0.484 · edge bets 14: won 64%, ROI +22% | — |
| XRP | 598 windows · right 74% vs Kalshi 74% · logloss 0.5153 vs 0.5145 · edge bets 16: won 38%, ROI -28% | 1480 windows · right 76% vs Kalshi 76% · logloss 0.4879 vs 0.4881 | — |
| ETH | 597 windows · right 73% vs Kalshi 74% · logloss 0.528 vs 0.527 · edge bets 15: won 67%, ROI +26% | 1484 windows · right 76% vs Kalshi 76% · logloss 0.4967 vs 0.4957 · edge bets 1: won 100%, ROI +96% | — |
| BTC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5179 vs 0.5169 · edge bets 23: won 48%, ROI -15% | 1483 windows · right 74% vs Kalshi 73% · logloss 0.5228 vs 0.5246 · edge bets 21: won 67%, ROI +18% | — |
| SOL | 598 windows · right 76% vs Kalshi 76% · logloss 0.4962 vs 0.4962 · edge bets 14: won 71%, ROI +27% | 1484 windows · right 76% vs Kalshi 76% · logloss 0.4912 vs 0.491 · edge bets 1: won 0%, ROI -100% | — |
| NEAR | 598 windows · right 76% vs Kalshi 76% · logloss 0.4921 vs 0.4926 · edge bets 10: won 60%, ROI +16% | 1481 windows · right 74% vs Kalshi 74% · logloss 0.5067 vs 0.5081 · edge bets 4: won 75%, ROI +37% | — |
| HYPE | 597 windows · right 74% vs Kalshi 74% · logloss 0.513 vs 0.5145 · edge bets 19: won 47%, ROI -15% | 1481 windows · right 75% vs Kalshi 75% · logloss 0.5052 vs 0.5068 · edge bets 3: won 100%, ROI +73% | — |
| BNB | 598 windows · right 74% vs Kalshi 74% · logloss 0.5145 vs 0.5161 · edge bets 31: won 74%, ROI +34% | 1478 windows · right 76% vs Kalshi 76% · logloss 0.491 vs 0.494 · edge bets 30: won 67%, ROI +21% | ✅ |
| ZEC | 597 windows · right 75% vs Kalshi 75% · logloss 0.4967 vs 0.4963 · edge bets 21: won 57%, ROI +3% | 1327 windows · right 75% vs Kalshi 75% · logloss 0.5032 vs 0.5043 | — |

**All weeks:** 5378 windows · right 74% vs Kalshi 74% · logloss 0.5106 vs 0.5106 · edge bets 177: won 57%, ROI +4%

**All months:** 13177 windows · right 75% vs Kalshi 75% · logloss 0.4985 vs 0.4996 · edge bets 74: won 68%, ROI +23%

| Month | Result |
|---|---|
| 2026-09 | 822 windows · right 76% vs Kalshi 76% · logloss 0.4798 vs 0.4813 · edge bets 6: won 50%, ROI -1% |
| 2026-10 | 8744 windows · right 76% vs Kalshi 75% · logloss 0.4947 vs 0.4954 · edge bets 50: won 70%, ROI +26% |
| 2026-11 | 3611 windows · right 74% vs Kalshi 74% · logloss 0.5121 vs 0.5141 · edge bets 18: won 67%, ROI +20% |

Strongest signals: `sgap` +0.073, `sr1` +0.037, `dmid5` +0.035, `s_US` -0.033, `s_EU` +0.032

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,272, target reached normally 23% | setups 6,636, target reached normally 22% | — |
| XRP | setups 2,510, target reached normally 24% | setups 6,621, target reached normally 21% | — |
| ETH | setups 2,318, target reached normally 23% | setups 6,118, target reached normally 23% | — |
| BTC | setups 2,268, target reached normally 21% | setups 5,984, target reached normally 21% | — |
| SOL | setups 2,427, target reached normally 23% | setups 6,388, target reached normally 22% | — |
| NEAR | setups 2,483, target reached normally 24% | setups 6,308, target reached normally 22% | — |
| HYPE | setups 2,298, target reached normally 21% | setups 6,298, target reached normally 24% | — |
| BNB | setups 2,349, target reached normally 23% | setups 6,177, target reached normally 22% | — |
| ZEC | setups 2,375, target reached normally 19% | setups 5,883, target reached normally 22% | — |

**All weeks:** setups 21,300, target reached normally 22%

**All months:** setups 56,413, target reached normally 22%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,262, target reached normally 59% | setups 13,893, target reached normally 56% | — |
| XRP | setups 5,861, target reached normally 57% | setups 13,980, target reached normally 55% | — |
| ETH | setups 6,127, target reached normally 58% | setups 14,423, target reached normally 57% | — |
| BTC | setups 6,154, target reached normally 58% | setups 14,917, target reached normally 57% | — |
| SOL | setups 6,026, target reached normally 55% | setups 14,093, target reached normally 56% | — |
| NEAR | setups 5,898, target reached normally 57% | setups 14,098, target reached normally 56% | — |
| HYPE | setups 6,096, target reached normally 58% | setups 13,927, target reached normally 56% | — |
| BNB | setups 5,935, target reached normally 57% | setups 13,992, target reached normally 55% | — |
| ZEC | setups 5,902, target reached normally 56% | setups 12,343, target reached normally 56% | — |
