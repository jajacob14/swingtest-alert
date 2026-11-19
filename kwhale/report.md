# Kalshi commodity 15-min model report
Trained 2026-11-18 22:34 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 19496

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 400 windows · right 75% vs Kalshi 75% · logloss 0.4921 vs 0.4928 | 3478 windows · right 74% vs Kalshi 74% · logloss 0.5106 vs 0.5104 | — |
| SILVER | 400 windows · right 75% vs Kalshi 75% · logloss 0.501 vs 0.5007 | 3462 windows · right 74% vs Kalshi 74% · logloss 0.5101 vs 0.5113 | — |
| WTI | 447 windows · right 73% vs Kalshi 74% · logloss 0.512 vs 0.5113 | 3632 windows · right 75% vs Kalshi 75% · logloss 0.5059 vs 0.506 | — |
| BRENT | 448 windows · right 74% vs Kalshi 75% · logloss 0.4902 vs 0.491 | 525 windows · right 75% vs Kalshi 76% · logloss 0.4919 vs 0.4908 | — |
| COPPER | 399 windows · right 77% vs Kalshi 77% · logloss 0.4849 vs 0.4866 | 2769 windows · right 75% vs Kalshi 75% · logloss 0.4998 vs 0.5005 | — |
| NATGAS | 448 windows · right 75% vs Kalshi 75% · logloss 0.4982 vs 0.5004 | 2944 windows · right 75% vs Kalshi 75% · logloss 0.4984 vs 0.4981 | — |
| PALLADIUM | 399 windows · right 75% vs Kalshi 74% · logloss 0.5094 vs 0.5092 | 1548 windows · right 75% vs Kalshi 74% · logloss 0.5084 vs 0.5103 | — |
| PLATINUM | 399 windows · right 75% vs Kalshi 75% · logloss 0.5012 vs 0.5017 | 1903 windows · right 75% vs Kalshi 75% · logloss 0.4996 vs 0.5012 | — |

**All weeks:** 3340 windows · right 75% vs Kalshi 75% · logloss 0.4988 vs 0.4993

**All months:** 20261 windows · right 75% vs Kalshi 75% · logloss 0.5047 vs 0.5052

| Month | Result |
|---|---|
| 2026-08 | 2704 windows · right 75% vs Kalshi 75% · logloss 0.5024 vs 0.5029 |
| 2026-09 | 6734 windows · right 75% vs Kalshi 74% · logloss 0.5081 vs 0.5083 |
| 2026-10 | 10823 windows · right 75% vs Kalshi 75% · logloss 0.5032 vs 0.5038 |

Strongest signals: `s_ASIA` -0.047, `s_EU` +0.036, `ofi3` +0.029, `dmid5` +0.026, `tleft` -0.021

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,696, target reached normally 20% | setups 14,273, target reached normally 20% | — |
| SILVER | setups 1,683, target reached normally 19% | setups 14,295, target reached normally 21% | — |
| WTI | setups 1,788, target reached normally 21% | setups 15,177, target reached normally 20% | — |
| BRENT | setups 2,083, target reached normally 19% | setups 2,233, target reached normally 12% | — |
| COPPER | setups 2,083, target reached normally 16% | setups 12,293, target reached normally 16% | — |
| NATGAS | setups 1,692, target reached normally 15% | setups 13,185, target reached normally 16% | — |
| PALLADIUM | setups 1,885, target reached normally 16% | setups 5,951, target reached normally 14% | — |
| PLATINUM | setups 1,926, target reached normally 19% | setups 7,619, target reached normally 15% | — |

**All weeks:** setups 14,836, target reached normally 18%

**All months:** setups 85,026, target reached normally 18%
