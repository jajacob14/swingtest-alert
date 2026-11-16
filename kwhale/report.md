# Kalshi commodity 15-min model report
Trained 2026-11-16 12:58 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 15273

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 401 windows · right 72% vs Kalshi 73% · logloss 0.5415 vs 0.5376 · edge bets 1: won 0%, ROI -100% | 3314 windows · right 74% vs Kalshi 74% · logloss 0.5089 vs 0.5093 | — |
| SILVER | 401 windows · right 74% vs Kalshi 74% · logloss 0.5178 vs 0.5163 · edge bets 3: won 100%, ROI +68% | 3297 windows · right 74% vs Kalshi 74% · logloss 0.5125 vs 0.5133 | — |
| WTI | 446 windows · right 75% vs Kalshi 75% · logloss 0.4992 vs 0.4964 | 3453 windows · right 75% vs Kalshi 75% · logloss 0.5043 vs 0.5048 | — |
| BRENT | 445 windows · right 74% vs Kalshi 75% · logloss 0.4994 vs 0.496 | 294 windows · right 76% vs Kalshi 76% · logloss 0.4789 vs 0.4814 | — |
| COPPER | 402 windows · right 76% vs Kalshi 76% · logloss 0.4972 vs 0.4968 | 2553 windows · right 75% vs Kalshi 75% · logloss 0.4988 vs 0.4995 | — |
| NATGAS | 445 windows · right 75% vs Kalshi 75% · logloss 0.5128 vs 0.5134 · edge bets 1: won 0%, ROI -100% | 2713 windows · right 75% vs Kalshi 75% · logloss 0.4955 vs 0.4961 | — |
| PALLADIUM | 401 windows · right 74% vs Kalshi 74% · logloss 0.5222 vs 0.5187 | 1332 windows · right 75% vs Kalshi 75% · logloss 0.5074 vs 0.5094 | — |
| PLATINUM | 401 windows · right 73% vs Kalshi 73% · logloss 0.542 vs 0.5397 | 1687 windows · right 75% vs Kalshi 75% · logloss 0.5028 vs 0.5041 | — |

**All weeks:** 3342 windows · right 74% vs Kalshi 74% · logloss 0.5158 vs 0.5137 · edge bets 5: won 60%, ROI +5%

**All months:** 18643 windows · right 75% vs Kalshi 75% · logloss 0.5042 vs 0.505

| Month | Result |
|---|---|
| 2026-08 | 2859 windows · right 75% vs Kalshi 75% · logloss 0.5013 vs 0.5019 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.508 vs 0.5083 |
| 2026-10 | 9050 windows · right 75% vs Kalshi 75% · logloss 0.5023 vs 0.5034 |

Strongest signals: `s_ASIA` -0.040, `dmid5` +0.028, `s_EU` +0.027, `ofi3` +0.025, `m_BRENT` +0.022

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,668, target reached normally 25% | setups 13,690, target reached normally 19% | — |
| SILVER | setups 1,639, target reached normally 21% | setups 13,670, target reached normally 21% | — |
| WTI | setups 1,821, target reached normally 19% | setups 14,437, target reached normally 20% | — |
| BRENT | setups 2,102, target reached normally 19% | setups 1,167, target reached normally 10% | — |
| COPPER | setups 2,037, target reached normally 16% | setups 11,363, target reached normally 16% | — |
| NATGAS | setups 1,800, target reached normally 17% | setups 11,999, target reached normally 16% | — |
| PALLADIUM | setups 1,936, target reached normally 18% | setups 5,114, target reached normally 14% | — |
| PLATINUM | setups 1,828, target reached normally 20% | setups 6,779, target reached normally 15% | — |

**All weeks:** setups 14,831, target reached normally 19%

**All months:** setups 78,219, target reached normally 18%
