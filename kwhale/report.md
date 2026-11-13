# Kalshi commodity 15-min model report
Trained 2026-11-13 04:22 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 12677

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 400 windows · right 75% vs Kalshi 75% · logloss 0.5038 vs 0.503 · edge bets 2: won 50%, ROI -14% | 3270 windows · right 74% vs Kalshi 74% · logloss 0.5055 vs 0.5061 | — |
| SILVER | 399 windows · right 75% vs Kalshi 75% · logloss 0.5058 vs 0.5048 | 3261 windows · right 74% vs Kalshi 74% · logloss 0.5077 vs 0.5087 | — |
| WTI | 448 windows · right 76% vs Kalshi 76% · logloss 0.4868 vs 0.484 · edge bets 5: won 0%, ROI -100% | 3392 windows · right 75% vs Kalshi 75% · logloss 0.5006 vs 0.5012 | — |
| BRENT | 448 windows · right 76% vs Kalshi 76% · logloss 0.4818 vs 0.4803 | 140 windows · right 79% vs Kalshi 78% · logloss 0.4543 vs 0.4551 | — |
| COPPER | 400 windows · right 76% vs Kalshi 77% · logloss 0.4792 vs 0.4795 | 2428 windows · right 75% vs Kalshi 75% · logloss 0.5022 vs 0.503 | — |
| NATGAS | 447 windows · right 74% vs Kalshi 74% · logloss 0.5255 vs 0.5262 | 2559 windows · right 75% vs Kalshi 75% · logloss 0.496 vs 0.4965 | — |
| PALLADIUM | 400 windows · right 76% vs Kalshi 76% · logloss 0.5018 vs 0.5001 · edge bets 4: won 25%, ROI -60% | 1207 windows · right 74% vs Kalshi 74% · logloss 0.5123 vs 0.5147 | — |
| PLATINUM | 399 windows · right 74% vs Kalshi 74% · logloss 0.5226 vs 0.5208 · edge bets 1: won 100%, ROI +72% | 1562 windows · right 75% vs Kalshi 75% · logloss 0.5008 vs 0.5024 | — |

**All weeks:** 3341 windows · right 75% vs Kalshi 75% · logloss 0.5008 vs 0.4997 · edge bets 12: won 25%, ROI -58%

**All months:** 17819 windows · right 75% vs Kalshi 75% · logloss 0.5028 vs 0.5037

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4978 vs 0.4983 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5079 vs 0.5083 |
| 2026-10 | 7963 windows · right 75% vs Kalshi 75% · logloss 0.5003 vs 0.5018 |

Strongest signals: `s_ASIA` -0.049, `dmid5` +0.030, `s_EU` +0.027, `s_US` +0.026, `ofi3` +0.025

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,714, target reached normally 23% | setups 13,625, target reached normally 19% | — |
| SILVER | setups 1,652, target reached normally 24% | setups 13,768, target reached normally 20% | — |
| WTI | setups 1,849, target reached normally 17% | setups 14,149, target reached normally 20% | — |
| BRENT | setups 2,165, target reached normally 16% | setups 570, target reached normally 14% | — |
| COPPER | setups 2,027, target reached normally 15% | setups 10,826, target reached normally 16% | — |
| NATGAS | setups 1,915, target reached normally 17% | setups 11,337, target reached normally 15% | — |
| PALLADIUM | setups 1,852, target reached normally 17% | setups 4,551, target reached normally 14% | — |
| PLATINUM | setups 1,785, target reached normally 20% | setups 6,368, target reached normally 14% | — |

**All weeks:** setups 14,959, target reached normally 19%

**All months:** setups 75,194, target reached normally 18%
