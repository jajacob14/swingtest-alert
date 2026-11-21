# Kalshi commodity 15-min model report
Trained 2026-11-21 03:47 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 22883

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 401 windows · right 75% vs Kalshi 75% · logloss 0.4909 vs 0.4922 | 3529 windows · right 74% vs Kalshi 74% · logloss 0.5089 vs 0.5088 | — |
| SILVER | 401 windows · right 75% vs Kalshi 76% · logloss 0.4967 vs 0.4954 | 3512 windows · right 74% vs Kalshi 74% · logloss 0.5074 vs 0.5083 | — |
| WTI | 449 windows · right 75% vs Kalshi 75% · logloss 0.4916 vs 0.4942 | 3703 windows · right 75% vs Kalshi 75% · logloss 0.5063 vs 0.5066 | — |
| BRENT | 449 windows · right 76% vs Kalshi 76% · logloss 0.4847 vs 0.4857 | 711 windows · right 74% vs Kalshi 74% · logloss 0.5109 vs 0.5112 | — |
| COPPER | 401 windows · right 74% vs Kalshi 74% · logloss 0.5206 vs 0.521 | 2922 windows · right 76% vs Kalshi 75% · logloss 0.4977 vs 0.4982 | — |
| NATGAS | 448 windows · right 75% vs Kalshi 75% · logloss 0.5004 vs 0.5022 | 3130 windows · right 75% vs Kalshi 75% · logloss 0.4996 vs 0.4989 · edge bets 36: won 44%, ROI -19% | — |
| PALLADIUM | 401 windows · right 74% vs Kalshi 74% · logloss 0.5094 vs 0.5088 | 1701 windows · right 75% vs Kalshi 75% · logloss 0.5061 vs 0.5076 | — |
| PLATINUM | 401 windows · right 75% vs Kalshi 75% · logloss 0.4995 vs 0.4996 | 2056 windows · right 75% vs Kalshi 75% · logloss 0.5038 vs 0.5049 | — |

**All weeks:** 3351 windows · right 75% vs Kalshi 75% · logloss 0.4988 vs 0.4996

**All months:** 21264 windows · right 75% vs Kalshi 75% · logloss 0.5046 vs 0.505 · edge bets 36: won 44%, ROI -19%

| Month | Result |
|---|---|
| 2026-08 | 2384 windows · right 76% vs Kalshi 75% · logloss 0.4926 vs 0.4932 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5081 vs 0.5083 · edge bets 8: won 12%, ROI -78% |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.5051 vs 0.5055 · edge bets 28: won 54%, ROI -1% |

Strongest signals: `s_ASIA` -0.038, `s_EU` +0.029, `dmid5` +0.025, `ofi3` +0.024, `tleft` -0.024

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,685, target reached normally 20% | setups 14,397, target reached normally 20% | — |
| SILVER | setups 1,714, target reached normally 22% | setups 14,435, target reached normally 21% | — |
| WTI | setups 1,830, target reached normally 21% | setups 15,403, target reached normally 20% | — |
| BRENT | setups 2,126, target reached normally 20% | setups 2,959, target reached normally 14% | — |
| COPPER | setups 2,016, target reached normally 19% | setups 13,081, target reached normally 16% | — |
| NATGAS | setups 1,721, target reached normally 16% | setups 14,006, target reached normally 16% | — |
| PALLADIUM | setups 1,768, target reached normally 17% | setups 6,673, target reached normally 14% | — |
| PLATINUM | setups 2,016, target reached normally 20% | setups 8,309, target reached normally 15% | — |

**All weeks:** setups 14,876, target reached normally 19%

**All months:** setups 89,263, target reached normally 18%
