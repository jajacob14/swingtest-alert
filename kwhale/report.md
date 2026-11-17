# Kalshi commodity 15-min model report
Trained 2026-11-17 00:30 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 16095

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 399 windows · right 73% vs Kalshi 74% · logloss 0.5262 vs 0.5239 | 3356 windows · right 74% vs Kalshi 74% · logloss 0.5097 vs 0.51 | — |
| SILVER | 399 windows · right 74% vs Kalshi 74% · logloss 0.517 vs 0.5144 · edge bets 1: won 100%, ROI +92% | 3339 windows · right 74% vs Kalshi 74% · logloss 0.513 vs 0.5136 | — |
| WTI | 448 windows · right 75% vs Kalshi 76% · logloss 0.4975 vs 0.4951 | 3500 windows · right 75% vs Kalshi 75% · logloss 0.504 vs 0.5044 | — |
| BRENT | 448 windows · right 75% vs Kalshi 76% · logloss 0.4937 vs 0.4913 | 341 windows · right 76% vs Kalshi 76% · logloss 0.481 vs 0.4833 | — |
| COPPER | 399 windows · right 76% vs Kalshi 76% · logloss 0.4887 vs 0.4892 | 2595 windows · right 76% vs Kalshi 75% · logloss 0.4994 vs 0.5001 | — |
| NATGAS | 448 windows · right 75% vs Kalshi 75% · logloss 0.5084 vs 0.51 | 2760 windows · right 75% vs Kalshi 75% · logloss 0.4951 vs 0.4958 | — |
| PALLADIUM | 399 windows · right 75% vs Kalshi 74% · logloss 0.5169 vs 0.5123 | 1374 windows · right 75% vs Kalshi 75% · logloss 0.5071 vs 0.5091 | — |
| PLATINUM | 399 windows · right 74% vs Kalshi 74% · logloss 0.5263 vs 0.5238 | 1729 windows · right 75% vs Kalshi 75% · logloss 0.5017 vs 0.5029 | — |

**All weeks:** 3339 windows · right 75% vs Kalshi 75% · logloss 0.5088 vs 0.507 · edge bets 1: won 100%, ROI +92%

**All months:** 18994 windows · right 75% vs Kalshi 75% · logloss 0.5042 vs 0.5049

| Month | Result |
|---|---|
| 2026-08 | 2859 windows · right 75% vs Kalshi 75% · logloss 0.5013 vs 0.5019 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5081 vs 0.5083 |
| 2026-10 | 9401 windows · right 75% vs Kalshi 75% · logloss 0.5023 vs 0.5034 |

Strongest signals: `s_ASIA` -0.040, `s_EU` +0.029, `ofi3` +0.029, `dmid5` +0.027, `m_BRENT` +0.024

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,678, target reached normally 25% | setups 13,876, target reached normally 20% | — |
| SILVER | setups 1,665, target reached normally 21% | setups 13,856, target reached normally 21% | — |
| WTI | setups 1,834, target reached normally 18% | setups 14,646, target reached normally 20% | — |
| BRENT | setups 2,113, target reached normally 19% | setups 1,390, target reached normally 11% | — |
| COPPER | setups 2,003, target reached normally 15% | setups 11,552, target reached normally 16% | — |
| NATGAS | setups 1,786, target reached normally 16% | setups 12,253, target reached normally 16% | — |
| PALLADIUM | setups 1,926, target reached normally 18% | setups 5,293, target reached normally 14% | — |
| PLATINUM | setups 1,850, target reached normally 19% | setups 6,959, target reached normally 14% | — |

**All weeks:** setups 14,855, target reached normally 19%

**All months:** setups 79,825, target reached normally 18%
