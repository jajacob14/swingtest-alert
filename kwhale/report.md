# Kalshi commodity 15-min model report
Trained 2026-11-22 22:19 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 23065

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 400 windows · right 76% vs Kalshi 76% · logloss 0.4883 vs 0.4895 | 3438 windows · right 74% vs Kalshi 74% · logloss 0.5055 vs 0.5052 | — |
| SILVER | 400 windows · right 76% vs Kalshi 76% · logloss 0.4931 vs 0.4918 | 3423 windows · right 74% vs Kalshi 74% · logloss 0.5059 vs 0.5068 | — |
| WTI | 450 windows · right 75% vs Kalshi 75% · logloss 0.4959 vs 0.4982 | 3626 windows · right 74% vs Kalshi 74% · logloss 0.5084 vs 0.5086 | — |
| BRENT | 450 windows · right 76% vs Kalshi 76% · logloss 0.4862 vs 0.4874 | 728 windows · right 74% vs Kalshi 74% · logloss 0.5101 vs 0.5106 | — |
| COPPER | 401 windows · right 74% vs Kalshi 74% · logloss 0.5174 vs 0.518 | 2938 windows · right 76% vs Kalshi 76% · logloss 0.4973 vs 0.4977 | — |
| NATGAS | 449 windows · right 74% vs Kalshi 74% · logloss 0.5024 vs 0.504 · edge bets 1: won 100%, ROI +75% | 3147 windows · right 75% vs Kalshi 75% · logloss 0.4998 vs 0.4991 · edge bets 38: won 42%, ROI -22% | — |
| PALLADIUM | 401 windows · right 74% vs Kalshi 74% · logloss 0.5063 vs 0.506 | 1717 windows · right 75% vs Kalshi 75% · logloss 0.5055 vs 0.5072 | — |
| PLATINUM | 400 windows · right 75% vs Kalshi 75% · logloss 0.4947 vs 0.4948 | 2072 windows · right 75% vs Kalshi 75% · logloss 0.5041 vs 0.5051 | — |

**All weeks:** 3351 windows · right 75% vs Kalshi 75% · logloss 0.4979 vs 0.4986 · edge bets 1: won 100%, ROI +75%

**All months:** 21089 windows · right 75% vs Kalshi 75% · logloss 0.5041 vs 0.5044 · edge bets 38: won 42%, ROI -22%

| Month | Result |
|---|---|
| 2026-08 | 2078 windows · right 76% vs Kalshi 76% · logloss 0.4873 vs 0.4877 · edge bets 1: won 0%, ROI -100% |
| 2026-09 | 6734 windows · right 75% vs Kalshi 74% · logloss 0.5082 vs 0.5083 · edge bets 10: won 20%, ROI -64% |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.505 vs 0.5055 · edge bets 27: won 52%, ROI -4% |
| 2026-11 | 131 windows · right 76% vs Kalshi 76% · logloss 0.47 vs 0.47 |

Strongest signals: `s_ASIA` -0.037, `s_EU` +0.028, `tleft` -0.026, `m_PALLADIUM` -0.025, `ofi3` +0.025

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,692, target reached normally 20% | setups 14,024, target reached normally 20% | — |
| SILVER | setups 1,739, target reached normally 22% | setups 14,071, target reached normally 21% | — |
| WTI | setups 1,830, target reached normally 21% | setups 15,012, target reached normally 20% | — |
| BRENT | setups 2,112, target reached normally 20% | setups 3,046, target reached normally 14% | — |
| COPPER | setups 2,004, target reached normally 20% | setups 13,172, target reached normally 15% | — |
| NATGAS | setups 1,744, target reached normally 15% | setups 14,079, target reached normally 16% | — |
| PALLADIUM | setups 1,750, target reached normally 17% | setups 6,749, target reached normally 14% | — |
| PLATINUM | setups 2,035, target reached normally 20% | setups 8,375, target reached normally 15% | — |

**All weeks:** setups 14,906, target reached normally 19%

**All months:** setups 88,528, target reached normally 18%
