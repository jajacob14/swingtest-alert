# Kalshi commodity 15-min model report
Trained 2026-11-24 22:12 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 26609

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 401 windows · right 75% vs Kalshi 75% · logloss 0.4985 vs 0.4977 | 3607 windows · right 74% vs Kalshi 74% · logloss 0.5057 vs 0.5053 | — |
| SILVER | 401 windows · right 76% vs Kalshi 76% · logloss 0.4846 vs 0.482 | 3591 windows · right 74% vs Kalshi 74% · logloss 0.5062 vs 0.5068 | — |
| WTI | 450 windows · right 75% vs Kalshi 75% · logloss 0.5028 vs 0.5035 | 3805 windows · right 75% vs Kalshi 75% · logloss 0.5076 vs 0.5078 | — |
| BRENT | 449 windows · right 76% vs Kalshi 76% · logloss 0.4799 vs 0.4798 · edge bets 6: won 33%, ROI -38% | 919 windows · right 75% vs Kalshi 75% · logloss 0.5032 vs 0.503 | — |
| COPPER | 401 windows · right 72% vs Kalshi 72% · logloss 0.5307 vs 0.5298 | 3119 windows · right 76% vs Kalshi 75% · logloss 0.4968 vs 0.4971 | — |
| NATGAS | 450 windows · right 76% vs Kalshi 75% · logloss 0.4935 vs 0.4961 · edge bets 2: won 50%, ROI -6% | 3338 windows · right 75% vs Kalshi 75% · logloss 0.499 vs 0.4981 · edge bets 10: won 30%, ROI -42% | — |
| PALLADIUM | 399 windows · right 72% vs Kalshi 72% · logloss 0.5342 vs 0.5328 | 1898 windows · right 75% vs Kalshi 75% · logloss 0.5076 vs 0.5085 | — |
| PLATINUM | 400 windows · right 75% vs Kalshi 75% · logloss 0.5134 vs 0.5129 | 2253 windows · right 75% vs Kalshi 75% · logloss 0.5035 vs 0.5043 | — |

**All weeks:** 3351 windows · right 75% vs Kalshi 75% · logloss 0.5041 vs 0.5038 · edge bets 8: won 38%, ROI -30%

**All months:** 22530 windows · right 75% vs Kalshi 75% · logloss 0.5037 vs 0.5038 · edge bets 10: won 30%, ROI -42%

| Month | Result |
|---|---|
| 2026-08 | 2041 windows · right 76% vs Kalshi 76% · logloss 0.4906 vs 0.4906 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5082 vs 0.5083 · edge bets 3: won 0%, ROI -100% |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.5053 vs 0.5055 · edge bets 7: won 43%, ROI -16% |
| 2026-11 | 1609 windows · right 76% vs Kalshi 76% · logloss 0.4884 vs 0.4892 |

Strongest signals: `s_ASIA` -0.037, `m_NATGAS` +0.028, `s_EU` +0.024, `tleft` -0.023, `dmid5` +0.021

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,674, target reached normally 21% | setups 14,683, target reached normally 20% | — |
| SILVER | setups 1,749, target reached normally 22% | setups 14,746, target reached normally 21% | — |
| WTI | setups 1,814, target reached normally 21% | setups 15,706, target reached normally 21% | — |
| BRENT | setups 2,118, target reached normally 17% | setups 3,925, target reached normally 14% | — |
| COPPER | setups 1,937, target reached normally 21% | setups 13,983, target reached normally 16% | — |
| NATGAS | setups 1,881, target reached normally 16% | setups 14,941, target reached normally 16% | — |
| PALLADIUM | setups 1,673, target reached normally 18% | setups 7,574, target reached normally 14% | — |
| PLATINUM | setups 1,970, target reached normally 19% | setups 9,179, target reached normally 15% | — |

**All weeks:** setups 14,816, target reached normally 19%

**All months:** setups 94,737, target reached normally 18%
