# Kalshi commodity 15-min model report
Trained 2026-11-04 22:26 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 99% of rows · commodity whale events on file: 1035

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 377 windows · right 75% vs Kalshi 75% · logloss 0.4964 vs 0.4931 · edge bets 30: won 50%, ROI -16% | 2716 windows · right 74% vs Kalshi 74% · logloss 0.5117 vs 0.5115 · edge bets 36: won 56%, ROI -11% | — |
| SILVER | 378 windows · right 74% vs Kalshi 74% · logloss 0.5141 vs 0.5149 · edge bets 15: won 80%, ROI +30% | 2707 windows · right 74% vs Kalshi 74% · logloss 0.5152 vs 0.5153 · edge bets 58: won 53%, ROI -13% | — |
| WTI | 422 windows · right 75% vs Kalshi 76% · logloss 0.5009 vs 0.4983 · edge bets 67: won 57%, ROI -5% | 2784 windows · right 76% vs Kalshi 76% · logloss 0.4967 vs 0.4963 · edge bets 98: won 57%, ROI -8% | — |
| BRENT | 422 windows · right 74% vs Kalshi 74% · logloss 0.5151 vs 0.5131 · edge bets 56: won 62%, ROI +1% | no data | — |
| COPPER | 377 windows · right 77% vs Kalshi 77% · logloss 0.4671 vs 0.4709 · edge bets 6: won 100%, ROI +57% | 1874 windows · right 75% vs Kalshi 75% · logloss 0.5002 vs 0.5001 · edge bets 58: won 66%, ROI +13% | — |
| NATGAS | 422 windows · right 74% vs Kalshi 73% · logloss 0.5077 vs 0.5059 · edge bets 15: won 40%, ROI -31% | 1951 windows · right 75% vs Kalshi 76% · logloss 0.4921 vs 0.4926 · edge bets 16: won 62%, ROI +3% | — |
| PALLADIUM | 378 windows · right 75% vs Kalshi 74% · logloss 0.5134 vs 0.5145 · edge bets 57: won 63%, ROI +9% | 653 windows · right 74% vs Kalshi 74% · logloss 0.5129 vs 0.5118 · edge bets 131: won 56%, ROI -2% | — |
| PLATINUM | 378 windows · right 72% vs Kalshi 72% · logloss 0.5327 vs 0.5325 · edge bets 17: won 82%, ROI +35% | 1008 windows · right 75% vs Kalshi 75% · logloss 0.5062 vs 0.506 · edge bets 53: won 55%, ROI -6% | — |

**All weeks:** 3154 windows · right 74% vs Kalshi 74% · logloss 0.506 vs 0.5054 · edge bets 263: won 62%, ROI +3%

**All months:** 13693 windows · right 75% vs Kalshi 75% · logloss 0.5046 vs 0.5045 · edge bets 450: won 57%, ROI -4%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4985 vs 0.4983 · edge bets 69: won 56%, ROI -9% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5086 vs 0.5083 · edge bets 191: won 58%, ROI -4% |
| 2026-10 | 3837 windows · right 75% vs Kalshi 75% · logloss 0.5025 vs 0.5028 · edge bets 190: won 57%, ROI -3% |

Strongest signals: `s_ASIA` -0.055, `dmid5` +0.048, `s_EU` +0.036, `ofi3` +0.030, `m_PALLADIUM` -0.026

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | cheap rows 1,483, spike-to-target normally 18% | cheap rows 11,367, spike-to-target normally 19% | — |
| SILVER | cheap rows 1,516, spike-to-target normally 21% | cheap rows 11,454, spike-to-target normally 21% | — |
| WTI | cheap rows 1,648, spike-to-target normally 21% | cheap rows 11,703, spike-to-target normally 19% | — |
| BRENT | cheap rows 1,835, spike-to-target normally 18% | no data | — |
| COPPER | cheap rows 1,796, spike-to-target normally 13% | cheap rows 8,475, spike-to-target normally 17% | — |
| NATGAS | cheap rows 1,785, spike-to-target normally 17% | cheap rows 8,938, spike-to-target normally 15% | — |
| PALLADIUM | cheap rows 1,706, spike-to-target normally 16% | cheap rows 2,357, spike-to-target normally 14% | — |
| PLATINUM | cheap rows 1,671, spike-to-target normally 17% | cheap rows 4,078, spike-to-target normally 15% | — |

**All weeks:** cheap rows 13,440, spike-to-target normally 18%

**All months:** cheap rows 58,372, spike-to-target normally 18%
