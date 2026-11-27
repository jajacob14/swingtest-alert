# Kalshi crypto 15-min model report
Trained 2026-11-26 19:25 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 58424

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 598 windows · right 73% vs Kalshi 73% · logloss 0.5283 vs 0.5284 · edge bets 32: won 44%, ROI -20% | 1399 windows · right 76% vs Kalshi 76% · logloss 0.4814 vs 0.4839 · edge bets 22: won 68%, ROI +28% | — |
| XRP | 598 windows · right 74% vs Kalshi 74% · logloss 0.5172 vs 0.5172 · edge bets 10: won 50%, ROI -5% | 1400 windows · right 77% vs Kalshi 77% · logloss 0.4827 vs 0.4828 · edge bets 2: won 50%, ROI -26% | — |
| ETH | 597 windows · right 73% vs Kalshi 74% · logloss 0.5233 vs 0.5221 · edge bets 13: won 62%, ROI +14% | 1404 windows · right 76% vs Kalshi 76% · logloss 0.4979 vs 0.4966 · edge bets 3: won 100%, ROI +90% | — |
| BTC | 597 windows · right 73% vs Kalshi 73% · logloss 0.5202 vs 0.5191 · edge bets 18: won 50%, ROI -10% | 1403 windows · right 74% vs Kalshi 73% · logloss 0.5213 vs 0.5227 · edge bets 24: won 58%, ROI +2% | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.5037 vs 0.5036 · edge bets 11: won 46%, ROI -18% | 1404 windows · right 76% vs Kalshi 76% · logloss 0.4914 vs 0.4911 · edge bets 1: won 0%, ROI -100% | — |
| NEAR | 598 windows · right 75% vs Kalshi 75% · logloss 0.5002 vs 0.502 · edge bets 7: won 57%, ROI +13% | 1401 windows · right 74% vs Kalshi 74% · logloss 0.5075 vs 0.509 · edge bets 7: won 86%, ROI +49% | — |
| HYPE | 597 windows · right 73% vs Kalshi 73% · logloss 0.5186 vs 0.5202 · edge bets 15: won 47%, ROI -15% | 1401 windows · right 75% vs Kalshi 75% · logloss 0.5047 vs 0.5065 · edge bets 7: won 71%, ROI +27% | — |
| BNB | 598 windows · right 74% vs Kalshi 74% · logloss 0.5093 vs 0.5117 · edge bets 27: won 78%, ROI +43% | 1398 windows · right 76% vs Kalshi 76% · logloss 0.4865 vs 0.4897 · edge bets 55: won 71%, ROI +30% | ✅ |
| ZEC | 598 windows · right 74% vs Kalshi 74% · logloss 0.495 vs 0.4952 · edge bets 15: won 67%, ROI +18% | 1247 windows · right 75% vs Kalshi 75% · logloss 0.5024 vs 0.5033 · edge bets 3: won 67%, ROI +30% | — |

**All weeks:** 5378 windows · right 74% vs Kalshi 74% · logloss 0.5129 vs 0.5133 · edge bets 148: won 56%, ROI +3%

**All months:** 12457 windows · right 75% vs Kalshi 75% · logloss 0.4973 vs 0.4984 · edge bets 124: won 68%, ROI +24%

| Month | Result |
|---|---|
| 2026-09 | 822 windows · right 76% vs Kalshi 76% · logloss 0.4799 vs 0.4813 · edge bets 8: won 62%, ROI +22% |
| 2026-10 | 8744 windows · right 76% vs Kalshi 75% · logloss 0.4946 vs 0.4954 · edge bets 94: won 70%, ROI +27% |
| 2026-11 | 2891 windows · right 75% vs Kalshi 75% · logloss 0.5104 vs 0.5125 · edge bets 22: won 64%, ROI +12% |

Strongest signals: `sgap` +0.082, `sr1` +0.041, `dmid5` +0.037, `tleft` -0.034, `s_EU` +0.034

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,317, target reached normally 23% | setups 6,315, target reached normally 22% | — |
| XRP | setups 2,539, target reached normally 25% | setups 6,292, target reached normally 21% | — |
| ETH | setups 2,368, target reached normally 24% | setups 5,796, target reached normally 23% | — |
| BTC | setups 2,296, target reached normally 21% | setups 5,658, target reached normally 21% | — |
| SOL | setups 2,412, target reached normally 22% | setups 6,052, target reached normally 22% | — |
| NEAR | setups 2,476, target reached normally 24% | setups 5,965, target reached normally 22% | — |
| HYPE | setups 2,329, target reached normally 21% | setups 5,953, target reached normally 24% | — |
| BNB | setups 2,390, target reached normally 22% | setups 5,889, target reached normally 22% | — |
| ZEC | setups 2,404, target reached normally 19% | setups 5,564, target reached normally 22% | — |

**All weeks:** setups 21,531, target reached normally 22%

**All months:** setups 53,484, target reached normally 22%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,205, target reached normally 59% | setups 13,083, target reached normally 56% | — |
| XRP | setups 5,835, target reached normally 57% | setups 13,204, target reached normally 55% | — |
| ETH | setups 6,105, target reached normally 57% | setups 13,609, target reached normally 57% | — |
| BTC | setups 6,155, target reached normally 57% | setups 14,083, target reached normally 57% | — |
| SOL | setups 6,023, target reached normally 56% | setups 13,296, target reached normally 56% | — |
| NEAR | setups 5,878, target reached normally 57% | setups 13,323, target reached normally 56% | — |
| HYPE | setups 6,042, target reached normally 57% | setups 13,182, target reached normally 56% | — |
| BNB | setups 5,860, target reached normally 57% | setups 13,165, target reached normally 55% | — |
| ZEC | setups 5,878, target reached normally 56% | setups 11,566, target reached normally 56% | — |
