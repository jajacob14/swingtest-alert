# Kalshi crypto 15-min model report
Trained 2026-11-21 04:03 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 285655

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5107 vs 0.5106 · edge bets 5: won 40%, ROI -30% | 3243 windows · right 75% vs Kalshi 75% · logloss 0.5005 vs 0.5006 · edge bets 2: won 0%, ROI -100% | — |
| ETH | 598 windows · right 73% vs Kalshi 74% · logloss 0.5238 vs 0.5205 · edge bets 9: won 56%, ROI +2% | 3089 windows · right 77% vs Kalshi 77% · logloss 0.4801 vs 0.4794 | — |
| SOL | 598 windows · right 73% vs Kalshi 73% · logloss 0.5255 vs 0.5242 · edge bets 9: won 44%, ROI -16% | 3089 windows · right 76% vs Kalshi 76% · logloss 0.4867 vs 0.4865 | — |
| XRP | 597 windows · right 74% vs Kalshi 74% · logloss 0.5226 vs 0.5203 · edge bets 37: won 49%, ROI -10% | 3086 windows · right 76% vs Kalshi 76% · logloss 0.4825 vs 0.4828 · edge bets 10: won 40%, ROI -24% | — |
| DOGE | 597 windows · right 75% vs Kalshi 75% · logloss 0.5116 vs 0.5105 · edge bets 14: won 64%, ROI +16% | 3087 windows · right 76% vs Kalshi 76% · logloss 0.4781 vs 0.479 · edge bets 3: won 100%, ROI +86% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5188 vs 0.5172 · edge bets 74: won 51%, ROI -6%

**All months:** 15594 windows · right 76% vs Kalshi 76% · logloss 0.4858 vs 0.4859 · edge bets 15: won 47%, ROI -13%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4633 vs 0.4642 · edge bets 2: won 0%, ROI -100% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4717 vs 0.4719 · edge bets 6: won 50%, ROI -6% |
| 2026-10 | 9235 windows · right 75% vs Kalshi 75% · logloss 0.4972 vs 0.4971 · edge bets 7: won 57%, ROI +4% |

Strongest signals: `sgap` +0.052, `dmid5` +0.024, `tleft` -0.021, `m_XRP` +0.020, `s_EU` +0.020

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,505, target reached normally 23% | setups 13,071, target reached normally 20% | — |
| ETH | setups 2,469, target reached normally 27% | setups 13,002, target reached normally 20% | — |
| SOL | setups 2,470, target reached normally 23% | setups 13,219, target reached normally 21% | — |
| XRP | setups 2,528, target reached normally 26% | setups 13,539, target reached normally 20% | — |
| DOGE | setups 2,510, target reached normally 23% | setups 13,237, target reached normally 20% | — |

**All weeks:** setups 12,482, target reached normally 24%

**All months:** setups 66,068, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,802, target reached normally 58% | setups 33,324, target reached normally 56% | — |
| ETH | setups 5,672, target reached normally 58% | setups 29,948, target reached normally 55% | — |
| SOL | setups 5,696, target reached normally 58% | setups 29,595, target reached normally 56% | — |
| XRP | setups 5,455, target reached normally 57% | setups 29,726, target reached normally 56% | — |
| DOGE | setups 5,598, target reached normally 57% | setups 29,532, target reached normally 56% | — |
