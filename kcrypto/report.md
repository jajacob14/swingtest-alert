# Kalshi crypto 15-min model report
Trained 2026-11-10 17:38 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 59407

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 75% vs Kalshi 75% · logloss 0.4967 vs 0.4975 · edge bets 33: won 76%, ROI +31% | 2257 windows · right 76% vs Kalshi 76% · logloss 0.4938 vs 0.4935 · edge bets 23: won 65%, ROI +4% | — |
| ETH | 597 windows · right 75% vs Kalshi 76% · logloss 0.4982 vs 0.4976 · edge bets 14: won 43%, ROI -25% | 2103 windows · right 78% vs Kalshi 78% · logloss 0.4623 vs 0.4617 · edge bets 3: won 33%, ROI -43% | — |
| SOL | 597 windows · right 74% vs Kalshi 74% · logloss 0.5203 vs 0.5195 · edge bets 37: won 51%, ROI -3% | 2103 windows · right 77% vs Kalshi 77% · logloss 0.4782 vs 0.4777 · edge bets 6: won 50%, ROI -15% | — |
| XRP | 598 windows · right 74% vs Kalshi 74% · logloss 0.5284 vs 0.5261 · edge bets 21: won 71%, ROI +29% | 2100 windows · right 77% vs Kalshi 77% · logloss 0.4677 vs 0.4687 · edge bets 29: won 59%, ROI +9% | — |
| DOGE | 598 windows · right 76% vs Kalshi 77% · logloss 0.4811 vs 0.4806 · edge bets 53: won 60%, ROI +14% | 2101 windows · right 78% vs Kalshi 78% · logloss 0.4632 vs 0.4642 · edge bets 16: won 62%, ROI +16% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.5048 vs 0.5042 · edge bets 158: won 61%, ROI +12%

**All months:** 10664 windows · right 77% vs Kalshi 77% · logloss 0.4735 vs 0.4736 · edge bets 77: won 60%, ROI +5%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4636 vs 0.4642 · edge bets 12: won 58%, ROI +5% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4714 vs 0.4719 · edge bets 35: won 69%, ROI +20% |
| 2026-10 | 4305 windows · right 76% vs Kalshi 76% · logloss 0.4796 vs 0.479 · edge bets 30: won 50%, ROI -13% |

Strongest signals: `sgap` +0.064, `dmid5` +0.030, `s_EU` +0.027, `dmid1` -0.024, `m_XRP` +0.023

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,429, target reached normally 23% | setups 9,185, target reached normally 19% | — |
| ETH | setups 2,521, target reached normally 23% | setups 9,083, target reached normally 19% | — |
| SOL | setups 2,545, target reached normally 23% | setups 9,241, target reached normally 20% | — |
| XRP | setups 2,517, target reached normally 24% | setups 9,336, target reached normally 20% | — |
| DOGE | setups 2,660, target reached normally 20% | setups 9,198, target reached normally 20% | — |

**All weeks:** setups 12,672, target reached normally 22%

**All months:** setups 46,043, target reached normally 19%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,954, target reached normally 56% | setups 23,272, target reached normally 55% | — |
| ETH | setups 5,796, target reached normally 56% | setups 20,163, target reached normally 53% | — |
| SOL | setups 5,736, target reached normally 58% | setups 20,050, target reached normally 55% | — |
| XRP | setups 5,602, target reached normally 56% | setups 20,234, target reached normally 54% | — |
| DOGE | setups 5,667, target reached normally 54% | setups 19,853, target reached normally 55% | — |
