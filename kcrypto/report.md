# Kalshi crypto 15-min model report
Trained 2026-11-20 19:33 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 277276

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 75% vs Kalshi 75% · logloss 0.4973 vs 0.4961 · edge bets 6: won 50%, ROI -12% | 3209 windows · right 75% vs Kalshi 75% · logloss 0.5012 vs 0.5011 · edge bets 3: won 33%, ROI -39% | — |
| ETH | 598 windows · right 73% vs Kalshi 74% · logloss 0.5263 vs 0.5222 · edge bets 6: won 50%, ROI -8% | 3055 windows · right 76% vs Kalshi 77% · logloss 0.4806 vs 0.4799 | — |
| SOL | 598 windows · right 74% vs Kalshi 74% · logloss 0.5202 vs 0.5185 · edge bets 12: won 50%, ROI -5% | 3055 windows · right 76% vs Kalshi 76% · logloss 0.4869 vs 0.4867 | — |
| XRP | 598 windows · right 74% vs Kalshi 75% · logloss 0.5126 vs 0.51 · edge bets 32: won 47%, ROI -13% | 3052 windows · right 76% vs Kalshi 76% · logloss 0.4821 vs 0.4824 · edge bets 11: won 55%, ROI +1% | — |
| DOGE | 597 windows · right 75% vs Kalshi 75% · logloss 0.5094 vs 0.509 · edge bets 13: won 54%, ROI -2% | 3053 windows · right 76% vs Kalshi 76% · logloss 0.4777 vs 0.4787 · edge bets 3: won 100%, ROI +86% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5131 vs 0.5111 · edge bets 69: won 49%, ROI -9%

**All months:** 15424 windows · right 76% vs Kalshi 76% · logloss 0.4859 vs 0.486 · edge bets 17: won 59%, ROI +9%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4637 vs 0.4642 · edge bets 4: won 50%, ROI -2% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4717 vs 0.4719 · edge bets 6: won 50%, ROI -6% |
| 2026-10 | 9065 windows · right 75% vs Kalshi 75% · logloss 0.4976 vs 0.4975 · edge bets 7: won 71%, ROI +26% |

Strongest signals: `sgap` +0.055, `dmid5` +0.026, `tleft` -0.023, `kvol` -0.019, `s_EU` +0.017

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,526, target reached normally 23% | setups 12,937, target reached normally 20% | — |
| ETH | setups 2,470, target reached normally 27% | setups 12,868, target reached normally 20% | — |
| SOL | setups 2,467, target reached normally 23% | setups 13,061, target reached normally 21% | — |
| XRP | setups 2,512, target reached normally 25% | setups 13,400, target reached normally 20% | — |
| DOGE | setups 2,515, target reached normally 23% | setups 13,106, target reached normally 20% | — |

**All weeks:** setups 12,490, target reached normally 24%

**All months:** setups 65,372, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,777, target reached normally 57% | setups 32,955, target reached normally 56% | — |
| ETH | setups 5,629, target reached normally 58% | setups 29,606, target reached normally 55% | — |
| SOL | setups 5,726, target reached normally 57% | setups 29,289, target reached normally 56% | — |
| XRP | setups 5,477, target reached normally 56% | setups 29,381, target reached normally 56% | — |
| DOGE | setups 5,615, target reached normally 56% | setups 29,176, target reached normally 56% | — |
