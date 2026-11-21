# Kalshi commodity 15-min model report
Trained 2026-11-20 20:37 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 22766

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 405 windows · right 75% vs Kalshi 75% · logloss 0.4955 vs 0.4965 | 3529 windows · right 74% vs Kalshi 74% · logloss 0.5088 vs 0.5088 | — |
| SILVER | 406 windows · right 75% vs Kalshi 75% · logloss 0.4982 vs 0.4974 | 3512 windows · right 74% vs Kalshi 74% · logloss 0.5074 vs 0.5083 | — |
| WTI | 440 windows · right 75% vs Kalshi 75% · logloss 0.4932 vs 0.4957 | 3706 windows · right 75% vs Kalshi 75% · logloss 0.5065 vs 0.5068 | — |
| BRENT | 440 windows · right 76% vs Kalshi 76% · logloss 0.4834 vs 0.4847 | 701 windows · right 74% vs Kalshi 75% · logloss 0.5079 vs 0.5084 | — |
| COPPER | 406 windows · right 74% vs Kalshi 74% · logloss 0.5215 vs 0.5217 | 2922 windows · right 76% vs Kalshi 75% · logloss 0.4977 vs 0.4982 | — |
| NATGAS | 439 windows · right 74% vs Kalshi 74% · logloss 0.502 vs 0.5043 | 3120 windows · right 75% vs Kalshi 75% · logloss 0.499 vs 0.4985 · edge bets 16: won 44%, ROI -20% | — |
| PALLADIUM | 406 windows · right 74% vs Kalshi 74% · logloss 0.5089 vs 0.5081 | 1701 windows · right 75% vs Kalshi 75% · logloss 0.506 vs 0.5076 | — |
| PLATINUM | 406 windows · right 75% vs Kalshi 75% · logloss 0.5 vs 0.5 | 2056 windows · right 75% vs Kalshi 75% · logloss 0.5038 vs 0.5049 | — |

**All weeks:** 3348 windows · right 75% vs Kalshi 75% · logloss 0.5 vs 0.5008

**All months:** 21247 windows · right 75% vs Kalshi 75% · logloss 0.5044 vs 0.5049 · edge bets 16: won 44%, ROI -20%

| Month | Result |
|---|---|
| 2026-08 | 2397 windows · right 75% vs Kalshi 75% · logloss 0.4929 vs 0.4935 |
| 2026-09 | 6734 windows · right 75% vs Kalshi 74% · logloss 0.5081 vs 0.5083 · edge bets 4: won 25%, ROI -55% |
| 2026-10 | 12116 windows · right 75% vs Kalshi 75% · logloss 0.5047 vs 0.5052 · edge bets 12: won 50%, ROI -8% |

Strongest signals: `s_ASIA` -0.038, `s_EU` +0.029, `ofi3` +0.024, `dmid5` +0.024, `tleft` -0.023

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,691, target reached normally 20% | setups 14,397, target reached normally 20% | — |
| SILVER | setups 1,729, target reached normally 22% | setups 14,435, target reached normally 21% | — |
| WTI | setups 1,801, target reached normally 22% | setups 15,426, target reached normally 20% | — |
| BRENT | setups 2,098, target reached normally 20% | setups 2,953, target reached normally 14% | — |
| COPPER | setups 2,045, target reached normally 20% | setups 13,081, target reached normally 16% | — |
| NATGAS | setups 1,700, target reached normally 16% | setups 13,996, target reached normally 16% | — |
| PALLADIUM | setups 1,785, target reached normally 17% | setups 6,673, target reached normally 14% | — |
| PLATINUM | setups 2,023, target reached normally 20% | setups 8,309, target reached normally 15% | — |

**All weeks:** setups 14,872, target reached normally 20%

**All months:** setups 89,270, target reached normally 18%
