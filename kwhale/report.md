# Kalshi commodity 15-min model report
Trained 2026-11-26 19:10 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 29784

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 395 windows · right 76% vs Kalshi 76% · logloss 0.4867 vs 0.4861 | 3669 windows · right 74% vs Kalshi 74% · logloss 0.5059 vs 0.5055 | — |
| SILVER | 395 windows · right 76% vs Kalshi 76% · logloss 0.4902 vs 0.49 | 3653 windows · right 74% vs Kalshi 74% · logloss 0.5098 vs 0.5104 | — |
| WTI | 454 windows · right 74% vs Kalshi 74% · logloss 0.5266 vs 0.5263 | 3878 windows · right 74% vs Kalshi 74% · logloss 0.5089 vs 0.5092 | — |
| BRENT | 454 windows · right 75% vs Kalshi 75% · logloss 0.505 vs 0.5037 · edge bets 2: won 0%, ROI -100% | 1091 windows · right 75% vs Kalshi 75% · logloss 0.5063 vs 0.5061 | — |
| COPPER | 395 windows · right 73% vs Kalshi 73% · logloss 0.5206 vs 0.5193 | 3281 windows · right 76% vs Kalshi 76% · logloss 0.4952 vs 0.4954 | — |
| NATGAS | 454 windows · right 75% vs Kalshi 75% · logloss 0.5052 vs 0.5079 | 3510 windows · right 75% vs Kalshi 75% · logloss 0.4994 vs 0.499 | — |
| PALLADIUM | 394 windows · right 74% vs Kalshi 74% · logloss 0.5259 vs 0.526 | 2060 windows · right 75% vs Kalshi 75% · logloss 0.5067 vs 0.5071 | — |
| PLATINUM | 395 windows · right 74% vs Kalshi 75% · logloss 0.5129 vs 0.5122 | 2415 windows · right 75% vs Kalshi 74% · logloss 0.509 vs 0.5096 | — |

**All weeks:** 3336 windows · right 75% vs Kalshi 75% · logloss 0.5094 vs 0.5092 · edge bets 2: won 0%, ROI -100%

**All months:** 23557 windows · right 75% vs Kalshi 75% · logloss 0.5049 vs 0.5051

| Month | Result |
|---|---|
| 2026-08 | 1742 windows · right 75% vs Kalshi 75% · logloss 0.4924 vs 0.4922 |
| 2026-09 | 6734 windows · right 75% vs Kalshi 74% · logloss 0.5082 vs 0.5083 |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.5052 vs 0.5055 |
| 2026-11 | 2935 windows · right 75% vs Kalshi 75% · logloss 0.5033 vs 0.5034 |

Strongest signals: `s_ASIA` -0.036, `m_NATGAS` +0.026, `tleft` -0.023, `m_PALLADIUM` -0.021, `s_US` +0.021

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,666, target reached normally 20% | setups 14,856, target reached normally 20% | — |
| SILVER | setups 1,732, target reached normally 23% | setups 14,886, target reached normally 21% | — |
| WTI | setups 1,808, target reached normally 23% | setups 15,907, target reached normally 21% | — |
| BRENT | setups 2,118, target reached normally 19% | setups 4,688, target reached normally 16% | — |
| COPPER | setups 1,886, target reached normally 20% | setups 14,873, target reached normally 15% | — |
| NATGAS | setups 1,865, target reached normally 17% | setups 15,669, target reached normally 16% | — |
| PALLADIUM | setups 1,704, target reached normally 20% | setups 8,328, target reached normally 14% | — |
| PLATINUM | setups 1,901, target reached normally 19% | setups 9,917, target reached normally 15% | — |

**All weeks:** setups 14,680, target reached normally 20%

**All months:** setups 99,124, target reached normally 18%
