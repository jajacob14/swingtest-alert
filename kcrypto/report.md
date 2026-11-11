# Kalshi crypto 15-min model report
Trained 2026-11-11 05:09 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 70192

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 75% vs Kalshi 75% · logloss 0.5015 vs 0.5015 · edge bets 33: won 76%, ROI +31% | 2303 windows · right 75% vs Kalshi 75% · logloss 0.4963 vs 0.4964 · edge bets 14: won 64%, ROI +5% | — |
| ETH | 597 windows · right 75% vs Kalshi 76% · logloss 0.5015 vs 0.5005 · edge bets 14: won 50%, ROI -7% | 2149 windows · right 78% vs Kalshi 78% · logloss 0.4649 vs 0.4646 · edge bets 2: won 0%, ROI -100% | — |
| SOL | 598 windows · right 74% vs Kalshi 74% · logloss 0.5136 vs 0.5134 · edge bets 30: won 53%, ROI +2% | 2149 windows · right 77% vs Kalshi 77% · logloss 0.4799 vs 0.4798 · edge bets 2: won 0%, ROI -100% | — |
| XRP | 598 windows · right 74% vs Kalshi 75% · logloss 0.5229 vs 0.5209 · edge bets 16: won 62%, ROI +19% | 2146 windows · right 77% vs Kalshi 77% · logloss 0.4695 vs 0.4704 · edge bets 18: won 50%, ROI -7% | — |
| DOGE | 598 windows · right 77% vs Kalshi 77% · logloss 0.4759 vs 0.4757 · edge bets 35: won 69%, ROI +32% | 2147 windows · right 77% vs Kalshi 77% · logloss 0.4658 vs 0.4669 · edge bets 5: won 80%, ROI +58% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.503 vs 0.5023 · edge bets 128: won 64%, ROI +19%

**All months:** 10894 windows · right 77% vs Kalshi 77% · logloss 0.4757 vs 0.476 · edge bets 41: won 54%, ROI -4%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4634 vs 0.4642 · edge bets 5: won 60%, ROI +11% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4713 vs 0.4719 · edge bets 22: won 55%, ROI -3% |
| 2026-10 | 4535 windows · right 76% vs Kalshi 76% · logloss 0.4849 vs 0.4847 · edge bets 14: won 50%, ROI -13% |

Strongest signals: `sgap` +0.056, `s_EU` +0.032, `dmid5` +0.027, `dmid1` -0.025, `sr1` +0.024

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,425, target reached normally 23% | setups 9,365, target reached normally 19% | — |
| ETH | setups 2,539, target reached normally 23% | setups 9,269, target reached normally 19% | — |
| SOL | setups 2,525, target reached normally 22% | setups 9,400, target reached normally 21% | — |
| XRP | setups 2,516, target reached normally 23% | setups 9,543, target reached normally 20% | — |
| DOGE | setups 2,664, target reached normally 21% | setups 9,384, target reached normally 20% | — |

**All weeks:** setups 12,669, target reached normally 22%

**All months:** setups 46,961, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,937, target reached normally 56% | setups 23,779, target reached normally 55% | — |
| ETH | setups 5,789, target reached normally 55% | setups 20,641, target reached normally 53% | — |
| SOL | setups 5,701, target reached normally 57% | setups 20,552, target reached normally 55% | — |
| XRP | setups 5,561, target reached normally 55% | setups 20,685, target reached normally 55% | — |
| DOGE | setups 5,648, target reached normally 54% | setups 20,324, target reached normally 55% | — |
