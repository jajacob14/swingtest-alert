# Kalshi crypto 15-min model report
Trained 2026-11-27 03:49 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 67461

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 598 windows · right 73% vs Kalshi 74% · logloss 0.523 vs 0.5236 · edge bets 23: won 48%, ROI -11% | 1433 windows · right 76% vs Kalshi 76% · logloss 0.4813 vs 0.4837 · edge bets 18: won 72%, ROI +38% | — |
| XRP | 597 windows · right 74% vs Kalshi 74% · logloss 0.5156 vs 0.5156 · edge bets 11: won 46%, ROI -12% | 1434 windows · right 76% vs Kalshi 76% · logloss 0.4848 vs 0.4849 | — |
| ETH | 597 windows · right 74% vs Kalshi 74% · logloss 0.5208 vs 0.5195 · edge bets 12: won 58%, ROI +11% | 1438 windows · right 76% vs Kalshi 76% · logloss 0.4958 vs 0.4946 · edge bets 2: won 100%, ROI +106% | — |
| BTC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5197 vs 0.5192 · edge bets 21: won 52%, ROI -6% | 1437 windows · right 74% vs Kalshi 74% · logloss 0.5194 vs 0.521 · edge bets 23: won 61%, ROI +6% | — |
| SOL | 597 windows · right 76% vs Kalshi 76% · logloss 0.498 vs 0.4979 · edge bets 10: won 50%, ROI -9% | 1438 windows · right 76% vs Kalshi 76% · logloss 0.4918 vs 0.4916 · edge bets 2: won 50%, ROI -4% | — |
| NEAR | 597 windows · right 75% vs Kalshi 76% · logloss 0.4944 vs 0.4953 · edge bets 6: won 50%, ROI +3% | 1435 windows · right 74% vs Kalshi 74% · logloss 0.5062 vs 0.5076 · edge bets 5: won 80%, ROI +43% | — |
| HYPE | 598 windows · right 73% vs Kalshi 73% · logloss 0.5206 vs 0.5225 · edge bets 14: won 43%, ROI -23% | 1435 windows · right 75% vs Kalshi 75% · logloss 0.5044 vs 0.5063 · edge bets 4: won 100%, ROI +74% | — |
| BNB | 598 windows · right 75% vs Kalshi 74% · logloss 0.5092 vs 0.5112 · edge bets 27: won 74%, ROI +36% | 1432 windows · right 76% vs Kalshi 76% · logloss 0.4871 vs 0.4901 · edge bets 39: won 67%, ROI +20% | ✅ |
| ZEC | 598 windows · right 75% vs Kalshi 75% · logloss 0.4948 vs 0.4948 · edge bets 12: won 67%, ROI +18% | 1281 windows · right 75% vs Kalshi 75% · logloss 0.5017 vs 0.5025 · edge bets 2: won 50%, ROI -4% | — |

**All weeks:** 5378 windows · right 74% vs Kalshi 74% · logloss 0.5107 vs 0.5111 · edge bets 136: won 56%, ROI +3%

**All months:** 12763 windows · right 75% vs Kalshi 75% · logloss 0.497 vs 0.4981 · edge bets 95: won 68%, ROI +24%

| Month | Result |
|---|---|
| 2026-09 | 822 windows · right 76% vs Kalshi 76% · logloss 0.4797 vs 0.4813 · edge bets 7: won 57%, ROI +15% |
| 2026-10 | 8744 windows · right 76% vs Kalshi 75% · logloss 0.4947 vs 0.4954 · edge bets 68: won 69%, ROI +25% |
| 2026-11 | 3197 windows · right 75% vs Kalshi 75% · logloss 0.5077 vs 0.5097 · edge bets 20: won 70%, ROI +25% |

Strongest signals: `sgap` +0.076, `sr1` +0.039, `dmid5` +0.035, `tleft` -0.034, `s_US` -0.032

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,314, target reached normally 23% | setups 6,464, target reached normally 22% | — |
| XRP | setups 2,534, target reached normally 26% | setups 6,432, target reached normally 21% | — |
| ETH | setups 2,340, target reached normally 23% | setups 5,955, target reached normally 23% | — |
| BTC | setups 2,271, target reached normally 21% | setups 5,812, target reached normally 21% | — |
| SOL | setups 2,441, target reached normally 22% | setups 6,215, target reached normally 22% | — |
| NEAR | setups 2,491, target reached normally 24% | setups 6,154, target reached normally 22% | — |
| HYPE | setups 2,314, target reached normally 21% | setups 6,116, target reached normally 24% | — |
| BNB | setups 2,364, target reached normally 22% | setups 6,015, target reached normally 22% | — |
| ZEC | setups 2,416, target reached normally 18% | setups 5,704, target reached normally 22% | — |

**All weeks:** setups 21,485, target reached normally 22%

**All months:** setups 54,867, target reached normally 22%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,197, target reached normally 59% | setups 13,399, target reached normally 56% | — |
| XRP | setups 5,813, target reached normally 57% | setups 13,528, target reached normally 55% | — |
| ETH | setups 6,097, target reached normally 57% | setups 13,932, target reached normally 57% | — |
| BTC | setups 6,149, target reached normally 58% | setups 14,426, target reached normally 57% | — |
| SOL | setups 5,981, target reached normally 55% | setups 13,625, target reached normally 56% | — |
| NEAR | setups 5,892, target reached normally 57% | setups 13,617, target reached normally 56% | — |
| HYPE | setups 6,058, target reached normally 58% | setups 13,483, target reached normally 56% | — |
| BNB | setups 5,848, target reached normally 56% | setups 13,515, target reached normally 55% | — |
| ZEC | setups 5,851, target reached normally 56% | setups 11,897, target reached normally 56% | — |
