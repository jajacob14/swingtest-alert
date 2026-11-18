# Kalshi commodity 15-min model report
Trained 2026-11-17 23:32 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 17764

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 399 windows · right 73% vs Kalshi 73% · logloss 0.5312 vs 0.5313 | 3442 windows · right 74% vs Kalshi 74% · logloss 0.51 vs 0.5102 | — |
| SILVER | 400 windows · right 74% vs Kalshi 74% · logloss 0.5181 vs 0.5157 | 3424 windows · right 74% vs Kalshi 74% · logloss 0.5115 vs 0.5126 | — |
| WTI | 447 windows · right 74% vs Kalshi 74% · logloss 0.5166 vs 0.5152 | 3591 windows · right 75% vs Kalshi 75% · logloss 0.5045 vs 0.5047 | — |
| BRENT | 448 windows · right 74% vs Kalshi 75% · logloss 0.5014 vs 0.4998 | 433 windows · right 76% vs Kalshi 77% · logloss 0.4825 vs 0.4827 | — |
| COPPER | 399 windows · right 77% vs Kalshi 77% · logloss 0.4827 vs 0.4839 | 2682 windows · right 75% vs Kalshi 75% · logloss 0.4999 vs 0.5006 | — |
| NATGAS | 448 windows · right 75% vs Kalshi 75% · logloss 0.5058 vs 0.5079 | 2852 windows · right 75% vs Kalshi 75% · logloss 0.4972 vs 0.4974 | — |
| PALLADIUM | 400 windows · right 74% vs Kalshi 73% · logloss 0.5276 vs 0.5254 | 1461 windows · right 75% vs Kalshi 75% · logloss 0.5061 vs 0.5083 | — |
| PLATINUM | 399 windows · right 73% vs Kalshi 73% · logloss 0.5313 vs 0.5285 | 1816 windows · right 75% vs Kalshi 75% · logloss 0.5013 vs 0.5027 | — |

**All weeks:** 3340 windows · right 74% vs Kalshi 74% · logloss 0.5139 vs 0.5131

**All months:** 19701 windows · right 75% vs Kalshi 75% · logloss 0.5043 vs 0.505

| Month | Result |
|---|---|
| 2026-08 | 2855 windows · right 75% vs Kalshi 75% · logloss 0.5008 vs 0.5015 |
| 2026-09 | 6734 windows · right 75% vs Kalshi 74% · logloss 0.508 vs 0.5083 |
| 2026-10 | 10112 windows · right 75% vs Kalshi 75% · logloss 0.5028 vs 0.5037 |

Strongest signals: `s_ASIA` -0.046, `s_EU` +0.033, `ofi3` +0.029, `dmid5` +0.027, `tleft` -0.019

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,675, target reached normally 24% | setups 14,206, target reached normally 20% | — |
| SILVER | setups 1,658, target reached normally 21% | setups 14,190, target reached normally 21% | — |
| WTI | setups 1,825, target reached normally 20% | setups 15,047, target reached normally 20% | — |
| BRENT | setups 2,130, target reached normally 20% | setups 1,813, target reached normally 10% | — |
| COPPER | setups 2,011, target reached normally 16% | setups 11,868, target reached normally 16% | — |
| NATGAS | setups 1,669, target reached normally 16% | setups 12,686, target reached normally 16% | — |
| PALLADIUM | setups 1,911, target reached normally 17% | setups 5,606, target reached normally 14% | — |
| PLATINUM | setups 1,879, target reached normally 21% | setups 7,281, target reached normally 14% | — |

**All weeks:** setups 14,758, target reached normally 19%

**All months:** setups 82,697, target reached normally 18%
