# Kalshi commodity 15-min model report
Trained 2026-11-19 10:04 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 20221

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 401 windows · right 75% vs Kalshi 75% · logloss 0.4948 vs 0.4948 | 3490 windows · right 74% vs Kalshi 74% · logloss 0.51 vs 0.5098 | — |
| SILVER | 401 windows · right 75% vs Kalshi 75% · logloss 0.4914 vs 0.491 | 3474 windows · right 74% vs Kalshi 74% · logloss 0.508 vs 0.5091 | — |
| WTI | 445 windows · right 74% vs Kalshi 74% · logloss 0.5054 vs 0.5055 | 3645 windows · right 75% vs Kalshi 75% · logloss 0.5055 vs 0.5056 | — |
| BRENT | 444 windows · right 75% vs Kalshi 74% · logloss 0.4953 vs 0.4961 | 563 windows · right 75% vs Kalshi 76% · logloss 0.4944 vs 0.493 | — |
| COPPER | 402 windows · right 76% vs Kalshi 76% · logloss 0.5006 vs 0.5015 | 2807 windows · right 76% vs Kalshi 75% · logloss 0.4994 vs 0.4999 | — |
| NATGAS | 445 windows · right 75% vs Kalshi 75% · logloss 0.4996 vs 0.502 | 2982 windows · right 75% vs Kalshi 75% · logloss 0.4982 vs 0.4978 · edge bets 5: won 20%, ROI -63% | — |
| PALLADIUM | 401 windows · right 75% vs Kalshi 74% · logloss 0.503 vs 0.5031 | 1586 windows · right 75% vs Kalshi 75% · logloss 0.5048 vs 0.5068 | — |
| PLATINUM | 402 windows · right 75% vs Kalshi 75% · logloss 0.4964 vs 0.4962 | 1941 windows · right 75% vs Kalshi 75% · logloss 0.4999 vs 0.5013 | — |

**All weeks:** 3341 windows · right 75% vs Kalshi 75% · logloss 0.4984 vs 0.4989

**All months:** 20488 windows · right 75% vs Kalshi 75% · logloss 0.5039 vs 0.5043 · edge bets 5: won 20%, ROI -63%

| Month | Result |
|---|---|
| 2026-08 | 2627 windows · right 75% vs Kalshi 75% · logloss 0.4986 vs 0.4992 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5081 vs 0.5083 · edge bets 1: won 0%, ROI -100% |
| 2026-10 | 11127 windows · right 75% vs Kalshi 75% · logloss 0.5026 vs 0.5031 · edge bets 4: won 25%, ROI -52% |

Strongest signals: `s_ASIA` -0.043, `s_EU` +0.035, `ofi3` +0.031, `dmid5` +0.025, `tleft` -0.022

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,703, target reached normally 21% | setups 14,299, target reached normally 20% | — |
| SILVER | setups 1,713, target reached normally 19% | setups 14,302, target reached normally 21% | — |
| WTI | setups 1,764, target reached normally 20% | setups 15,244, target reached normally 20% | — |
| BRENT | setups 2,040, target reached normally 20% | setups 2,394, target reached normally 12% | — |
| COPPER | setups 2,065, target reached normally 18% | setups 12,490, target reached normally 16% | — |
| NATGAS | setups 1,680, target reached normally 15% | setups 13,383, target reached normally 16% | — |
| PALLADIUM | setups 1,873, target reached normally 15% | setups 6,165, target reached normally 14% | — |
| PLATINUM | setups 1,963, target reached normally 19% | setups 7,774, target reached normally 15% | — |

**All weeks:** setups 14,801, target reached normally 18%

**All months:** setups 86,051, target reached normally 18%
