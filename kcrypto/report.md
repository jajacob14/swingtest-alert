# Kalshi crypto 15-min model report
Trained 2026-11-21 15:35 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 295231

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5119 vs 0.5115 · edge bets 5: won 40%, ROI -30% | 3289 windows · right 75% vs Kalshi 75% · logloss 0.5011 vs 0.5011 · edge bets 4: won 25%, ROI -56% | — |
| ETH | 597 windows · right 73% vs Kalshi 74% · logloss 0.5236 vs 0.5211 · edge bets 10: won 60%, ROI +10% | 3135 windows · right 77% vs Kalshi 77% · logloss 0.4786 vs 0.4778 | — |
| SOL | 598 windows · right 74% vs Kalshi 74% · logloss 0.5191 vs 0.5186 · edge bets 8: won 38%, ROI -30% | 3135 windows · right 76% vs Kalshi 76% · logloss 0.4879 vs 0.4878 | — |
| XRP | 597 windows · right 74% vs Kalshi 74% · logloss 0.5194 vs 0.5179 · edge bets 43: won 51%, ROI -6% | 3132 windows · right 76% vs Kalshi 76% · logloss 0.4824 vs 0.4826 · edge bets 21: won 57%, ROI +6% | — |
| DOGE | 598 windows · right 75% vs Kalshi 75% · logloss 0.5109 vs 0.5104 · edge bets 20: won 60%, ROI +13% | 3133 windows · right 76% vs Kalshi 76% · logloss 0.4782 vs 0.4793 · edge bets 4: won 100%, ROI +87% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5169 vs 0.5159 · edge bets 86: won 52%, ROI -4%

**All months:** 15824 windows · right 76% vs Kalshi 76% · logloss 0.4859 vs 0.4859 · edge bets 29: won 59%, ROI +8%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4631 vs 0.4642 · edge bets 5: won 60%, ROI +8% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4718 vs 0.4719 · edge bets 10: won 50%, ROI -6% |
| 2026-10 | 9465 windows · right 75% vs Kalshi 75% · logloss 0.497 vs 0.4969 · edge bets 14: won 64%, ROI +17% |

Strongest signals: `sgap` +0.052, `s_EU` +0.032, `dmid5` +0.025, `m_XRP` +0.020, `s_US` -0.019

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,495, target reached normally 24% | setups 13,226, target reached normally 19% | — |
| ETH | setups 2,435, target reached normally 26% | setups 13,190, target reached normally 20% | — |
| SOL | setups 2,483, target reached normally 23% | setups 13,374, target reached normally 21% | — |
| XRP | setups 2,540, target reached normally 26% | setups 13,709, target reached normally 20% | — |
| DOGE | setups 2,504, target reached normally 23% | setups 13,446, target reached normally 20% | — |

**All weeks:** setups 12,457, target reached normally 24%

**All months:** setups 66,945, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,840, target reached normally 58% | setups 33,822, target reached normally 56% | — |
| ETH | setups 5,714, target reached normally 58% | setups 30,393, target reached normally 55% | — |
| SOL | setups 5,715, target reached normally 57% | setups 30,080, target reached normally 56% | — |
| XRP | setups 5,416, target reached normally 57% | setups 30,187, target reached normally 56% | — |
| DOGE | setups 5,615, target reached normally 57% | setups 29,998, target reached normally 56% | — |
