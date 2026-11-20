# Kalshi commodity 15-min model report
Trained 2026-11-20 09:07 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 21959

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 410 windows · right 75% vs Kalshi 75% · logloss 0.4965 vs 0.4969 | 3526 windows · right 74% vs Kalshi 74% · logloss 0.509 vs 0.5087 | — |
| SILVER | 410 windows · right 75% vs Kalshi 75% · logloss 0.4948 vs 0.4947 | 3510 windows · right 74% vs Kalshi 74% · logloss 0.5078 vs 0.5087 | — |
| WTI | 431 windows · right 75% vs Kalshi 75% · logloss 0.4891 vs 0.4913 | 3685 windows · right 75% vs Kalshi 75% · logloss 0.5059 vs 0.5061 | — |
| BRENT | 430 windows · right 76% vs Kalshi 76% · logloss 0.4807 vs 0.4819 | 655 windows · right 75% vs Kalshi 75% · logloss 0.4996 vs 0.4995 | — |
| COPPER | 410 windows · right 75% vs Kalshi 75% · logloss 0.5107 vs 0.5108 | 2894 windows · right 76% vs Kalshi 75% · logloss 0.4982 vs 0.4988 | — |
| NATGAS | 430 windows · right 75% vs Kalshi 75% · logloss 0.4933 vs 0.495 | 3074 windows · right 75% vs Kalshi 75% · logloss 0.4982 vs 0.498 · edge bets 1: won 0%, ROI -100% | — |
| PALLADIUM | 411 windows · right 74% vs Kalshi 74% · logloss 0.5096 vs 0.509 | 1673 windows · right 75% vs Kalshi 75% · logloss 0.5059 vs 0.5075 | — |
| PLATINUM | 410 windows · right 74% vs Kalshi 74% · logloss 0.5065 vs 0.5063 | 2028 windows · right 75% vs Kalshi 75% · logloss 0.5037 vs 0.5048 | — |

**All weeks:** 3342 windows · right 75% vs Kalshi 75% · logloss 0.4973 vs 0.4979

**All months:** 21045 windows · right 75% vs Kalshi 75% · logloss 0.5041 vs 0.5045 · edge bets 1: won 0%, ROI -100%

| Month | Result |
|---|---|
| 2026-08 | 2473 windows · right 75% vs Kalshi 75% · logloss 0.4949 vs 0.4954 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5082 vs 0.5083 |
| 2026-10 | 11838 windows · right 75% vs Kalshi 75% · logloss 0.5037 vs 0.5043 · edge bets 1: won 0%, ROI -100% |

Strongest signals: `s_ASIA` -0.039, `s_EU` +0.029, `ofi3` +0.026, `tleft` -0.024, `dmid5` +0.024

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,689, target reached normally 20% | setups 14,440, target reached normally 20% | — |
| SILVER | setups 1,706, target reached normally 21% | setups 14,425, target reached normally 21% | — |
| WTI | setups 1,743, target reached normally 21% | setups 15,379, target reached normally 20% | — |
| BRENT | setups 2,076, target reached normally 19% | setups 2,777, target reached normally 13% | — |
| COPPER | setups 2,088, target reached normally 19% | setups 12,948, target reached normally 16% | — |
| NATGAS | setups 1,669, target reached normally 16% | setups 13,857, target reached normally 16% | — |
| PALLADIUM | setups 1,836, target reached normally 16% | setups 6,539, target reached normally 14% | — |
| PLATINUM | setups 2,004, target reached normally 19% | setups 8,189, target reached normally 15% | — |

**All weeks:** setups 14,811, target reached normally 19%

**All months:** setups 88,554, target reached normally 18%
