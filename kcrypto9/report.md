# Kalshi crypto 15-min model report
Trained 2026-11-25 08:51 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 24603

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 597 windows · right 74% vs Kalshi 74% · logloss 0.5164 vs 0.5166 · edge bets 16: won 44%, ROI -21% | 1269 windows · right 76% vs Kalshi 76% · logloss 0.4775 vs 0.4801 · edge bets 27: won 67%, ROI +24% | — |
| XRP | 598 windows · right 74% vs Kalshi 74% · logloss 0.518 vs 0.5174 · edge bets 6: won 33%, ROI -38% | 1270 windows · right 77% vs Kalshi 77% · logloss 0.4792 vs 0.4797 · edge bets 1: won 100%, ROI +56% | — |
| ETH | 597 windows · right 73% vs Kalshi 73% · logloss 0.5313 vs 0.5304 · edge bets 7: won 71%, ROI +32% | 1274 windows · right 76% vs Kalshi 76% · logloss 0.492 vs 0.4907 · edge bets 3: won 100%, ROI +90% | — |
| BTC | 598 windows · right 73% vs Kalshi 74% · logloss 0.5175 vs 0.5176 · edge bets 10: won 60%, ROI +9% | 1273 windows · right 74% vs Kalshi 74% · logloss 0.5221 vs 0.5229 · edge bets 31: won 58%, ROI -1% | — |
| SOL | 597 windows · right 76% vs Kalshi 75% · logloss 0.4947 vs 0.4953 · edge bets 5: won 80%, ROI +42% | 1274 windows · right 76% vs Kalshi 76% · logloss 0.4874 vs 0.4869 · edge bets 3: won 33%, ROI -38% | — |
| NEAR | 598 windows · right 76% vs Kalshi 76% · logloss 0.491 vs 0.4935 · edge bets 6: won 83%, ROI +51% | 1271 windows · right 75% vs Kalshi 75% · logloss 0.5037 vs 0.5056 · edge bets 10: won 80%, ROI +38% | — |
| HYPE | 597 windows · right 73% vs Kalshi 73% · logloss 0.5257 vs 0.5281 · edge bets 14: won 57%, ROI -1% | 1271 windows · right 75% vs Kalshi 75% · logloss 0.5079 vs 0.5105 · edge bets 14: won 79%, ROI +42% | — |
| BNB | 598 windows · right 75% vs Kalshi 74% · logloss 0.504 vs 0.5071 · edge bets 21: won 71%, ROI +29% | 1268 windows · right 76% vs Kalshi 76% · logloss 0.4896 vs 0.4925 · edge bets 68: won 69%, ROI +28% | ✅ |
| ZEC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5035 vs 0.5028 · edge bets 12: won 50%, ROI -8% | 1117 windows · right 75% vs Kalshi 75% · logloss 0.5027 vs 0.5033 · edge bets 4: won 50%, ROI -6% | — |

**All weeks:** 5378 windows · right 74% vs Kalshi 74% · logloss 0.5113 vs 0.5121 · edge bets 97: won 60%, ROI +8%

**All months:** 11287 windows · right 76% vs Kalshi 75% · logloss 0.4958 vs 0.4969 · edge bets 161: won 68%, ROI +22%

| Month | Result |
|---|---|
| 2026-09 | 822 windows · right 76% vs Kalshi 76% · logloss 0.4799 vs 0.4813 · edge bets 10: won 60%, ROI +18% |
| 2026-10 | 8744 windows · right 76% vs Kalshi 75% · logloss 0.4947 vs 0.4954 · edge bets 125: won 68%, ROI +24% |
| 2026-11 | 1721 windows · right 75% vs Kalshi 75% · logloss 0.5087 vs 0.512 · edge bets 26: won 69%, ROI +19% |

Strongest signals: `sgap` +0.095, `sr1` +0.042, `s_EU` +0.037, `tleft` -0.032, `dmid5` +0.032

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,379, target reached normally 22% | setups 5,740, target reached normally 22% | — |
| XRP | setups 2,521, target reached normally 26% | setups 5,749, target reached normally 21% | — |
| ETH | setups 2,397, target reached normally 25% | setups 5,255, target reached normally 22% | — |
| BTC | setups 2,396, target reached normally 22% | setups 5,121, target reached normally 20% | — |
| SOL | setups 2,430, target reached normally 21% | setups 5,489, target reached normally 22% | — |
| NEAR | setups 2,509, target reached normally 24% | setups 5,385, target reached normally 22% | — |
| HYPE | setups 2,400, target reached normally 23% | setups 5,402, target reached normally 24% | — |
| BNB | setups 2,444, target reached normally 23% | setups 5,307, target reached normally 22% | — |
| ZEC | setups 2,322, target reached normally 20% | setups 4,967, target reached normally 21% | — |

**All weeks:** setups 21,798, target reached normally 23%

**All months:** setups 48,415, target reached normally 22%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,017, target reached normally 58% | setups 11,805, target reached normally 55% | — |
| XRP | setups 5,751, target reached normally 57% | setups 11,964, target reached normally 55% | — |
| ETH | setups 6,030, target reached normally 58% | setups 12,369, target reached normally 56% | — |
| BTC | setups 5,966, target reached normally 58% | setups 12,801, target reached normally 56% | — |
| SOL | setups 5,941, target reached normally 56% | setups 12,015, target reached normally 56% | — |
| NEAR | setups 5,829, target reached normally 57% | setups 12,062, target reached normally 55% | — |
| HYPE | setups 5,925, target reached normally 58% | setups 11,923, target reached normally 56% | — |
| BNB | setups 5,746, target reached normally 57% | setups 11,981, target reached normally 55% | — |
| ZEC | setups 5,955, target reached normally 56% | setups 10,351, target reached normally 56% | — |
