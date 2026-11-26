# Kalshi crypto 15-min model report
Trained 2026-11-26 07:54 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 46655

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 598 windows · right 74% vs Kalshi 74% · logloss 0.5216 vs 0.5211 · edge bets 28: won 54%, ROI -0% | 1353 windows · right 76% vs Kalshi 76% · logloss 0.4773 vs 0.4796 · edge bets 28: won 64%, ROI +18% | — |
| XRP | 598 windows · right 75% vs Kalshi 74% · logloss 0.5141 vs 0.5133 · edge bets 11: won 55%, ROI +2% | 1354 windows · right 76% vs Kalshi 76% · logloss 0.4835 vs 0.4837 · edge bets 1: won 100%, ROI +56% | — |
| ETH | 597 windows · right 72% vs Kalshi 73% · logloss 0.5308 vs 0.5297 · edge bets 12: won 75%, ROI +35% | 1358 windows · right 76% vs Kalshi 76% · logloss 0.4943 vs 0.4929 · edge bets 6: won 67%, ROI +27% | — |
| BTC | 598 windows · right 73% vs Kalshi 73% · logloss 0.5196 vs 0.5186 · edge bets 16: won 56%, ROI -1% | 1357 windows · right 74% vs Kalshi 74% · logloss 0.5172 vs 0.5183 · edge bets 29: won 55%, ROI -5% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.4991 vs 0.4993 · edge bets 12: won 42%, ROI -26% | 1358 windows · right 76% vs Kalshi 76% · logloss 0.4915 vs 0.491 · edge bets 3: won 33%, ROI -38% | — |
| NEAR | 597 windows · right 76% vs Kalshi 76% · logloss 0.4925 vs 0.4942 · edge bets 11: won 64%, ROI +19% | 1355 windows · right 74% vs Kalshi 74% · logloss 0.5065 vs 0.508 · edge bets 8: won 88%, ROI +53% | — |
| HYPE | 597 windows · right 74% vs Kalshi 74% · logloss 0.5136 vs 0.5156 · edge bets 18: won 50%, ROI -11% | 1355 windows · right 75% vs Kalshi 75% · logloss 0.5032 vs 0.5052 · edge bets 9: won 67%, ROI +23% | — |
| BNB | 597 windows · right 74% vs Kalshi 73% · logloss 0.5161 vs 0.5198 · edge bets 31: won 71%, ROI +30% | 1352 windows · right 76% vs Kalshi 76% · logloss 0.4862 vs 0.4891 · edge bets 67: won 67%, ROI +25% | ✅ |
| ZEC | 598 windows · right 75% vs Kalshi 75% · logloss 0.4937 vs 0.4929 · edge bets 18: won 56%, ROI +1% | 1201 windows · right 75% vs Kalshi 75% · logloss 0.5007 vs 0.5016 · edge bets 5: won 60%, ROI +12% | — |

**All weeks:** 5378 windows · right 74% vs Kalshi 74% · logloss 0.5112 vs 0.5116 · edge bets 157: won 59%, ROI +7%

**All months:** 12043 windows · right 76% vs Kalshi 76% · logloss 0.4956 vs 0.4966 · edge bets 156: won 65%, ROI +18%

| Month | Result |
|---|---|
| 2026-09 | 822 windows · right 76% vs Kalshi 76% · logloss 0.4799 vs 0.4813 · edge bets 10: won 60%, ROI +15% |
| 2026-10 | 8744 windows · right 76% vs Kalshi 75% · logloss 0.4947 vs 0.4954 · edge bets 122: won 64%, ROI +17% |
| 2026-11 | 2477 windows · right 75% vs Kalshi 75% · logloss 0.5041 vs 0.506 · edge bets 24: won 71%, ROI +25% |

Strongest signals: `sgap` +0.088, `sr1` +0.041, `s_EU` +0.035, `dmid5` +0.032, `tleft` -0.032

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,332, target reached normally 23% | setups 6,144, target reached normally 22% | — |
| XRP | setups 2,528, target reached normally 26% | setups 6,118, target reached normally 21% | — |
| ETH | setups 2,386, target reached normally 24% | setups 5,632, target reached normally 23% | — |
| BTC | setups 2,344, target reached normally 21% | setups 5,491, target reached normally 21% | — |
| SOL | setups 2,424, target reached normally 21% | setups 5,866, target reached normally 22% | — |
| NEAR | setups 2,470, target reached normally 24% | setups 5,776, target reached normally 22% | — |
| HYPE | setups 2,352, target reached normally 22% | setups 5,766, target reached normally 24% | — |
| BNB | setups 2,378, target reached normally 22% | setups 5,704, target reached normally 22% | — |
| ZEC | setups 2,381, target reached normally 20% | setups 5,332, target reached normally 21% | — |

**All weeks:** setups 21,595, target reached normally 23%

**All months:** setups 51,829, target reached normally 22%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,106, target reached normally 58% | setups 12,596, target reached normally 55% | — |
| XRP | setups 5,745, target reached normally 57% | setups 12,733, target reached normally 55% | — |
| ETH | setups 6,035, target reached normally 58% | setups 13,136, target reached normally 56% | — |
| BTC | setups 6,037, target reached normally 57% | setups 13,594, target reached normally 56% | — |
| SOL | setups 5,939, target reached normally 56% | setups 12,812, target reached normally 56% | — |
| NEAR | setups 5,800, target reached normally 58% | setups 12,826, target reached normally 56% | — |
| HYPE | setups 5,961, target reached normally 57% | setups 12,709, target reached normally 56% | — |
| BNB | setups 5,787, target reached normally 57% | setups 12,706, target reached normally 54% | — |
| ZEC | setups 5,869, target reached normally 56% | setups 11,144, target reached normally 56% | — |
