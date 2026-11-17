# Kalshi commodity 15-min model report
Trained 2026-11-17 12:01 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 16937

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 401 windows · right 74% vs Kalshi 74% · logloss 0.5221 vs 0.5219 | 3402 windows · right 74% vs Kalshi 74% · logloss 0.5114 vs 0.5114 | — |
| SILVER | 401 windows · right 74% vs Kalshi 74% · logloss 0.5132 vs 0.5108 | 3385 windows · right 74% vs Kalshi 74% · logloss 0.5121 vs 0.513 | — |
| WTI | 444 windows · right 75% vs Kalshi 75% · logloss 0.5091 vs 0.5062 | 3546 windows · right 75% vs Kalshi 75% · logloss 0.5041 vs 0.5045 | — |
| BRENT | 445 windows · right 74% vs Kalshi 75% · logloss 0.5072 vs 0.5052 | 387 windows · right 76% vs Kalshi 76% · logloss 0.4842 vs 0.4851 | — |
| COPPER | 401 windows · right 75% vs Kalshi 76% · logloss 0.4953 vs 0.4958 | 2641 windows · right 75% vs Kalshi 75% · logloss 0.5004 vs 0.5011 | — |
| NATGAS | 445 windows · right 75% vs Kalshi 75% · logloss 0.5117 vs 0.5131 | 2806 windows · right 75% vs Kalshi 75% · logloss 0.4962 vs 0.4966 | — |
| PALLADIUM | 401 windows · right 75% vs Kalshi 75% · logloss 0.5113 vs 0.5092 | 1420 windows · right 75% vs Kalshi 75% · logloss 0.508 vs 0.5101 | — |
| PLATINUM | 401 windows · right 74% vs Kalshi 74% · logloss 0.5266 vs 0.5231 | 1775 windows · right 75% vs Kalshi 75% · logloss 0.5016 vs 0.5029 | — |

**All weeks:** 3339 windows · right 74% vs Kalshi 75% · logloss 0.5119 vs 0.5105

**All months:** 19362 windows · right 75% vs Kalshi 75% · logloss 0.5048 vs 0.5054

| Month | Result |
|---|---|
| 2026-08 | 2859 windows · right 75% vs Kalshi 75% · logloss 0.5014 vs 0.5019 |
| 2026-09 | 6734 windows · right 75% vs Kalshi 74% · logloss 0.5081 vs 0.5083 |
| 2026-10 | 9769 windows · right 75% vs Kalshi 75% · logloss 0.5034 vs 0.5044 |

Strongest signals: `s_ASIA` -0.042, `s_EU` +0.030, `ofi3` +0.029, `dmid5` +0.025, `m_BRENT` +0.020

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,684, target reached normally 24% | setups 14,025, target reached normally 20% | — |
| SILVER | setups 1,683, target reached normally 20% | setups 14,008, target reached normally 21% | — |
| WTI | setups 1,841, target reached normally 20% | setups 14,879, target reached normally 20% | — |
| BRENT | setups 2,121, target reached normally 19% | setups 1,618, target reached normally 11% | — |
| COPPER | setups 2,016, target reached normally 17% | setups 11,719, target reached normally 16% | — |
| NATGAS | setups 1,719, target reached normally 16% | setups 12,494, target reached normally 16% | — |
| PALLADIUM | setups 1,987, target reached normally 17% | setups 5,456, target reached normally 14% | — |
| PLATINUM | setups 1,878, target reached normally 20% | setups 7,137, target reached normally 15% | — |

**All weeks:** setups 14,929, target reached normally 19%

**All months:** setups 81,336, target reached normally 18%
