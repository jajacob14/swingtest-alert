# Kalshi commodity 15-min model report
Trained 2026-11-06 03:09 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 3312

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 391 windows · right 75% vs Kalshi 75% · logloss 0.4987 vs 0.4984 · edge bets 14: won 50%, ROI -14% | 2818 windows · right 74% vs Kalshi 74% · logloss 0.5087 vs 0.5089 · edge bets 47: won 55%, ROI -11% | — |
| SILVER | 391 windows · right 74% vs Kalshi 74% · logloss 0.5238 vs 0.5227 · edge bets 14: won 79%, ROI +24% | 2809 windows · right 74% vs Kalshi 74% · logloss 0.5132 vs 0.5136 · edge bets 38: won 47%, ROI -23% | — |
| WTI | 426 windows · right 76% vs Kalshi 76% · logloss 0.498 vs 0.4977 · edge bets 45: won 51%, ROI -17% | 2891 windows · right 76% vs Kalshi 76% · logloss 0.4964 vs 0.4963 · edge bets 88: won 51%, ROI -16% | — |
| BRENT | 426 windows · right 75% vs Kalshi 75% · logloss 0.5091 vs 0.5072 · edge bets 22: won 73%, ROI +14% | no data | — |
| COPPER | 391 windows · right 77% vs Kalshi 77% · logloss 0.464 vs 0.464 · edge bets 1: won 100%, ROI +96% | 1976 windows · right 75% vs Kalshi 75% · logloss 0.4998 vs 0.4999 · edge bets 56: won 68%, ROI +13% | — |
| NATGAS | 426 windows · right 75% vs Kalshi 74% · logloss 0.4953 vs 0.4958 · edge bets 6: won 33%, ROI -46% | 2058 windows · right 75% vs Kalshi 75% · logloss 0.497 vs 0.4973 · edge bets 10: won 70%, ROI +14% | — |
| PALLADIUM | 391 windows · right 75% vs Kalshi 75% · logloss 0.4978 vs 0.4958 · edge bets 48: won 60%, ROI -0% | 755 windows · right 75% vs Kalshi 75% · logloss 0.5069 vs 0.509 · edge bets 85: won 56%, ROI -0% | — |
| PLATINUM | 391 windows · right 72% vs Kalshi 72% · logloss 0.5352 vs 0.5344 · edge bets 7: won 86%, ROI +39% | 1110 windows · right 75% vs Kalshi 75% · logloss 0.5028 vs 0.5039 · edge bets 18: won 61%, ROI +3% | — |

**All weeks:** 3233 windows · right 75% vs Kalshi 75% · logloss 0.5025 vs 0.5018 · edge bets 157: won 60%, ROI -1%

**All months:** 14417 windows · right 75% vs Kalshi 75% · logloss 0.5036 vs 0.504 · edge bets 342: won 56%, ROI -6%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4983 vs 0.4983 · edge bets 56: won 52%, ROI -16% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5085 vs 0.5083 · edge bets 129: won 57%, ROI -6% |
| 2026-10 | 4561 windows · right 75% vs Kalshi 75% · logloss 0.5002 vs 0.5015 · edge bets 157: won 58%, ROI -1% |

Strongest signals: `s_ASIA` -0.055, `dmid5` +0.052, `s_EU` +0.043, `ofi3` +0.028, `bigc` -0.027

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | cheap rows 1,610, spike-to-target normally 22% | cheap rows 11,762, spike-to-target normally 19% | — |
| SILVER | cheap rows 1,635, spike-to-target normally 24% | cheap rows 11,866, spike-to-target normally 21% | — |
| WTI | cheap rows 1,611, spike-to-target normally 21% | cheap rows 12,131, spike-to-target normally 19% | — |
| BRENT | cheap rows 1,843, spike-to-target normally 19% | no data | — |
| COPPER | cheap rows 1,955, spike-to-target normally 13% | cheap rows 8,894, spike-to-target normally 17% | — |
| NATGAS | cheap rows 1,822, spike-to-target normally 16% | cheap rows 9,404, spike-to-target normally 16% | — |
| PALLADIUM | cheap rows 1,794, spike-to-target normally 16% | cheap rows 2,761, spike-to-target normally 13% | — |
| PLATINUM | cheap rows 1,729, spike-to-target normally 17% | cheap rows 4,510, spike-to-target normally 15% | — |

**All weeks:** cheap rows 13,999, spike-to-target normally 18%

**All months:** cheap rows 61,328, spike-to-target normally 18%
