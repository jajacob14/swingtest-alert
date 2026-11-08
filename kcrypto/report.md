# Kalshi crypto 15-min model report
Trained 2026-11-08 01:52 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 13691

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 73% vs Kalshi 73% · logloss 0.5248 vs 0.5265 · edge bets 29: won 69%, ROI +18% | 2002 windows · right 76% vs Kalshi 76% · logloss 0.4947 vs 0.4942 · edge bets 67: won 51%, ROI -13% | — |
| ETH | 597 windows · right 75% vs Kalshi 75% · logloss 0.5034 vs 0.5042 · edge bets 24: won 58%, ROI -0% | 1848 windows · right 78% vs Kalshi 78% · logloss 0.4628 vs 0.4616 · edge bets 39: won 31%, ROI -45% | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.4995 vs 0.4991 · edge bets 29: won 45%, ROI -17% | 1848 windows · right 77% vs Kalshi 76% · logloss 0.4802 vs 0.48 · edge bets 21: won 43%, ROI -24% | — |
| XRP | 598 windows · right 74% vs Kalshi 75% · logloss 0.5178 vs 0.5167 · edge bets 7: won 57%, ROI +3% | 1845 windows · right 77% vs Kalshi 77% · logloss 0.4685 vs 0.4688 · edge bets 54: won 52%, ROI -5% | — |
| DOGE | 598 windows · right 76% vs Kalshi 76% · logloss 0.4951 vs 0.4957 · edge bets 66: won 56%, ROI +4% | 1846 windows · right 78% vs Kalshi 78% · logloss 0.461 vs 0.4617 · edge bets 35: won 60%, ROI +12% | ✅ |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.5083 vs 0.5086 · edge bets 155: won 57%, ROI +2%

**All months:** 9389 windows · right 77% vs Kalshi 77% · logloss 0.4739 vs 0.4737 · edge bets 216: won 48%, ROI -14%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4634 vs 0.4642 · edge bets 35: won 49%, ROI -13% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4717 vs 0.4719 · edge bets 94: won 44%, ROI -24% |
| 2026-10 | 3030 windows · right 76% vs Kalshi 76% · logloss 0.4831 vs 0.4817 · edge bets 87: won 53%, ROI -3% |

Strongest signals: `sgap` +0.067, `dmid5` +0.036, `s_EU` +0.030, `m_XRP` +0.030, `dmid1` -0.030

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,346, target reached normally 22% | setups 8,094, target reached normally 18% | — |
| ETH | setups 2,531, target reached normally 23% | setups 7,967, target reached normally 18% | — |
| SOL | setups 2,552, target reached normally 22% | setups 8,161, target reached normally 20% | — |
| XRP | setups 2,456, target reached normally 23% | setups 8,215, target reached normally 19% | — |
| DOGE | setups 2,648, target reached normally 22% | setups 8,106, target reached normally 18% | — |

**All weeks:** setups 12,533, target reached normally 22%

**All months:** setups 40,543, target reached normally 19%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 6,270, target reached normally 58% | setups 20,877, target reached normally 55% | — |
| ETH | setups 5,803, target reached normally 56% | setups 17,894, target reached normally 53% | — |
| SOL | setups 5,720, target reached normally 56% | setups 17,684, target reached normally 55% | — |
| XRP | setups 5,750, target reached normally 56% | setups 17,923, target reached normally 54% | — |
| DOGE | setups 5,633, target reached normally 56% | setups 17,554, target reached normally 54% | — |
