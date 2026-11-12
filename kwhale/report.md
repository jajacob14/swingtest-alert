# Kalshi commodity 15-min model report
Trained 2026-11-12 16:51 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 11829

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 402 windows · right 75% vs Kalshi 76% · logloss 0.497 vs 0.4958 · edge bets 8: won 50%, ROI -14% | 3226 windows · right 74% vs Kalshi 74% · logloss 0.5062 vs 0.5067 | — |
| SILVER | 402 windows · right 76% vs Kalshi 76% · logloss 0.4919 vs 0.4902 · edge bets 2: won 100%, ROI +68% | 3217 windows · right 74% vs Kalshi 74% · logloss 0.5087 vs 0.5097 | — |
| WTI | 445 windows · right 76% vs Kalshi 76% · logloss 0.4878 vs 0.4856 · edge bets 10: won 20%, ROI -68% | 3346 windows · right 75% vs Kalshi 75% · logloss 0.5008 vs 0.5014 | — |
| BRENT | 446 windows · right 77% vs Kalshi 77% · logloss 0.4804 vs 0.4796 · edge bets 1: won 100%, ROI +61% | 94 windows · right 79% vs Kalshi 78% · logloss 0.4686 vs 0.4682 | — |
| COPPER | 401 windows · right 76% vs Kalshi 76% · logloss 0.4832 vs 0.4804 · edge bets 6: won 33%, ROI -42% | 2384 windows · right 75% vs Kalshi 75% · logloss 0.502 vs 0.5026 | — |
| NATGAS | 446 windows · right 74% vs Kalshi 74% · logloss 0.5199 vs 0.5193 · edge bets 2: won 50%, ROI -17% | 2513 windows · right 75% vs Kalshi 75% · logloss 0.4968 vs 0.4971 | — |
| PALLADIUM | 402 windows · right 77% vs Kalshi 77% · logloss 0.4807 vs 0.4806 · edge bets 15: won 27%, ROI -53% | 1163 windows · right 74% vs Kalshi 74% · logloss 0.5117 vs 0.5141 · edge bets 29: won 55%, ROI +1% | — |
| PLATINUM | 402 windows · right 74% vs Kalshi 74% · logloss 0.514 vs 0.5118 · edge bets 9: won 44%, ROI -22% | 1518 windows · right 75% vs Kalshi 75% · logloss 0.5017 vs 0.5031 | — |

**All weeks:** 3346 windows · right 76% vs Kalshi 76% · logloss 0.4945 vs 0.493 · edge bets 53: won 38%, ROI -36%

**All months:** 17461 windows · right 75% vs Kalshi 75% · logloss 0.5035 vs 0.5042 · edge bets 29: won 55%, ROI +1%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4978 vs 0.4983 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5081 vs 0.5083 · edge bets 3: won 67%, ROI +17% |
| 2026-10 | 7605 windows · right 75% vs Kalshi 75% · logloss 0.5017 vs 0.5031 · edge bets 26: won 54%, ROI -1% |

Strongest signals: `s_ASIA` -0.049, `dmid5` +0.037, `s_EU` +0.027, `s_US` +0.026, `ofi3` +0.021

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,715, target reached normally 23% | setups 13,437, target reached normally 19% | — |
| SILVER | setups 1,692, target reached normally 23% | setups 13,571, target reached normally 21% | — |
| WTI | setups 1,810, target reached normally 17% | setups 13,938, target reached normally 19% | — |
| BRENT | setups 2,116, target reached normally 16% | setups 364, target reached normally 14% | — |
| COPPER | setups 2,063, target reached normally 15% | setups 10,645, target reached normally 16% | — |
| NATGAS | setups 1,896, target reached normally 17% | setups 11,127, target reached normally 16% | — |
| PALLADIUM | setups 1,851, target reached normally 16% | setups 4,379, target reached normally 14% | — |
| PLATINUM | setups 1,802, target reached normally 19% | setups 6,186, target reached normally 15% | — |

**All weeks:** setups 14,945, target reached normally 18%

**All months:** setups 73,647, target reached normally 18%
