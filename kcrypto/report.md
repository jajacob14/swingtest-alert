# Kalshi crypto 15-min model report
Trained 2026-11-14 13:49 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 137228

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 75% vs Kalshi 75% · logloss 0.4978 vs 0.4974 · edge bets 18: won 39%, ROI -35% | 2618 windows · right 75% vs Kalshi 75% · logloss 0.4982 vs 0.4982 · edge bets 8: won 50%, ROI -15% | — |
| ETH | 596 windows · right 74% vs Kalshi 75% · logloss 0.5097 vs 0.5091 · edge bets 6: won 33%, ROI -42% | 2464 windows · right 77% vs Kalshi 77% · logloss 0.4699 vs 0.4695 · edge bets 6: won 33%, ROI -45% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.4979 vs 0.4993 · edge bets 11: won 46%, ROI -16% | 2464 windows · right 77% vs Kalshi 77% · logloss 0.4813 vs 0.4812 · edge bets 1: won 100%, ROI +79% | — |
| XRP | 598 windows · right 76% vs Kalshi 76% · logloss 0.5035 vs 0.4998 · edge bets 35: won 63%, ROI +10% | 2461 windows · right 77% vs Kalshi 77% · logloss 0.4735 vs 0.474 · edge bets 41: won 61%, ROI +12% | — |
| DOGE | 598 windows · right 74% vs Kalshi 74% · logloss 0.5063 vs 0.5071 · edge bets 7: won 57%, ROI -5% | 2462 windows · right 77% vs Kalshi 76% · logloss 0.4749 vs 0.4761 · edge bets 7: won 86%, ROI +61% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.503 vs 0.5025 · edge bets 77: won 52%, ROI -10%

**All months:** 12469 windows · right 76% vs Kalshi 76% · logloss 0.4799 vs 0.4801 · edge bets 63: won 60%, ROI +8%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4634 vs 0.4642 · edge bets 13: won 62%, ROI +11% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4715 vs 0.4719 · edge bets 28: won 57%, ROI +1% |
| 2026-10 | 6110 windows · right 76% vs Kalshi 76% · logloss 0.491 vs 0.4909 · edge bets 22: won 64%, ROI +17% |

Strongest signals: `sgap` +0.058, `s_EU` +0.036, `tleft` -0.030, `dmid5` +0.027, `vcum` -0.021

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,508, target reached normally 23% | setups 10,562, target reached normally 19% | — |
| ETH | setups 2,429, target reached normally 25% | setups 10,521, target reached normally 19% | — |
| SOL | setups 2,548, target reached normally 22% | setups 10,680, target reached normally 21% | — |
| XRP | setups 2,588, target reached normally 24% | setups 10,915, target reached normally 20% | — |
| DOGE | setups 2,592, target reached normally 24% | setups 10,629, target reached normally 20% | — |

**All weeks:** setups 12,665, target reached normally 23%

**All months:** setups 53,307, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,623, target reached normally 55% | setups 27,038, target reached normally 55% | — |
| ETH | setups 5,676, target reached normally 56% | setups 23,713, target reached normally 54% | — |
| SOL | setups 5,594, target reached normally 56% | setups 23,602, target reached normally 55% | — |
| XRP | setups 5,442, target reached normally 54% | setups 23,697, target reached normally 55% | — |
| DOGE | setups 5,532, target reached normally 56% | setups 23,459, target reached normally 56% | — |
