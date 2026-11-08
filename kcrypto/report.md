# Kalshi crypto 15-min model report
Trained 2026-11-08 13:24 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 20999

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 73% vs Kalshi 73% · logloss 0.5218 vs 0.5228 · edge bets 38: won 71%, ROI +23% | 2048 windows · right 76% vs Kalshi 76% · logloss 0.494 vs 0.4938 · edge bets 42: won 62%, ROI +3% | — |
| ETH | 597 windows · right 75% vs Kalshi 76% · logloss 0.5079 vs 0.5064 · edge bets 18: won 44%, ROI -22% | 1894 windows · right 78% vs Kalshi 78% · logloss 0.4617 vs 0.4608 · edge bets 11: won 55%, ROI +0% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.5022 vs 0.5013 · edge bets 32: won 50%, ROI -9% | 1894 windows · right 76% vs Kalshi 76% · logloss 0.4806 vs 0.4805 · edge bets 12: won 42%, ROI -26% | — |
| XRP | 598 windows · right 74% vs Kalshi 74% · logloss 0.5244 vs 0.5232 · edge bets 11: won 36%, ROI -35% | 1891 windows · right 77% vs Kalshi 77% · logloss 0.469 vs 0.4696 · edge bets 36: won 53%, ROI -3% | — |
| DOGE | 597 windows · right 75% vs Kalshi 76% · logloss 0.5015 vs 0.5011 · edge bets 63: won 54%, ROI +0% | 1892 windows · right 78% vs Kalshi 78% · logloss 0.4601 vs 0.461 · edge bets 22: won 68%, ROI +25% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 75% · logloss 0.5116 vs 0.511 · edge bets 162: won 55%, ROI -1%

**All months:** 9619 windows · right 77% vs Kalshi 77% · logloss 0.4735 vs 0.4736 · edge bets 123: won 58%, ROI +2%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4633 vs 0.4642 · edge bets 20: won 50%, ROI -8% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4715 vs 0.4719 · edge bets 54: won 59%, ROI +2% |
| 2026-10 | 3260 windows · right 76% vs Kalshi 76% · logloss 0.4816 vs 0.4808 · edge bets 49: won 59%, ROI +5% |

Strongest signals: `sgap` +0.069, `dmid5` +0.039, `dmid1` -0.029, `s_EU` +0.029, `s_US` -0.028

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,336, target reached normally 22% | setups 8,299, target reached normally 18% | — |
| ETH | setups 2,518, target reached normally 23% | setups 8,187, target reached normally 18% | — |
| SOL | setups 2,513, target reached normally 23% | setups 8,363, target reached normally 20% | — |
| XRP | setups 2,426, target reached normally 23% | setups 8,431, target reached normally 19% | — |
| DOGE | setups 2,602, target reached normally 21% | setups 8,324, target reached normally 18% | — |

**All weeks:** setups 12,395, target reached normally 22%

**All months:** setups 41,604, target reached normally 19%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 6,227, target reached normally 57% | setups 21,319, target reached normally 55% | — |
| ETH | setups 5,801, target reached normally 56% | setups 18,304, target reached normally 53% | — |
| SOL | setups 5,773, target reached normally 56% | setups 18,125, target reached normally 55% | — |
| XRP | setups 5,778, target reached normally 57% | setups 18,345, target reached normally 54% | — |
| DOGE | setups 5,684, target reached normally 55% | setups 17,962, target reached normally 54% | — |
