# Kalshi commodity 15-min model report
Trained 2026-11-06 14:40 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 4288

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 398 windows · right 75% vs Kalshi 75% · logloss 0.503 vs 0.503 · edge bets 9: won 67%, ROI +7% | 2864 windows · right 74% vs Kalshi 74% · logloss 0.5096 vs 0.5098 · edge bets 40: won 55%, ROI -12% | — |
| SILVER | 398 windows · right 74% vs Kalshi 75% · logloss 0.5152 vs 0.5151 · edge bets 11: won 82%, ROI +28% | 2855 windows · right 74% vs Kalshi 74% · logloss 0.5141 vs 0.5144 · edge bets 40: won 52%, ROI -14% | — |
| WTI | 418 windows · right 76% vs Kalshi 76% · logloss 0.493 vs 0.4939 · edge bets 17: won 47%, ROI -27% | 2937 windows · right 76% vs Kalshi 76% · logloss 0.4969 vs 0.4973 · edge bets 63: won 49%, ROI -21% | — |
| BRENT | 418 windows · right 77% vs Kalshi 77% · logloss 0.4911 vs 0.4913 · edge bets 13: won 77%, ROI +18% | no data | — |
| COPPER | 399 windows · right 77% vs Kalshi 77% · logloss 0.4651 vs 0.4658 · edge bets 1: won 100%, ROI +96% | 2022 windows · right 75% vs Kalshi 75% · logloss 0.4996 vs 0.4998 · edge bets 45: won 67%, ROI +11% | — |
| NATGAS | 418 windows · right 75% vs Kalshi 75% · logloss 0.4923 vs 0.4919 · edge bets 6: won 17%, ROI -72% | 2104 windows · right 75% vs Kalshi 75% · logloss 0.4974 vs 0.4975 · edge bets 11: won 64%, ROI +1% | — |
| PALLADIUM | 399 windows · right 77% vs Kalshi 76% · logloss 0.482 vs 0.4827 · edge bets 36: won 69%, ROI +16% | 801 windows · right 75% vs Kalshi 74% · logloss 0.5138 vs 0.5152 · edge bets 90: won 58%, ROI +2% | ✅ |
| PLATINUM | 399 windows · right 74% vs Kalshi 73% · logloss 0.52 vs 0.5202 · edge bets 5: won 80%, ROI +36% | 1156 windows · right 75% vs Kalshi 75% · logloss 0.5046 vs 0.5055 · edge bets 33: won 70%, ROI +20% | — |

**All weeks:** 3247 windows · right 76% vs Kalshi 76% · logloss 0.495 vs 0.4953 · edge bets 98: won 65%, ROI +6%

**All months:** 14739 windows · right 75% vs Kalshi 75% · logloss 0.5046 vs 0.505 · edge bets 322: won 58%, ROI -4%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4982 vs 0.4983 · edge bets 48: won 50%, ROI -20% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5084 vs 0.5083 · edge bets 111: won 57%, ROI -6% |
| 2026-10 | 4883 windows · right 75% vs Kalshi 75% · logloss 0.5036 vs 0.5048 · edge bets 163: won 61%, ROI +3% |

Strongest signals: `s_ASIA` -0.054, `dmid5` +0.052, `s_EU` +0.037, `ofi3` +0.032, `bigc` -0.027

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | cheap rows 1,584, spike-to-target normally 23% | cheap rows 11,946, spike-to-target normally 19% | — |
| SILVER | cheap rows 1,644, spike-to-target normally 23% | cheap rows 12,057, spike-to-target normally 21% | — |
| WTI | cheap rows 1,624, spike-to-target normally 20% | cheap rows 12,336, spike-to-target normally 19% | — |
| BRENT | cheap rows 1,851, spike-to-target normally 17% | no data | — |
| COPPER | cheap rows 2,007, spike-to-target normally 14% | cheap rows 9,104, spike-to-target normally 17% | — |
| NATGAS | cheap rows 1,808, spike-to-target normally 17% | cheap rows 9,550, spike-to-target normally 16% | — |
| PALLADIUM | cheap rows 1,806, spike-to-target normally 17% | cheap rows 2,919, spike-to-target normally 14% | — |
| PLATINUM | cheap rows 1,739, spike-to-target normally 17% | cheap rows 4,712, spike-to-target normally 15% | — |

**All weeks:** cheap rows 14,063, spike-to-target normally 18%

**All months:** cheap rows 62,624, spike-to-target normally 18%
