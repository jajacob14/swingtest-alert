# Kalshi crypto 15-min model report
Trained 2026-11-25 00:51 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 18885

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 598 windows · right 74% vs Kalshi 74% · logloss 0.5135 vs 0.5133 · edge bets 18: won 44%, ROI -19% | 1237 windows · right 77% vs Kalshi 77% · logloss 0.4733 vs 0.4756 · edge bets 30: won 67%, ROI +24% | — |
| XRP | 597 windows · right 74% vs Kalshi 74% · logloss 0.5243 vs 0.5238 · edge bets 6: won 50%, ROI -1% | 1238 windows · right 77% vs Kalshi 77% · logloss 0.4777 vs 0.4782 · edge bets 1: won 100%, ROI +56% | — |
| ETH | 598 windows · right 73% vs Kalshi 73% · logloss 0.5283 vs 0.5266 · edge bets 4: won 50%, ROI -8% | 1242 windows · right 76% vs Kalshi 76% · logloss 0.4914 vs 0.4901 · edge bets 2: won 100%, ROI +106% | — |
| BTC | 598 windows · right 73% vs Kalshi 73% · logloss 0.5197 vs 0.5206 · edge bets 8: won 62%, ROI +9% | 1241 windows · right 74% vs Kalshi 74% · logloss 0.5216 vs 0.5224 · edge bets 31: won 58%, ROI -1% | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.4975 vs 0.4979 · edge bets 1: won 0%, ROI -100% | 1242 windows · right 77% vs Kalshi 76% · logloss 0.4859 vs 0.4855 · edge bets 4: won 50%, ROI -7% | — |
| NEAR | 597 windows · right 76% vs Kalshi 75% · logloss 0.4956 vs 0.4978 · edge bets 8: won 62%, ROI +14% | 1239 windows · right 75% vs Kalshi 75% · logloss 0.5023 vs 0.5043 · edge bets 10: won 80%, ROI +38% | — |
| HYPE | 598 windows · right 74% vs Kalshi 74% · logloss 0.5201 vs 0.5223 · edge bets 9: won 56%, ROI -6% | 1239 windows · right 75% vs Kalshi 75% · logloss 0.505 vs 0.5075 · edge bets 14: won 79%, ROI +44% | — |
| BNB | 597 windows · right 75% vs Kalshi 74% · logloss 0.5065 vs 0.5089 · edge bets 19: won 63%, ROI +12% | 1236 windows · right 76% vs Kalshi 76% · logloss 0.4882 vs 0.491 · edge bets 67: won 67%, ROI +23% | ✅ |
| ZEC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5054 vs 0.5055 · edge bets 6: won 50%, ROI -12% | 1085 windows · right 75% vs Kalshi 75% · logloss 0.5038 vs 0.5037 · edge bets 5: won 60%, ROI +6% | — |

**All weeks:** 5378 windows · right 74% vs Kalshi 74% · logloss 0.5123 vs 0.513 · edge bets 79: won 54%, ROI -2%

**All months:** 10999 windows · right 76% vs Kalshi 76% · logloss 0.4943 vs 0.4953 · edge bets 164: won 67%, ROI +21%

| Month | Result |
|---|---|
| 2026-09 | 822 windows · right 76% vs Kalshi 76% · logloss 0.4798 vs 0.4813 · edge bets 10: won 60%, ROI +18% |
| 2026-10 | 8744 windows · right 76% vs Kalshi 75% · logloss 0.4948 vs 0.4954 · edge bets 132: won 67%, ROI +22% |
| 2026-11 | 1433 windows · right 76% vs Kalshi 76% · logloss 0.4994 vs 0.5029 · edge bets 22: won 68%, ROI +17% |

Strongest signals: `sgap` +0.094, `sr1` +0.043, `s_EU` +0.035, `tleft` -0.031, `dmid5` +0.030

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,396, target reached normally 23% | setups 5,608, target reached normally 21% | — |
| XRP | setups 2,518, target reached normally 27% | setups 5,615, target reached normally 21% | — |
| ETH | setups 2,417, target reached normally 25% | setups 5,129, target reached normally 22% | — |
| BTC | setups 2,417, target reached normally 23% | setups 4,977, target reached normally 20% | — |
| SOL | setups 2,452, target reached normally 21% | setups 5,354, target reached normally 21% | — |
| NEAR | setups 2,509, target reached normally 24% | setups 5,233, target reached normally 21% | — |
| HYPE | setups 2,430, target reached normally 23% | setups 5,276, target reached normally 24% | — |
| BNB | setups 2,474, target reached normally 23% | setups 5,176, target reached normally 22% | — |
| ZEC | setups 2,333, target reached normally 21% | setups 4,840, target reached normally 22% | — |

**All weeks:** setups 21,946, target reached normally 23%

**All months:** setups 47,208, target reached normally 22%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 5,966, target reached normally 57% | setups 11,479, target reached normally 55% | — |
| XRP | setups 5,696, target reached normally 57% | setups 11,655, target reached normally 55% | — |
| ETH | setups 5,981, target reached normally 57% | setups 12,042, target reached normally 56% | — |
| BTC | setups 5,946, target reached normally 58% | setups 12,476, target reached normally 56% | — |
| SOL | setups 5,903, target reached normally 55% | setups 11,707, target reached normally 56% | — |
| NEAR | setups 5,771, target reached normally 57% | setups 11,757, target reached normally 55% | — |
| HYPE | setups 5,857, target reached normally 57% | setups 11,613, target reached normally 56% | — |
| BNB | setups 5,692, target reached normally 57% | setups 11,655, target reached normally 55% | — |
| ZEC | setups 5,927, target reached normally 56% | setups 10,006, target reached normally 56% | — |
