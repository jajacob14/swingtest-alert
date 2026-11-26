# Kalshi commodity 15-min model report
Trained 2026-11-26 07:39 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 29018

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 402 windows · right 76% vs Kalshi 76% · logloss 0.4913 vs 0.4905 | 3654 windows · right 74% vs Kalshi 74% · logloss 0.5053 vs 0.5049 | — |
| SILVER | 403 windows · right 77% vs Kalshi 78% · logloss 0.4777 vs 0.4769 | 3638 windows · right 74% vs Kalshi 74% · logloss 0.5091 vs 0.5098 | — |
| WTI | 446 windows · right 74% vs Kalshi 74% · logloss 0.5146 vs 0.5134 | 3857 windows · right 74% vs Kalshi 74% · logloss 0.5087 vs 0.509 | — |
| BRENT | 446 windows · right 75% vs Kalshi 75% · logloss 0.4919 vs 0.4902 · edge bets 4: won 50%, ROI -16% | 1045 windows · right 75% vs Kalshi 75% · logloss 0.5028 vs 0.5026 | — |
| COPPER | 402 windows · right 73% vs Kalshi 73% · logloss 0.5249 vs 0.5232 | 3240 windows · right 76% vs Kalshi 76% · logloss 0.4958 vs 0.4961 | — |
| NATGAS | 446 windows · right 76% vs Kalshi 76% · logloss 0.4867 vs 0.4889 | 3464 windows · right 75% vs Kalshi 75% · logloss 0.4991 vs 0.4986 | — |
| PALLADIUM | 403 windows · right 74% vs Kalshi 73% · logloss 0.532 vs 0.5317 | 2019 windows · right 75% vs Kalshi 75% · logloss 0.506 vs 0.5064 | — |
| PLATINUM | 403 windows · right 74% vs Kalshi 74% · logloss 0.5176 vs 0.5165 | 2374 windows · right 75% vs Kalshi 74% · logloss 0.5071 vs 0.5079 | — |

**All weeks:** 3351 windows · right 75% vs Kalshi 75% · logloss 0.5043 vs 0.5037 · edge bets 4: won 50%, ROI -16%

**All months:** 23291 windows · right 75% vs Kalshi 75% · logloss 0.5043 vs 0.5045

| Month | Result |
|---|---|
| 2026-08 | 1819 windows · right 75% vs Kalshi 75% · logloss 0.4945 vs 0.4942 |
| 2026-09 | 6734 windows · right 75% vs Kalshi 74% · logloss 0.5082 vs 0.5083 |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.5052 vs 0.5055 |
| 2026-11 | 2592 windows · right 75% vs Kalshi 75% · logloss 0.4966 vs 0.4969 |

Strongest signals: `s_ASIA` -0.037, `m_NATGAS` +0.026, `s_US` +0.025, `tleft` -0.023, `m_PALLADIUM` -0.021

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,723, target reached normally 20% | setups 14,812, target reached normally 20% | — |
| SILVER | setups 1,767, target reached normally 22% | setups 14,831, target reached normally 21% | — |
| WTI | setups 1,819, target reached normally 23% | setups 15,877, target reached normally 21% | — |
| BRENT | setups 2,127, target reached normally 18% | setups 4,520, target reached normally 15% | — |
| COPPER | setups 1,923, target reached normally 20% | setups 14,640, target reached normally 15% | — |
| NATGAS | setups 1,906, target reached normally 16% | setups 15,477, target reached normally 16% | — |
| PALLADIUM | setups 1,752, target reached normally 21% | setups 8,160, target reached normally 14% | — |
| PLATINUM | setups 1,948, target reached normally 19% | setups 9,723, target reached normally 15% | — |

**All weeks:** setups 14,965, target reached normally 20%

**All months:** setups 98,040, target reached normally 18%
