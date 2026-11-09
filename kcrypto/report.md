# Kalshi crypto 15-min model report
Trained 2026-11-09 08:08 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 35644

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 74% vs Kalshi 74% · logloss 0.5108 vs 0.5113 · edge bets 35: won 71%, ROI +24% | 2123 windows · right 76% vs Kalshi 76% · logloss 0.4932 vs 0.4932 · edge bets 24: won 67%, ROI +10% | — |
| ETH | 597 windows · right 75% vs Kalshi 76% · logloss 0.5042 vs 0.503 · edge bets 17: won 47%, ROI -17% | 1969 windows · right 78% vs Kalshi 78% · logloss 0.4612 vs 0.4606 · edge bets 3: won 33%, ROI -43% | — |
| SOL | 598 windows · right 74% vs Kalshi 74% · logloss 0.5156 vs 0.5147 · edge bets 35: won 43%, ROI -21% | 1969 windows · right 76% vs Kalshi 76% · logloss 0.4805 vs 0.4805 · edge bets 4: won 25%, ROI -59% | — |
| XRP | 598 windows · right 74% vs Kalshi 74% · logloss 0.5218 vs 0.519 · edge bets 21: won 52%, ROI -6% | 1966 windows · right 77% vs Kalshi 77% · logloss 0.4698 vs 0.4708 · edge bets 27: won 56%, ROI +4% | — |
| DOGE | 598 windows · right 76% vs Kalshi 76% · logloss 0.4963 vs 0.4941 · edge bets 69: won 55%, ROI +2% | 1967 windows · right 78% vs Kalshi 78% · logloss 0.4607 vs 0.4617 · edge bets 14: won 64%, ROI +19% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.5097 vs 0.5084 · edge bets 177: won 55%, ROI -1%

**All months:** 9994 windows · right 77% vs Kalshi 77% · logloss 0.4735 vs 0.4738 · edge bets 72: won 58%, ROI +3%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4632 vs 0.4642 · edge bets 8: won 62%, ROI +14% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4713 vs 0.4719 · edge bets 32: won 62%, ROI +9% |
| 2026-10 | 3635 windows · right 76% vs Kalshi 76% · logloss 0.481 vs 0.4806 · edge bets 32: won 53%, ROI -6% |

Strongest signals: `sgap` +0.063, `dmid5` +0.031, `dmid1` -0.029, `s_EU` +0.027, `m_XRP` +0.026

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,360, target reached normally 22% | setups 8,593, target reached normally 18% | — |
| ETH | setups 2,505, target reached normally 22% | setups 8,492, target reached normally 18% | — |
| SOL | setups 2,520, target reached normally 24% | setups 8,656, target reached normally 20% | — |
| XRP | setups 2,476, target reached normally 22% | setups 8,734, target reached normally 19% | — |
| DOGE | setups 2,650, target reached normally 21% | setups 8,604, target reached normally 19% | — |

**All weeks:** setups 12,511, target reached normally 22%

**All months:** setups 43,079, target reached normally 19%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 6,141, target reached normally 57% | setups 22,078, target reached normally 55% | — |
| ETH | setups 5,860, target reached normally 56% | setups 19,007, target reached normally 53% | — |
| SOL | setups 5,760, target reached normally 57% | setups 18,833, target reached normally 55% | — |
| XRP | setups 5,688, target reached normally 56% | setups 19,049, target reached normally 54% | — |
| DOGE | setups 5,660, target reached normally 55% | setups 18,664, target reached normally 55% | — |
