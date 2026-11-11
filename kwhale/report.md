# Kalshi commodity 15-min model report
Trained 2026-11-11 06:17 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 9432

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 399 windows · right 77% vs Kalshi 77% · logloss 0.478 vs 0.4787 · edge bets 4: won 75%, ROI +32% | 3104 windows · right 74% vs Kalshi 74% · logloss 0.5064 vs 0.5068 · edge bets 12: won 67%, ROI +8% | — |
| SILVER | 400 windows · right 77% vs Kalshi 77% · logloss 0.4903 vs 0.4912 · edge bets 1: won 100%, ROI +64% | 3095 windows · right 74% vs Kalshi 74% · logloss 0.5099 vs 0.5109 · edge bets 19: won 58%, ROI -4% | — |
| WTI | 444 windows · right 75% vs Kalshi 75% · logloss 0.491 vs 0.4922 · edge bets 4: won 25%, ROI -61% | 3216 windows · right 75% vs Kalshi 75% · logloss 0.499 vs 0.4997 · edge bets 5: won 60%, ROI +0% | — |
| BRENT | 443 windows · right 76% vs Kalshi 76% · logloss 0.4893 vs 0.4889 | no data | — |
| COPPER | 400 windows · right 78% vs Kalshi 79% · logloss 0.4532 vs 0.4535 · edge bets 3: won 0%, ROI -100% | 2262 windows · right 75% vs Kalshi 75% · logloss 0.5044 vs 0.5045 · edge bets 2: won 50%, ROI -21% | — |
| NATGAS | 443 windows · right 75% vs Kalshi 75% · logloss 0.5081 vs 0.5091 | 2383 windows · right 75% vs Kalshi 75% · logloss 0.4967 vs 0.4968 · edge bets 2: won 100%, ROI +64% | — |
| PALLADIUM | 400 windows · right 79% vs Kalshi 79% · logloss 0.4513 vs 0.4482 · edge bets 46: won 54%, ROI -7% | 1041 windows · right 74% vs Kalshi 74% · logloss 0.5138 vs 0.5157 · edge bets 53: won 66%, ROI +15% | — |
| PLATINUM | 401 windows · right 75% vs Kalshi 75% · logloss 0.5001 vs 0.4994 · edge bets 12: won 50%, ROI -12% | 1396 windows · right 75% vs Kalshi 75% · logloss 0.4999 vs 0.501 · edge bets 29: won 62%, ROI +9% | — |

**All weeks:** 3330 windows · right 76% vs Kalshi 77% · logloss 0.4833 vs 0.4833 · edge bets 70: won 51%, ROI -11%

**All months:** 16497 windows · right 75% vs Kalshi 75% · logloss 0.5038 vs 0.5045 · edge bets 122: won 64%, ROI +9%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4979 vs 0.4983 · edge bets 9: won 67%, ROI +10% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5081 vs 0.5083 · edge bets 27: won 67%, ROI +12% |
| 2026-10 | 6641 windows · right 75% vs Kalshi 75% · logloss 0.5023 vs 0.5035 · edge bets 86: won 63%, ROI +9% |

Strongest signals: `s_ASIA` -0.053, `dmid5` +0.046, `s_EU` +0.034, `ofi3` +0.033, `s_US` +0.024

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,714, target reached normally 23% | setups 12,960, target reached normally 19% | — |
| SILVER | setups 1,668, target reached normally 24% | setups 13,090, target reached normally 21% | — |
| WTI | setups 1,679, target reached normally 18% | setups 13,419, target reached normally 19% | — |
| BRENT | setups 1,984, target reached normally 17% | no data | — |
| COPPER | setups 2,162, target reached normally 13% | setups 10,047, target reached normally 17% | — |
| NATGAS | setups 1,946, target reached normally 16% | setups 10,635, target reached normally 16% | — |
| PALLADIUM | setups 1,820, target reached normally 15% | setups 3,890, target reached normally 14% | — |
| PLATINUM | setups 1,739, target reached normally 18% | setups 5,725, target reached normally 15% | — |

**All weeks:** setups 14,712, target reached normally 18%

**All months:** setups 69,766, target reached normally 18%
