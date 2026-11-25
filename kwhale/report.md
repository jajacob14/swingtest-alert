# Kalshi commodity 15-min model report
Trained 2026-11-25 08:56 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 27355

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 403 windows · right 74% vs Kalshi 74% · logloss 0.5097 vs 0.5092 | 3625 windows · right 74% vs Kalshi 74% · logloss 0.5053 vs 0.505 | — |
| SILVER | 403 windows · right 76% vs Kalshi 76% · logloss 0.4843 vs 0.4825 | 3610 windows · right 74% vs Kalshi 74% · logloss 0.5061 vs 0.5068 | — |
| WTI | 446 windows · right 75% vs Kalshi 75% · logloss 0.5049 vs 0.5056 | 3823 windows · right 74% vs Kalshi 74% · logloss 0.5077 vs 0.508 | — |
| BRENT | 445 windows · right 76% vs Kalshi 76% · logloss 0.4877 vs 0.4864 · edge bets 8: won 38%, ROI -30% | 962 windows · right 75% vs Kalshi 75% · logloss 0.5005 vs 0.5006 | — |
| COPPER | 402 windows · right 72% vs Kalshi 72% · logloss 0.5329 vs 0.5312 | 3162 windows · right 76% vs Kalshi 76% · logloss 0.4962 vs 0.4965 | — |
| NATGAS | 447 windows · right 76% vs Kalshi 76% · logloss 0.4776 vs 0.4804 · edge bets 1: won 100%, ROI +89% | 3381 windows · right 75% vs Kalshi 75% · logloss 0.4996 vs 0.4989 · edge bets 1: won 0%, ROI -100% | — |
| PALLADIUM | 402 windows · right 72% vs Kalshi 72% · logloss 0.5464 vs 0.5445 | 1941 windows · right 75% vs Kalshi 75% · logloss 0.5076 vs 0.5085 | — |
| PLATINUM | 403 windows · right 72% vs Kalshi 73% · logloss 0.5421 vs 0.5411 | 2296 windows · right 75% vs Kalshi 75% · logloss 0.5054 vs 0.5062 | — |

**All weeks:** 3351 windows · right 74% vs Kalshi 74% · logloss 0.5097 vs 0.5092 · edge bets 9: won 44%, ROI -17%

**All months:** 22800 windows · right 75% vs Kalshi 75% · logloss 0.5037 vs 0.5039 · edge bets 1: won 0%, ROI -100%

| Month | Result |
|---|---|
| 2026-08 | 1967 windows · right 76% vs Kalshi 76% · logloss 0.491 vs 0.4911 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5082 vs 0.5083 |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.5053 vs 0.5055 · edge bets 1: won 0%, ROI -100% |
| 2026-11 | 1953 windows · right 75% vs Kalshi 75% · logloss 0.4908 vs 0.4916 |

Strongest signals: `s_ASIA` -0.035, `m_NATGAS` +0.030, `tleft` -0.025, `dmid5` +0.023, `m_PALLADIUM` -0.022

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,653, target reached normally 21% | setups 14,747, target reached normally 20% | — |
| SILVER | setups 1,712, target reached normally 22% | setups 14,839, target reached normally 21% | — |
| WTI | setups 1,807, target reached normally 21% | setups 15,778, target reached normally 21% | — |
| BRENT | setups 2,134, target reached normally 17% | setups 4,149, target reached normally 14% | — |
| COPPER | setups 1,941, target reached normally 21% | setups 14,202, target reached normally 15% | — |
| NATGAS | setups 1,928, target reached normally 16% | setups 15,123, target reached normally 16% | — |
| PALLADIUM | setups 1,675, target reached normally 20% | setups 7,772, target reached normally 14% | — |
| PLATINUM | setups 1,939, target reached normally 20% | setups 9,375, target reached normally 15% | — |

**All weeks:** setups 14,789, target reached normally 20%

**All months:** setups 95,985, target reached normally 18%
