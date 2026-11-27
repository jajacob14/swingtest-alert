# Kalshi commodity 15-min model report
Trained 2026-11-27 03:49 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 30499

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 395 windows · right 76% vs Kalshi 76% · logloss 0.4802 vs 0.4792 | 3685 windows · right 74% vs Kalshi 74% · logloss 0.5061 vs 0.5054 | — |
| SILVER | 395 windows · right 76% vs Kalshi 76% · logloss 0.4809 vs 0.48 | 3669 windows · right 74% vs Kalshi 74% · logloss 0.5098 vs 0.5103 | — |
| WTI | 454 windows · right 73% vs Kalshi 73% · logloss 0.5345 vs 0.5336 | 3893 windows · right 74% vs Kalshi 74% · logloss 0.5093 vs 0.5094 | — |
| BRENT | 454 windows · right 74% vs Kalshi 74% · logloss 0.5163 vs 0.5144 · edge bets 3: won 0%, ROI -100% | 1126 windows · right 75% vs Kalshi 75% · logloss 0.5069 vs 0.5066 | — |
| COPPER | 395 windows · right 73% vs Kalshi 73% · logloss 0.5181 vs 0.5174 | 3316 windows · right 76% vs Kalshi 76% · logloss 0.4946 vs 0.4948 | — |
| NATGAS | 454 windows · right 75% vs Kalshi 75% · logloss 0.5054 vs 0.5082 | 3545 windows · right 75% vs Kalshi 75% · logloss 0.4987 vs 0.4982 · edge bets 2: won 50%, ROI -4% | — |
| PALLADIUM | 394 windows · right 74% vs Kalshi 74% · logloss 0.5284 vs 0.5282 | 2095 windows · right 75% vs Kalshi 75% · logloss 0.5054 vs 0.5056 | — |
| PLATINUM | 395 windows · right 75% vs Kalshi 75% · logloss 0.5056 vs 0.5049 | 2450 windows · right 75% vs Kalshi 74% · logloss 0.5087 vs 0.5092 | — |

**All weeks:** 3336 windows · right 74% vs Kalshi 75% · logloss 0.5093 vs 0.5089 · edge bets 3: won 0%, ROI -100%

**All months:** 23779 windows · right 75% vs Kalshi 75% · logloss 0.5047 vs 0.5047 · edge bets 2: won 50%, ROI -4%

| Month | Result |
|---|---|
| 2026-08 | 1684 windows · right 75% vs Kalshi 75% · logloss 0.4924 vs 0.492 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5084 vs 0.5083 |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.5054 vs 0.5055 · edge bets 2: won 50%, ROI -4% |
| 2026-11 | 3215 windows · right 75% vs Kalshi 75% · logloss 0.5008 vs 0.5007 |

Strongest signals: `s_ASIA` -0.032, `m_NATGAS` +0.025, `tleft` -0.022, `dmid5` +0.022, `m_PALLADIUM` -0.020

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,667, target reached normally 19% | setups 14,929, target reached normally 20% | — |
| SILVER | setups 1,718, target reached normally 22% | setups 14,954, target reached normally 21% | — |
| WTI | setups 1,781, target reached normally 23% | setups 15,955, target reached normally 21% | — |
| BRENT | setups 2,092, target reached normally 20% | setups 4,845, target reached normally 15% | — |
| COPPER | setups 1,860, target reached normally 20% | setups 15,065, target reached normally 15% | — |
| NATGAS | setups 1,852, target reached normally 18% | setups 15,869, target reached normally 16% | — |
| PALLADIUM | setups 1,732, target reached normally 20% | setups 8,495, target reached normally 14% | — |
| PLATINUM | setups 1,887, target reached normally 19% | setups 10,059, target reached normally 16% | — |

**All weeks:** setups 14,589, target reached normally 20%

**All months:** setups 100,171, target reached normally 18%
