# Kalshi crypto 15-min model report
Trained 2026-11-22 05:34 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 307847

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 74% vs Kalshi 74% · logloss 0.5024 vs 0.5023 · edge bets 5: won 60%, ROI +4% | 3345 windows · right 75% vs Kalshi 75% · logloss 0.5009 vs 0.501 · edge bets 4: won 25%, ROI -56% | — |
| ETH | 597 windows · right 74% vs Kalshi 74% · logloss 0.5117 vs 0.5102 · edge bets 4: won 75%, ROI +47% | 3191 windows · right 77% vs Kalshi 77% · logloss 0.4776 vs 0.477 | — |
| SOL | 598 windows · right 74% vs Kalshi 74% · logloss 0.5064 vs 0.5054 · edge bets 13: won 54%, ROI -7% | 3191 windows · right 76% vs Kalshi 76% · logloss 0.4866 vs 0.4866 | — |
| XRP | 598 windows · right 75% vs Kalshi 75% · logloss 0.5124 vs 0.5117 · edge bets 22: won 50%, ROI -10% | 3188 windows · right 76% vs Kalshi 76% · logloss 0.4817 vs 0.4819 · edge bets 13: won 62%, ROI +16% | — |
| DOGE | 598 windows · right 75% vs Kalshi 76% · logloss 0.4989 vs 0.4983 · edge bets 16: won 50%, ROI -5% | 3189 windows · right 76% vs Kalshi 76% · logloss 0.477 vs 0.4781 · edge bets 4: won 100%, ROI +91% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.5064 vs 0.5055 · edge bets 60: won 53%, ROI -3%

**All months:** 16104 windows · right 76% vs Kalshi 76% · logloss 0.485 vs 0.4851 · edge bets 21: won 62%, ROI +16%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4632 vs 0.4642 · edge bets 3: won 67%, ROI +27% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4718 vs 0.4719 · edge bets 5: won 40%, ROI -23% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4969 vs 0.4969 · edge bets 11: won 64%, ROI +16% |
| 2026-11 | 215 windows · right 80% vs Kalshi 80% · logloss 0.4206 vs 0.4212 · edge bets 2: won 100%, ROI +92% |

Strongest signals: `sgap` +0.047, `s_EU` +0.035, `dmid5` +0.027, `m_XRP` +0.020, `s_US` -0.020

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,499, target reached normally 22% | setups 13,461, target reached normally 19% | — |
| ETH | setups 2,443, target reached normally 25% | setups 13,432, target reached normally 20% | — |
| SOL | setups 2,527, target reached normally 22% | setups 13,627, target reached normally 21% | — |
| XRP | setups 2,561, target reached normally 26% | setups 13,944, target reached normally 20% | — |
| DOGE | setups 2,488, target reached normally 22% | setups 13,720, target reached normally 20% | — |

**All weeks:** setups 12,518, target reached normally 23%

**All months:** setups 68,184, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,814, target reached normally 57% | setups 34,386, target reached normally 56% | — |
| ETH | setups 5,731, target reached normally 57% | setups 30,886, target reached normally 55% | — |
| SOL | setups 5,684, target reached normally 56% | setups 30,517, target reached normally 56% | — |
| XRP | setups 5,424, target reached normally 57% | setups 30,703, target reached normally 56% | — |
| DOGE | setups 5,656, target reached normally 56% | setups 30,487, target reached normally 56% | — |
