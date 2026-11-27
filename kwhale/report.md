# Kalshi commodity 15-min model report
Trained 2026-11-27 13:25 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 31347

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 406 windows · right 76% vs Kalshi 76% · logloss 0.4851 vs 0.4833 | 3701 windows · right 74% vs Kalshi 74% · logloss 0.506 vs 0.5056 | — |
| SILVER | 406 windows · right 76% vs Kalshi 76% · logloss 0.4885 vs 0.4881 | 3685 windows · right 74% vs Kalshi 74% · logloss 0.5098 vs 0.5102 | — |
| WTI | 436 windows · right 73% vs Kalshi 73% · logloss 0.536 vs 0.535 | 3910 windows · right 74% vs Kalshi 75% · logloss 0.5085 vs 0.5086 | — |
| BRENT | 436 windows · right 74% vs Kalshi 74% · logloss 0.5196 vs 0.5175 · edge bets 19: won 47%, ROI -15% | 1164 windows · right 75% vs Kalshi 75% · logloss 0.5035 vs 0.5032 · edge bets 1: won 100%, ROI +96% | — |
| COPPER | 406 windows · right 74% vs Kalshi 73% · logloss 0.5153 vs 0.5155 | 3354 windows · right 76% vs Kalshi 76% · logloss 0.494 vs 0.494 | — |
| NATGAS | 435 windows · right 76% vs Kalshi 75% · logloss 0.5026 vs 0.5051 · edge bets 3: won 67%, ROI +27% | 3583 windows · right 75% vs Kalshi 75% · logloss 0.4986 vs 0.4979 · edge bets 5: won 60%, ROI +12% | — |
| PALLADIUM | 406 windows · right 74% vs Kalshi 73% · logloss 0.5371 vs 0.5363 | 2133 windows · right 75% vs Kalshi 75% · logloss 0.5033 vs 0.5036 | — |
| PLATINUM | 405 windows · right 74% vs Kalshi 74% · logloss 0.5156 vs 0.5149 | 2488 windows · right 75% vs Kalshi 75% · logloss 0.5078 vs 0.5083 | — |

**All weeks:** 3336 windows · right 74% vs Kalshi 74% · logloss 0.5126 vs 0.5121 · edge bets 22: won 50%, ROI -9%

**All months:** 24018 windows · right 75% vs Kalshi 75% · logloss 0.504 vs 0.504 · edge bets 6: won 67%, ROI +25%

| Month | Result |
|---|---|
| 2026-08 | 1619 windows · right 75% vs Kalshi 75% · logloss 0.494 vs 0.4935 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5084 vs 0.5083 · edge bets 1: won 0%, ROI -100% |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.5055 vs 0.5055 · edge bets 5: won 80%, ROI +51% |
| 2026-11 | 3519 windows · right 76% vs Kalshi 75% · logloss 0.4951 vs 0.495 |

Strongest signals: `s_ASIA` -0.030, `m_NATGAS` +0.025, `tleft` -0.022, `m_PALLADIUM` -0.022, `dmid5` +0.021

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,718, target reached normally 20% | setups 14,991, target reached normally 20% | — |
| SILVER | setups 1,750, target reached normally 22% | setups 15,001, target reached normally 21% | — |
| WTI | setups 1,709, target reached normally 23% | setups 16,008, target reached normally 21% | — |
| BRENT | setups 2,039, target reached normally 19% | setups 5,027, target reached normally 15% | — |
| COPPER | setups 1,906, target reached normally 20% | setups 15,276, target reached normally 15% | — |
| NATGAS | setups 1,825, target reached normally 19% | setups 16,005, target reached normally 16% | — |
| PALLADIUM | setups 1,789, target reached normally 20% | setups 8,672, target reached normally 14% | — |
| PLATINUM | setups 1,889, target reached normally 20% | setups 10,219, target reached normally 16% | — |

**All weeks:** setups 14,625, target reached normally 20%

**All months:** setups 101,199, target reached normally 18%
