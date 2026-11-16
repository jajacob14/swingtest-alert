# Kalshi commodity 15-min model report
Trained 2026-11-16 01:26 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 14416

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 400 windows · right 73% vs Kalshi 73% · logloss 0.531 vs 0.5274 · edge bets 1: won 0%, ROI -100% | 3268 windows · right 74% vs Kalshi 74% · logloss 0.508 vs 0.5084 | — |
| SILVER | 399 windows · right 75% vs Kalshi 75% · logloss 0.5045 vs 0.5019 | 3251 windows · right 74% vs Kalshi 74% · logloss 0.5107 vs 0.5115 | — |
| WTI | 448 windows · right 74% vs Kalshi 74% · logloss 0.5141 vs 0.5118 · edge bets 4: won 25%, ROI -59% | 3407 windows · right 75% vs Kalshi 75% · logloss 0.5027 vs 0.5033 | — |
| BRENT | 449 windows · right 74% vs Kalshi 74% · logloss 0.5111 vs 0.5091 | 248 windows · right 77% vs Kalshi 77% · logloss 0.4726 vs 0.4754 | — |
| COPPER | 399 windows · right 75% vs Kalshi 76% · logloss 0.4903 vs 0.4901 | 2507 windows · right 75% vs Kalshi 75% · logloss 0.5006 vs 0.5012 | — |
| NATGAS | 449 windows · right 74% vs Kalshi 74% · logloss 0.5241 vs 0.5223 | 2667 windows · right 75% vs Kalshi 75% · logloss 0.4974 vs 0.4979 | — |
| PALLADIUM | 399 windows · right 75% vs Kalshi 75% · logloss 0.5104 vs 0.5081 · edge bets 4: won 25%, ROI -61% | 1286 windows · right 75% vs Kalshi 74% · logloss 0.5098 vs 0.512 | — |
| PLATINUM | 399 windows · right 73% vs Kalshi 73% · logloss 0.5426 vs 0.5396 · edge bets 2: won 50%, ROI -14% | 1641 windows · right 75% vs Kalshi 75% · logloss 0.5019 vs 0.5033 | — |

**All weeks:** 3342 windows · right 74% vs Kalshi 74% · logloss 0.5159 vs 0.5137 · edge bets 11: won 27%, ROI -55%

**All months:** 18275 windows · right 75% vs Kalshi 75% · logloss 0.504 vs 0.5048

| Month | Result |
|---|---|
| 2026-08 | 2859 windows · right 75% vs Kalshi 75% · logloss 0.5013 vs 0.5019 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5079 vs 0.5083 |
| 2026-10 | 8682 windows · right 75% vs Kalshi 75% · logloss 0.5017 vs 0.503 |

Strongest signals: `s_ASIA` -0.041, `dmid5` +0.032, `ofi3` +0.027, `m_BRENT` +0.025, `s_EU` +0.023

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,739, target reached normally 25% | setups 13,532, target reached normally 19% | — |
| SILVER | setups 1,686, target reached normally 20% | setups 13,538, target reached normally 21% | — |
| WTI | setups 1,786, target reached normally 19% | setups 14,272, target reached normally 20% | — |
| BRENT | setups 2,084, target reached normally 18% | setups 972, target reached normally 11% | — |
| COPPER | setups 2,029, target reached normally 15% | setups 11,151, target reached normally 16% | — |
| NATGAS | setups 1,873, target reached normally 16% | setups 11,753, target reached normally 16% | — |
| PALLADIUM | setups 1,926, target reached normally 17% | setups 4,896, target reached normally 14% | — |
| PLATINUM | setups 1,831, target reached normally 20% | setups 6,626, target reached normally 15% | — |

**All weeks:** setups 14,954, target reached normally 19%

**All months:** setups 76,740, target reached normally 18%
