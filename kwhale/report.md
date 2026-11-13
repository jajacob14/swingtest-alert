# Kalshi commodity 15-min model report
Trained 2026-11-13 15:52 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 13577

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 410 windows · right 74% vs Kalshi 74% · logloss 0.5108 vs 0.5092 · edge bets 1: won 0%, ROI -100% | 3316 windows · right 74% vs Kalshi 74% · logloss 0.5057 vs 0.5062 | — |
| SILVER | 410 windows · right 75% vs Kalshi 75% · logloss 0.5079 vs 0.5061 | 3307 windows · right 74% vs Kalshi 74% · logloss 0.5084 vs 0.5093 | — |
| WTI | 430 windows · right 74% vs Kalshi 75% · logloss 0.5055 vs 0.5033 · edge bets 6: won 17%, ROI -72% | 3438 windows · right 75% vs Kalshi 75% · logloss 0.4998 vs 0.5004 | — |
| BRENT | 430 windows · right 75% vs Kalshi 74% · logloss 0.5065 vs 0.5056 | 186 windows · right 80% vs Kalshi 79% · logloss 0.4435 vs 0.4458 | — |
| COPPER | 410 windows · right 75% vs Kalshi 75% · logloss 0.4942 vs 0.4946 | 2474 windows · right 75% vs Kalshi 75% · logloss 0.5008 vs 0.5013 | — |
| NATGAS | 430 windows · right 73% vs Kalshi 73% · logloss 0.5262 vs 0.5263 · edge bets 1: won 0%, ROI -100% | 2605 windows · right 76% vs Kalshi 75% · logloss 0.496 vs 0.4964 | — |
| PALLADIUM | 411 windows · right 76% vs Kalshi 75% · logloss 0.5068 vs 0.5056 | 1253 windows · right 75% vs Kalshi 74% · logloss 0.5098 vs 0.5119 | — |
| PLATINUM | 411 windows · right 73% vs Kalshi 73% · logloss 0.5342 vs 0.5321 · edge bets 1: won 100%, ROI +72% | 1608 windows · right 75% vs Kalshi 75% · logloss 0.4992 vs 0.5007 | — |

**All weeks:** 3342 windows · right 74% vs Kalshi 74% · logloss 0.5115 vs 0.5103 · edge bets 9: won 22%, ROI -62%

**All months:** 18187 windows · right 75% vs Kalshi 75% · logloss 0.5021 vs 0.5028

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4979 vs 0.4983 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.508 vs 0.5083 |
| 2026-10 | 8331 windows · right 75% vs Kalshi 75% · logloss 0.4988 vs 0.5001 |

Strongest signals: `s_ASIA` -0.045, `dmid5` +0.035, `s_EU` +0.025, `s_US` +0.023, `ofi3` +0.022

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,763, target reached normally 24% | setups 13,773, target reached normally 19% | — |
| SILVER | setups 1,701, target reached normally 23% | setups 13,899, target reached normally 21% | — |
| WTI | setups 1,745, target reached normally 19% | setups 14,347, target reached normally 20% | — |
| BRENT | setups 2,036, target reached normally 19% | setups 768, target reached normally 11% | — |
| COPPER | setups 2,071, target reached normally 16% | setups 11,020, target reached normally 16% | — |
| NATGAS | setups 1,850, target reached normally 16% | setups 11,513, target reached normally 16% | — |
| PALLADIUM | setups 1,920, target reached normally 18% | setups 4,756, target reached normally 14% | — |
| PLATINUM | setups 1,843, target reached normally 20% | setups 6,508, target reached normally 14% | — |

**All weeks:** setups 14,929, target reached normally 19%

**All months:** setups 76,584, target reached normally 18%
