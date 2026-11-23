# Kalshi commodity 15-min model report
Trained 2026-11-23 16:19 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 24458

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 403 windows · right 75% vs Kalshi 75% · logloss 0.4961 vs 0.4976 | 3508 windows · right 74% vs Kalshi 74% · logloss 0.5053 vs 0.5048 | — |
| SILVER | 402 windows · right 76% vs Kalshi 76% · logloss 0.4944 vs 0.4931 · edge bets 1: won 0%, ROI -100% | 3493 windows · right 74% vs Kalshi 74% · logloss 0.5057 vs 0.5065 | — |
| WTI | 447 windows · right 75% vs Kalshi 75% · logloss 0.4998 vs 0.5029 | 3696 windows · right 74% vs Kalshi 74% · logloss 0.5081 vs 0.5082 | — |
| BRENT | 446 windows · right 77% vs Kalshi 76% · logloss 0.4714 vs 0.4728 · edge bets 7: won 43%, ROI -25% | 800 windows · right 74% vs Kalshi 74% · logloss 0.5091 vs 0.5086 · edge bets 5: won 60%, ROI +10% | — |
| COPPER | 402 windows · right 72% vs Kalshi 72% · logloss 0.5361 vs 0.5352 | 3010 windows · right 76% vs Kalshi 76% · logloss 0.4971 vs 0.4973 | — |
| NATGAS | 446 windows · right 76% vs Kalshi 76% · logloss 0.4921 vs 0.4935 · edge bets 4: won 25%, ROI -54% | 3219 windows · right 75% vs Kalshi 75% · logloss 0.4988 vs 0.4979 · edge bets 139: won 50%, ROI -10% | — |
| PALLADIUM | 403 windows · right 73% vs Kalshi 73% · logloss 0.5203 vs 0.5202 | 1789 windows · right 75% vs Kalshi 75% · logloss 0.5066 vs 0.5078 | — |
| PLATINUM | 402 windows · right 75% vs Kalshi 75% · logloss 0.5049 vs 0.5047 | 2144 windows · right 75% vs Kalshi 75% · logloss 0.5051 vs 0.5059 | — |

**All weeks:** 3351 windows · right 75% vs Kalshi 75% · logloss 0.5012 vs 0.5019 · edge bets 12: won 33%, ROI -40%

**All months:** 21659 windows · right 75% vs Kalshi 75% · logloss 0.5039 vs 0.504 · edge bets 144: won 50%, ROI -9%

| Month | Result |
|---|---|
| 2026-08 | 2072 windows · right 76% vs Kalshi 76% · logloss 0.4878 vs 0.488 · edge bets 1: won 0%, ROI -100% |
| 2026-09 | 6734 windows · right 75% vs Kalshi 74% · logloss 0.5083 vs 0.5083 · edge bets 34: won 50%, ROI -10% |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.5051 vs 0.5055 · edge bets 106: won 51%, ROI -7% |
| 2026-11 | 707 windows · right 76% vs Kalshi 75% · logloss 0.4887 vs 0.4855 · edge bets 3: won 33%, ROI -36% |

Strongest signals: `s_ASIA` -0.038, `s_EU` +0.028, `ofi3` +0.026, `tleft` -0.025, `m_NATGAS` +0.023

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,670, target reached normally 19% | setups 14,289, target reached normally 19% | — |
| SILVER | setups 1,755, target reached normally 22% | setups 14,339, target reached normally 21% | — |
| WTI | setups 1,827, target reached normally 22% | setups 15,268, target reached normally 21% | — |
| BRENT | setups 2,124, target reached normally 18% | setups 3,387, target reached normally 14% | — |
| COPPER | setups 1,997, target reached normally 21% | setups 13,495, target reached normally 15% | — |
| NATGAS | setups 1,805, target reached normally 16% | setups 14,394, target reached normally 16% | — |
| PALLADIUM | setups 1,690, target reached normally 16% | setups 7,059, target reached normally 14% | — |
| PLATINUM | setups 2,030, target reached normally 20% | setups 8,658, target reached normally 15% | — |

**All weeks:** setups 14,898, target reached normally 19%

**All months:** setups 90,889, target reached normally 18%
