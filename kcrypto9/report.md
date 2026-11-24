# Kalshi crypto 15-min model report
Trained 2026-11-24 16:23 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 9460

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| ETH | 598 windows · right 74% vs Kalshi 74% · logloss 0.5203 vs 0.5187 · edge bets 2: won 50%, ROI -14% | 1208 windows · right 76% vs Kalshi 76% · logloss 0.494 vs 0.4926 · edge bets 3: won 100%, ROI +90% | — |
| BTC | 597 windows · right 73% vs Kalshi 73% · logloss 0.52 vs 0.5215 · edge bets 5: won 40%, ROI -33% | 1207 windows · right 74% vs Kalshi 74% · logloss 0.521 vs 0.5218 · edge bets 33: won 58%, ROI -2% | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.5032 vs 0.504 | 1208 windows · right 77% vs Kalshi 76% · logloss 0.485 vs 0.4844 · edge bets 2: won 50%, ROI -21% | — |
| XRP | 597 windows · right 74% vs Kalshi 74% · logloss 0.5259 vs 0.5248 · edge bets 5: won 60%, ROI +18% | 1204 windows · right 77% vs Kalshi 77% · logloss 0.4758 vs 0.4764 · edge bets 2: won 50%, ROI -11% | — |
| NEAR | 598 windows · right 76% vs Kalshi 76% · logloss 0.4894 vs 0.4912 · edge bets 11: won 73%, ROI +27% | 1205 windows · right 75% vs Kalshi 74% · logloss 0.5034 vs 0.5056 · edge bets 10: won 80%, ROI +38% | — |
| HYPE | 598 windows · right 74% vs Kalshi 73% · logloss 0.5226 vs 0.5246 · edge bets 6: won 83%, ROI +38% | 1205 windows · right 75% vs Kalshi 75% · logloss 0.5048 vs 0.5073 · edge bets 13: won 77%, ROI +41% | — |
| DOGE | 598 windows · right 75% vs Kalshi 75% · logloss 0.5023 vs 0.5019 · edge bets 15: won 60%, ROI +5% | 1203 windows · right 77% vs Kalshi 76% · logloss 0.4756 vs 0.478 · edge bets 32: won 66%, ROI +22% | — |
| BNB | 598 windows · right 76% vs Kalshi 76% · logloss 0.4884 vs 0.4887 · edge bets 21: won 67%, ROI +22% | 1202 windows · right 76% vs Kalshi 76% · logloss 0.4892 vs 0.4921 · edge bets 68: won 69%, ROI +26% | ✅ |
| ZEC | 596 windows · right 74% vs Kalshi 74% · logloss 0.5063 vs 0.5059 · edge bets 2: won 0%, ROI -100% | 1051 windows · right 75% vs Kalshi 75% · logloss 0.5057 vs 0.5056 · edge bets 5: won 60%, ROI +6% | — |

**All weeks:** 5377 windows · right 74% vs Kalshi 74% · logloss 0.5087 vs 0.5091 · edge bets 67: won 63%, ROI +12%

**All months:** 10693 windows · right 76% vs Kalshi 76% · logloss 0.4948 vs 0.4959 · edge bets 168: won 67%, ROI +21%

| Month | Result |
|---|---|
| 2026-09 | 822 windows · right 76% vs Kalshi 76% · logloss 0.4799 vs 0.4813 · edge bets 11: won 55%, ROI +5% |
| 2026-10 | 8744 windows · right 76% vs Kalshi 75% · logloss 0.4948 vs 0.4954 · edge bets 139: won 68%, ROI +23% |
| 2026-11 | 1127 windows · right 75% vs Kalshi 75% · logloss 0.5059 vs 0.5102 · edge bets 18: won 67%, ROI +12% |

Strongest signals: `sgap` +0.092, `sr1` +0.047, `s_EU` +0.036, `tleft` -0.032, `dmid5` +0.030

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| ETH | setups 2,418, target reached normally 24% | setups 4,963, target reached normally 23% | — |
| BTC | setups 2,404, target reached normally 23% | setups 4,832, target reached normally 20% | — |
| SOL | setups 2,439, target reached normally 20% | setups 5,196, target reached normally 22% | — |
| XRP | setups 2,509, target reached normally 26% | setups 5,480, target reached normally 20% | — |
| NEAR | setups 2,522, target reached normally 24% | setups 5,067, target reached normally 21% | — |
| HYPE | setups 2,405, target reached normally 23% | setups 5,115, target reached normally 24% | — |
| DOGE | setups 2,408, target reached normally 22% | setups 5,431, target reached normally 21% | — |
| BNB | setups 2,488, target reached normally 22% | setups 5,001, target reached normally 22% | — |
| ZEC | setups 2,353, target reached normally 22% | setups 4,677, target reached normally 22% | — |

**All weeks:** setups 21,946, target reached normally 23%

**All months:** setups 45,762, target reached normally 22%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| ETH | setups 5,985, target reached normally 57% | setups 11,754, target reached normally 56% | — |
| BTC | setups 5,970, target reached normally 58% | setups 12,149, target reached normally 56% | — |
| SOL | setups 5,911, target reached normally 56% | setups 11,426, target reached normally 56% | — |
| XRP | setups 5,696, target reached normally 57% | setups 11,354, target reached normally 55% | — |
| NEAR | setups 5,740, target reached normally 57% | setups 11,473, target reached normally 56% | — |
| HYPE | setups 5,877, target reached normally 57% | setups 11,327, target reached normally 56% | — |
| DOGE | setups 5,909, target reached normally 57% | setups 11,229, target reached normally 55% | — |
| BNB | setups 5,703, target reached normally 55% | setups 11,385, target reached normally 55% | — |
| ZEC | setups 5,942, target reached normally 56% | setups 9,761, target reached normally 56% | — |
