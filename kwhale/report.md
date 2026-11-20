# Kalshi commodity 15-min model report
Trained 2026-11-19 21:36 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 21114

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 399 windows · right 75% vs Kalshi 75% · logloss 0.4926 vs 0.494 | 3505 windows · right 74% vs Kalshi 74% · logloss 0.5099 vs 0.5094 | — |
| SILVER | 400 windows · right 75% vs Kalshi 75% · logloss 0.4992 vs 0.4981 | 3489 windows · right 74% vs Kalshi 74% · logloss 0.5095 vs 0.5106 | — |
| WTI | 448 windows · right 75% vs Kalshi 75% · logloss 0.4878 vs 0.4887 | 3664 windows · right 75% vs Kalshi 75% · logloss 0.5061 vs 0.5062 | — |
| BRENT | 449 windows · right 77% vs Kalshi 77% · logloss 0.4725 vs 0.474 | 609 windows · right 75% vs Kalshi 76% · logloss 0.4951 vs 0.495 | — |
| COPPER | 399 windows · right 75% vs Kalshi 76% · logloss 0.4982 vs 0.4986 | 2848 windows · right 75% vs Kalshi 75% · logloss 0.4996 vs 0.5002 | — |
| NATGAS | 448 windows · right 75% vs Kalshi 75% · logloss 0.4988 vs 0.5005 | 3028 windows · right 75% vs Kalshi 75% · logloss 0.4972 vs 0.4967 · edge bets 14: won 43%, ROI -23% | — |
| PALLADIUM | 399 windows · right 74% vs Kalshi 74% · logloss 0.5099 vs 0.5102 | 1627 windows · right 75% vs Kalshi 75% · logloss 0.5054 vs 0.5074 | — |
| PLATINUM | 400 windows · right 74% vs Kalshi 74% · logloss 0.5048 vs 0.5053 | 1982 windows · right 75% vs Kalshi 75% · logloss 0.5033 vs 0.5047 | — |

**All weeks:** 3342 windows · right 75% vs Kalshi 75% · logloss 0.4949 vs 0.4957

**All months:** 20752 windows · right 75% vs Kalshi 75% · logloss 0.5044 vs 0.5049 · edge bets 14: won 43%, ROI -23%

| Month | Result |
|---|---|
| 2026-08 | 2548 windows · right 75% vs Kalshi 75% · logloss 0.4988 vs 0.4995 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5082 vs 0.5083 · edge bets 3: won 33%, ROI -42% |
| 2026-10 | 11470 windows · right 75% vs Kalshi 75% · logloss 0.5035 vs 0.504 · edge bets 11: won 46%, ROI -17% |

Strongest signals: `s_ASIA` -0.044, `s_EU` +0.038, `ofi3` +0.029, `dmid5` +0.027, `tleft` -0.024

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,641, target reached normally 20% | setups 14,372, target reached normally 20% | — |
| SILVER | setups 1,692, target reached normally 20% | setups 14,327, target reached normally 21% | — |
| WTI | setups 1,777, target reached normally 19% | setups 15,307, target reached normally 20% | — |
| BRENT | setups 2,084, target reached normally 18% | setups 2,572, target reached normally 12% | — |
| COPPER | setups 2,041, target reached normally 18% | setups 12,675, target reached normally 16% | — |
| NATGAS | setups 1,701, target reached normally 16% | setups 13,617, target reached normally 16% | — |
| PALLADIUM | setups 1,786, target reached normally 16% | setups 6,315, target reached normally 14% | — |
| PLATINUM | setups 1,973, target reached normally 20% | setups 7,952, target reached normally 15% | — |

**All weeks:** setups 14,695, target reached normally 18%

**All months:** setups 87,137, target reached normally 18%
