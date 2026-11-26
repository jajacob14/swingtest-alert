# Kalshi commodity 15-min model report
Trained 2026-11-25 20:27 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 28342

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 401 windows · right 75% vs Kalshi 75% · logloss 0.5027 vs 0.5026 | 3642 windows · right 74% vs Kalshi 74% · logloss 0.5052 vs 0.5051 | — |
| SILVER | 400 windows · right 76% vs Kalshi 77% · logloss 0.489 vs 0.4878 | 3626 windows · right 74% vs Kalshi 74% · logloss 0.5081 vs 0.509 | — |
| WTI | 450 windows · right 74% vs Kalshi 74% · logloss 0.516 vs 0.5154 | 3845 windows · right 75% vs Kalshi 75% · logloss 0.5073 vs 0.5077 | — |
| BRENT | 450 windows · right 76% vs Kalshi 76% · logloss 0.4932 vs 0.4918 · edge bets 3: won 33%, ROI -43% | 1008 windows · right 75% vs Kalshi 75% · logloss 0.5011 vs 0.501 | — |
| COPPER | 399 windows · right 72% vs Kalshi 72% · logloss 0.531 vs 0.5293 | 3203 windows · right 76% vs Kalshi 76% · logloss 0.4961 vs 0.4964 | — |
| NATGAS | 450 windows · right 76% vs Kalshi 76% · logloss 0.4859 vs 0.4884 | 3427 windows · right 75% vs Kalshi 75% · logloss 0.4996 vs 0.499 | — |
| PALLADIUM | 401 windows · right 72% vs Kalshi 72% · logloss 0.55 vs 0.549 | 1982 windows · right 75% vs Kalshi 75% · logloss 0.5084 vs 0.5089 | — |
| PLATINUM | 400 windows · right 73% vs Kalshi 73% · logloss 0.5346 vs 0.5338 | 2337 windows · right 75% vs Kalshi 74% · logloss 0.5071 vs 0.5081 | — |

**All weeks:** 3351 windows · right 74% vs Kalshi 74% · logloss 0.5121 vs 0.5116 · edge bets 3: won 33%, ROI -43%

**All months:** 23070 windows · right 75% vs Kalshi 75% · logloss 0.5042 vs 0.5044

| Month | Result |
|---|---|
| 2026-08 | 1894 windows · right 76% vs Kalshi 76% · logloss 0.4918 vs 0.4918 |
| 2026-09 | 6734 windows · right 75% vs Kalshi 74% · logloss 0.5081 vs 0.5083 |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.5052 vs 0.5055 |
| 2026-11 | 2296 windows · right 75% vs Kalshi 75% · logloss 0.4972 vs 0.4978 |

Strongest signals: `s_ASIA` -0.038, `m_NATGAS` +0.028, `s_US` +0.024, `dmid5` +0.021, `tleft` -0.021

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,661, target reached normally 21% | setups 14,773, target reached normally 20% | — |
| SILVER | setups 1,727, target reached normally 23% | setups 14,827, target reached normally 21% | — |
| WTI | setups 1,837, target reached normally 22% | setups 15,876, target reached normally 21% | — |
| BRENT | setups 2,139, target reached normally 17% | setups 4,355, target reached normally 14% | — |
| COPPER | setups 1,904, target reached normally 20% | setups 14,400, target reached normally 15% | — |
| NATGAS | setups 1,953, target reached normally 16% | setups 15,286, target reached normally 16% | — |
| PALLADIUM | setups 1,724, target reached normally 21% | setups 7,971, target reached normally 14% | — |
| PLATINUM | setups 1,920, target reached normally 20% | setups 9,557, target reached normally 15% | — |

**All weeks:** setups 14,865, target reached normally 20%

**All months:** setups 97,045, target reached normally 18%
