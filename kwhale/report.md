# Kalshi commodity 15-min model report
Trained 2026-11-14 14:49 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 13937

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 401 windows · right 73% vs Kalshi 74% · logloss 0.5197 vs 0.5176 · edge bets 1: won 0%, ROI -100% | 3317 windows · right 74% vs Kalshi 74% · logloss 0.5057 vs 0.5062 | — |
| SILVER | 401 windows · right 75% vs Kalshi 75% · logloss 0.5113 vs 0.5091 | 3308 windows · right 74% vs Kalshi 74% · logloss 0.5085 vs 0.5093 | — |
| WTI | 449 windows · right 74% vs Kalshi 74% · logloss 0.5156 vs 0.5135 · edge bets 6: won 17%, ROI -72% | 3467 windows · right 75% vs Kalshi 75% · logloss 0.5006 vs 0.5011 | — |
| BRENT | 449 windows · right 75% vs Kalshi 75% · logloss 0.506 vs 0.505 · edge bets 1: won 100%, ROI +61% | 215 windows · right 79% vs Kalshi 79% · logloss 0.4481 vs 0.4521 | — |
| COPPER | 401 windows · right 75% vs Kalshi 75% · logloss 0.497 vs 0.4969 | 2475 windows · right 75% vs Kalshi 75% · logloss 0.5009 vs 0.5013 | — |
| NATGAS | 448 windows · right 73% vs Kalshi 74% · logloss 0.5309 vs 0.5305 | 2634 windows · right 75% vs Kalshi 75% · logloss 0.4983 vs 0.4988 | — |
| PALLADIUM | 401 windows · right 75% vs Kalshi 76% · logloss 0.5082 vs 0.5063 | 1254 windows · right 75% vs Kalshi 74% · logloss 0.5101 vs 0.5122 | — |
| PLATINUM | 401 windows · right 73% vs Kalshi 73% · logloss 0.538 vs 0.5356 | 1609 windows · right 75% vs Kalshi 75% · logloss 0.4998 vs 0.5012 | — |

**All weeks:** 3351 windows · right 74% vs Kalshi 74% · logloss 0.5159 vs 0.5144 · edge bets 8: won 25%, ROI -57%

**All months:** 18279 windows · right 75% vs Kalshi 75% · logloss 0.5026 vs 0.5034

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4979 vs 0.4983 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5079 vs 0.5083 |
| 2026-10 | 8423 windows · right 75% vs Kalshi 75% · logloss 0.5 vs 0.5013 |

Strongest signals: `s_ASIA` -0.043, `dmid5` +0.034, `ofi3` +0.025, `s_EU` +0.024, `m_BRENT` +0.023

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,732, target reached normally 24% | setups 13,778, target reached normally 19% | — |
| SILVER | setups 1,679, target reached normally 22% | setups 13,904, target reached normally 21% | — |
| WTI | setups 1,788, target reached normally 19% | setups 14,481, target reached normally 20% | — |
| BRENT | setups 2,081, target reached normally 18% | setups 865, target reached normally 10% | — |
| COPPER | setups 2,049, target reached normally 16% | setups 11,020, target reached normally 16% | — |
| NATGAS | setups 1,868, target reached normally 17% | setups 11,569, target reached normally 16% | — |
| PALLADIUM | setups 1,902, target reached normally 18% | setups 4,756, target reached normally 14% | — |
| PLATINUM | setups 1,806, target reached normally 20% | setups 6,510, target reached normally 14% | — |

**All weeks:** setups 14,905, target reached normally 19%

**All months:** setups 76,883, target reached normally 18%
