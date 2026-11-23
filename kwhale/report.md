# Kalshi commodity 15-min model report
Trained 2026-11-23 09:56 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 24057

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 403 windows · right 75% vs Kalshi 75% · logloss 0.4982 vs 0.4995 | 3482 windows · right 74% vs Kalshi 74% · logloss 0.5049 vs 0.5045 | — |
| SILVER | 402 windows · right 75% vs Kalshi 76% · logloss 0.4953 vs 0.4934 · edge bets 3: won 33%, ROI -36% | 3467 windows · right 74% vs Kalshi 74% · logloss 0.5063 vs 0.5071 | — |
| WTI | 447 windows · right 75% vs Kalshi 75% · logloss 0.4934 vs 0.4967 | 3670 windows · right 74% vs Kalshi 74% · logloss 0.5084 vs 0.5085 | — |
| BRENT | 447 windows · right 76% vs Kalshi 76% · logloss 0.4769 vs 0.4782 · edge bets 6: won 33%, ROI -43% | 774 windows · right 74% vs Kalshi 74% · logloss 0.5119 vs 0.5115 · edge bets 4: won 50%, ROI -6% | — |
| COPPER | 402 windows · right 73% vs Kalshi 73% · logloss 0.5324 vs 0.5321 | 2984 windows · right 76% vs Kalshi 76% · logloss 0.4967 vs 0.4969 | — |
| NATGAS | 447 windows · right 74% vs Kalshi 74% · logloss 0.5068 vs 0.5081 · edge bets 2: won 50%, ROI -3% | 3193 windows · right 75% vs Kalshi 75% · logloss 0.4993 vs 0.4987 · edge bets 87: won 44%, ROI -20% | — |
| PALLADIUM | 401 windows · right 73% vs Kalshi 74% · logloss 0.5173 vs 0.5175 | 1763 windows · right 75% vs Kalshi 75% · logloss 0.5071 vs 0.5085 | — |
| PLATINUM | 402 windows · right 74% vs Kalshi 74% · logloss 0.5116 vs 0.5117 | 2118 windows · right 75% vs Kalshi 75% · logloss 0.505 vs 0.5059 | — |

**All weeks:** 3351 windows · right 74% vs Kalshi 74% · logloss 0.5034 vs 0.5041 · edge bets 11: won 36%, ROI -34%

**All months:** 21451 windows · right 75% vs Kalshi 75% · logloss 0.5042 vs 0.5044 · edge bets 91: won 44%, ROI -19%

| Month | Result |
|---|---|
| 2026-08 | 2072 windows · right 76% vs Kalshi 76% · logloss 0.4878 vs 0.488 · edge bets 1: won 0%, ROI -100% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5083 vs 0.5083 · edge bets 23: won 44%, ROI -22% |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.5051 vs 0.5055 · edge bets 65: won 46%, ROI -15% |
| 2026-11 | 499 windows · right 75% vs Kalshi 74% · logloss 0.4961 vs 0.4925 · edge bets 2: won 0%, ROI -100% |

Strongest signals: `s_ASIA` -0.037, `s_EU` +0.029, `tleft` -0.023, `m_BRENT` +0.023, `ofi3` +0.023

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,681, target reached normally 20% | setups 14,204, target reached normally 19% | — |
| SILVER | setups 1,763, target reached normally 23% | setups 14,228, target reached normally 21% | — |
| WTI | setups 1,863, target reached normally 22% | setups 15,170, target reached normally 20% | — |
| BRENT | setups 2,156, target reached normally 19% | setups 3,246, target reached normally 14% | — |
| COPPER | setups 2,025, target reached normally 20% | setups 13,378, target reached normally 15% | — |
| NATGAS | setups 1,752, target reached normally 16% | setups 14,269, target reached normally 16% | — |
| PALLADIUM | setups 1,710, target reached normally 17% | setups 6,955, target reached normally 14% | — |
| PLATINUM | setups 2,028, target reached normally 21% | setups 8,567, target reached normally 15% | — |

**All weeks:** setups 14,978, target reached normally 20%

**All months:** setups 90,017, target reached normally 18%
