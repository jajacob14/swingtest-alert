# Kalshi commodity 15-min model report
Trained 2026-11-05 16:16 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 2426

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 386 windows · right 75% vs Kalshi 76% · logloss 0.4992 vs 0.4961 · edge bets 49: won 49%, ROI -18% | 2779 windows · right 74% vs Kalshi 74% · logloss 0.5106 vs 0.5105 · edge bets 49: won 51%, ROI -18% | — |
| SILVER | 386 windows · right 74% vs Kalshi 74% · logloss 0.5208 vs 0.5209 · edge bets 30: won 70%, ROI +16% | 2770 windows · right 74% vs Kalshi 74% · logloss 0.5147 vs 0.5149 · edge bets 61: won 56%, ROI -7% | — |
| WTI | 430 windows · right 75% vs Kalshi 75% · logloss 0.5079 vs 0.5065 · edge bets 54: won 54%, ROI -13% | 2848 windows · right 76% vs Kalshi 76% · logloss 0.4959 vs 0.4961 · edge bets 59: won 48%, ROI -24% | — |
| BRENT | 430 windows · right 75% vs Kalshi 75% · logloss 0.5162 vs 0.5151 · edge bets 29: won 76%, ROI +20% | no data | — |
| COPPER | 385 windows · right 76% vs Kalshi 76% · logloss 0.4761 vs 0.4757 · edge bets 11: won 73%, ROI +16% | 1937 windows · right 75% vs Kalshi 75% · logloss 0.5006 vs 0.5006 · edge bets 69: won 62%, ROI +9% | — |
| NATGAS | 430 windows · right 74% vs Kalshi 73% · logloss 0.5033 vs 0.5047 · edge bets 14: won 50%, ROI -18% | 2015 windows · right 75% vs Kalshi 75% · logloss 0.4961 vs 0.4963 · edge bets 14: won 64%, ROI +8% | — |
| PALLADIUM | 387 windows · right 75% vs Kalshi 74% · logloss 0.507 vs 0.5053 · edge bets 66: won 59%, ROI +2% | 716 windows · right 74% vs Kalshi 74% · logloss 0.5126 vs 0.5128 · edge bets 118: won 56%, ROI -2% | — |
| PLATINUM | 386 windows · right 73% vs Kalshi 72% · logloss 0.5362 vs 0.5354 · edge bets 20: won 75%, ROI +23% | 1071 windows · right 75% vs Kalshi 75% · logloss 0.5059 vs 0.5058 · edge bets 71: won 55%, ROI -6% | — |

**All weeks:** 3220 windows · right 74% vs Kalshi 74% · logloss 0.5083 vs 0.5075 · edge bets 273: won 60%, ROI -0%

**All months:** 14136 windows · right 75% vs Kalshi 75% · logloss 0.5047 vs 0.5048 · edge bets 441: won 55%, ROI -6%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4983 vs 0.4983 · edge bets 61: won 48%, ROI -22% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5084 vs 0.5083 · edge bets 181: won 55%, ROI -7% |
| 2026-10 | 4280 windows · right 75% vs Kalshi 75% · logloss 0.5036 vs 0.5041 · edge bets 199: won 58%, ROI -1% |

Strongest signals: `s_ASIA` -0.058, `dmid5` +0.048, `s_EU` +0.044, `ofi3` +0.026, `spread` +0.022

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | cheap rows 1,530, spike-to-target normally 21% | cheap rows 11,592, spike-to-target normally 19% | — |
| SILVER | cheap rows 1,571, spike-to-target normally 24% | cheap rows 11,684, spike-to-target normally 21% | — |
| WTI | cheap rows 1,650, spike-to-target normally 21% | cheap rows 11,965, spike-to-target normally 19% | — |
| BRENT | cheap rows 1,868, spike-to-target normally 19% | no data | — |
| COPPER | cheap rows 1,888, spike-to-target normally 13% | cheap rows 8,718, spike-to-target normally 17% | — |
| NATGAS | cheap rows 1,752, spike-to-target normally 16% | cheap rows 9,192, spike-to-target normally 16% | — |
| PALLADIUM | cheap rows 1,781, spike-to-target normally 16% | cheap rows 2,572, spike-to-target normally 13% | — |
| PLATINUM | cheap rows 1,704, spike-to-target normally 17% | cheap rows 4,320, spike-to-target normally 15% | — |

**All weeks:** cheap rows 13,744, spike-to-target normally 18%

**All months:** cheap rows 60,043, spike-to-target normally 18%
