# Kalshi commodity 15-min model report
Trained 2026-11-18 11:03 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 18605

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 401 windows · right 74% vs Kalshi 74% · logloss 0.5148 vs 0.5152 | 3463 windows · right 74% vs Kalshi 74% · logloss 0.5104 vs 0.5102 | — |
| SILVER | 400 windows · right 75% vs Kalshi 75% · logloss 0.5034 vs 0.503 | 3445 windows · right 74% vs Kalshi 74% · logloss 0.5114 vs 0.5124 | — |
| WTI | 445 windows · right 73% vs Kalshi 74% · logloss 0.5224 vs 0.5211 | 3612 windows · right 75% vs Kalshi 75% · logloss 0.5057 vs 0.5058 | — |
| BRENT | 445 windows · right 74% vs Kalshi 74% · logloss 0.5071 vs 0.506 | 479 windows · right 76% vs Kalshi 76% · logloss 0.4902 vs 0.4892 | — |
| COPPER | 402 windows · right 77% vs Kalshi 77% · logloss 0.4923 vs 0.4928 | 2728 windows · right 76% vs Kalshi 75% · logloss 0.4995 vs 0.5001 | — |
| NATGAS | 444 windows · right 75% vs Kalshi 75% · logloss 0.5043 vs 0.5061 | 2898 windows · right 75% vs Kalshi 75% · logloss 0.4973 vs 0.4972 | — |
| PALLADIUM | 401 windows · right 75% vs Kalshi 75% · logloss 0.5111 vs 0.5099 | 1507 windows · right 75% vs Kalshi 74% · logloss 0.5098 vs 0.5117 | — |
| PLATINUM | 402 windows · right 73% vs Kalshi 73% · logloss 0.5252 vs 0.5238 | 1862 windows · right 75% vs Kalshi 75% · logloss 0.5011 vs 0.5027 | — |

**All weeks:** 3340 windows · right 74% vs Kalshi 74% · logloss 0.5101 vs 0.5098

**All months:** 19994 windows · right 75% vs Kalshi 75% · logloss 0.5049 vs 0.5054

| Month | Result |
|---|---|
| 2026-08 | 2780 windows · right 75% vs Kalshi 75% · logloss 0.5015 vs 0.5021 |
| 2026-09 | 6734 windows · right 75% vs Kalshi 74% · logloss 0.5081 vs 0.5083 |
| 2026-10 | 10480 windows · right 75% vs Kalshi 75% · logloss 0.5037 vs 0.5044 |

Strongest signals: `s_ASIA` -0.047, `s_EU` +0.037, `ofi3` +0.029, `dmid5` +0.025, `m_GOLD` -0.021

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,678, target reached normally 22% | setups 14,253, target reached normally 20% | — |
| SILVER | setups 1,673, target reached normally 20% | setups 14,266, target reached normally 21% | — |
| WTI | setups 1,821, target reached normally 21% | setups 15,073, target reached normally 20% | — |
| BRENT | setups 2,099, target reached normally 20% | setups 2,020, target reached normally 11% | — |
| COPPER | setups 2,078, target reached normally 17% | setups 12,098, target reached normally 16% | — |
| NATGAS | setups 1,680, target reached normally 16% | setups 12,942, target reached normally 16% | — |
| PALLADIUM | setups 1,882, target reached normally 16% | setups 5,779, target reached normally 14% | — |
| PLATINUM | setups 1,912, target reached normally 21% | setups 7,444, target reached normally 14% | — |

**All weeks:** setups 14,823, target reached normally 19%

**All months:** setups 83,875, target reached normally 18%
