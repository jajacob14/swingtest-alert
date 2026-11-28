# Kalshi commodity 15-min model report
Trained 2026-11-28 00:54 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 31821

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 390 windows · right 76% vs Kalshi 76% · logloss 0.4808 vs 0.4782 | 3691 windows · right 74% vs Kalshi 74% · logloss 0.5067 vs 0.506 | — |
| SILVER | 390 windows · right 76% vs Kalshi 76% · logloss 0.4833 vs 0.4832 | 3675 windows · right 74% vs Kalshi 74% · logloss 0.5101 vs 0.5103 | — |
| WTI | 458 windows · right 72% vs Kalshi 72% · logloss 0.5461 vs 0.5448 | 3927 windows · right 74% vs Kalshi 75% · logloss 0.5089 vs 0.5088 | — |
| BRENT | 457 windows · right 74% vs Kalshi 74% · logloss 0.5297 vs 0.5288 · edge bets 11: won 36%, ROI -31% | 1207 windows · right 75% vs Kalshi 75% · logloss 0.5013 vs 0.501 · edge bets 1: won 100%, ROI +96% | — |
| COPPER | 390 windows · right 74% vs Kalshi 74% · logloss 0.5131 vs 0.5135 | 3369 windows · right 76% vs Kalshi 76% · logloss 0.4943 vs 0.4941 | — |
| NATGAS | 458 windows · right 75% vs Kalshi 75% · logloss 0.506 vs 0.5087 · edge bets 3: won 67%, ROI +24% | 3626 windows · right 75% vs Kalshi 75% · logloss 0.4982 vs 0.4972 · edge bets 13: won 54%, ROI +4% | — |
| PALLADIUM | 390 windows · right 74% vs Kalshi 73% · logloss 0.5402 vs 0.5397 | 2148 windows · right 75% vs Kalshi 75% · logloss 0.5028 vs 0.503 | — |
| PLATINUM | 390 windows · right 74% vs Kalshi 74% · logloss 0.5224 vs 0.5212 | 2503 windows · right 75% vs Kalshi 75% · logloss 0.5073 vs 0.5076 | — |

**All weeks:** 3323 windows · right 74% vs Kalshi 74% · logloss 0.5159 vs 0.5156 · edge bets 14: won 43%, ROI -19%

**All months:** 24146 windows · right 75% vs Kalshi 75% · logloss 0.504 vs 0.5038 · edge bets 14: won 57%, ROI +11%

| Month | Result |
|---|---|
| 2026-08 | 1543 windows · right 75% vs Kalshi 75% · logloss 0.4945 vs 0.4937 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5085 vs 0.5083 · edge bets 4: won 50%, ROI -6% |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.5056 vs 0.5055 · edge bets 10: won 60%, ROI +18% |
| 2026-11 | 3723 windows · right 76% vs Kalshi 76% · logloss 0.494 vs 0.4937 |

Strongest signals: `s_ASIA` -0.029, `m_NATGAS` +0.025, `m_BRENT` +0.024, `tleft` -0.023, `dmid5` +0.022

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,663, target reached normally 20% | setups 14,946, target reached normally 20% | — |
| SILVER | setups 1,688, target reached normally 22% | setups 14,948, target reached normally 21% | — |
| WTI | setups 1,692, target reached normally 23% | setups 16,028, target reached normally 21% | — |
| BRENT | setups 2,045, target reached normally 20% | setups 5,193, target reached normally 15% | — |
| COPPER | setups 1,824, target reached normally 21% | setups 15,352, target reached normally 15% | — |
| NATGAS | setups 1,887, target reached normally 19% | setups 16,163, target reached normally 16% | — |
| PALLADIUM | setups 1,759, target reached normally 20% | setups 8,745, target reached normally 14% | — |
| PLATINUM | setups 1,844, target reached normally 21% | setups 10,303, target reached normally 16% | — |

**All weeks:** setups 14,402, target reached normally 21%

**All months:** setups 101,678, target reached normally 18%
