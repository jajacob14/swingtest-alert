# Kalshi commodity 15-min model report
Trained 2026-11-05 04:45 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 1550

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 385 windows · right 75% vs Kalshi 75% · logloss 0.4922 vs 0.4891 · edge bets 35: won 46%, ROI -22% | 2734 windows · right 74% vs Kalshi 74% · logloss 0.5109 vs 0.5109 · edge bets 35: won 51%, ROI -18% | — |
| SILVER | 384 windows · right 74% vs Kalshi 74% · logloss 0.5118 vs 0.5119 · edge bets 26: won 69%, ROI +13% | 2725 windows · right 74% vs Kalshi 74% · logloss 0.5148 vs 0.515 · edge bets 47: won 49%, ROI -19% | — |
| WTI | 429 windows · right 74% vs Kalshi 75% · logloss 0.5105 vs 0.5078 · edge bets 53: won 55%, ROI -11% | 2802 windows · right 76% vs Kalshi 76% · logloss 0.4964 vs 0.4963 · edge bets 58: won 53%, ROI -16% | — |
| BRENT | 428 windows · right 74% vs Kalshi 75% · logloss 0.5223 vs 0.5198 · edge bets 40: won 65%, ROI +4% | no data | — |
| COPPER | 384 windows · right 77% vs Kalshi 77% · logloss 0.4602 vs 0.462 · edge bets 6: won 67%, ROI +9% | 1892 windows · right 75% vs Kalshi 75% · logloss 0.5002 vs 0.5004 · edge bets 30: won 63%, ROI +8% | — |
| NATGAS | 428 windows · right 74% vs Kalshi 72% · logloss 0.5108 vs 0.5101 · edge bets 13: won 46%, ROI -22% | 1969 windows · right 75% vs Kalshi 75% · logloss 0.4938 vs 0.4941 · edge bets 12: won 75%, ROI +22% | — |
| PALLADIUM | 384 windows · right 75% vs Kalshi 75% · logloss 0.5052 vs 0.5055 · edge bets 60: won 60%, ROI +4% | 671 windows · right 75% vs Kalshi 75% · logloss 0.509 vs 0.5085 · edge bets 138: won 56%, ROI -2% | — |
| PLATINUM | 384 windows · right 73% vs Kalshi 73% · logloss 0.5235 vs 0.523 · edge bets 19: won 74%, ROI +21% | 1026 windows · right 75% vs Kalshi 75% · logloss 0.5037 vs 0.5036 · edge bets 51: won 57%, ROI -1% | — |

**All weeks:** 3206 windows · right 75% vs Kalshi 74% · logloss 0.5051 vs 0.5041 · edge bets 252: won 59%, ROI -2%

**All months:** 13819 windows · right 75% vs Kalshi 75% · logloss 0.5042 vs 0.5042 · edge bets 371: won 56%, ROI -6%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4984 vs 0.4983 · edge bets 52: won 52%, ROI -17% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5084 vs 0.5083 · edge bets 145: won 57%, ROI -6% |
| 2026-10 | 3963 windows · right 75% vs Kalshi 75% · logloss 0.5015 vs 0.5019 · edge bets 174: won 56%, ROI -3% |

Strongest signals: `s_ASIA` -0.055, `dmid5` +0.044, `s_EU` +0.036, `ofi3` +0.030, `m_PALLADIUM` -0.027

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | cheap rows 1,499, spike-to-target normally 20% | cheap rows 11,435, spike-to-target normally 19% | — |
| SILVER | cheap rows 1,551, spike-to-target normally 21% | cheap rows 11,532, spike-to-target normally 21% | — |
| WTI | cheap rows 1,665, spike-to-target normally 20% | cheap rows 11,781, spike-to-target normally 19% | — |
| BRENT | cheap rows 1,885, spike-to-target normally 18% | no data | — |
| COPPER | cheap rows 1,882, spike-to-target normally 12% | cheap rows 8,544, spike-to-target normally 17% | — |
| NATGAS | cheap rows 1,803, spike-to-target normally 17% | cheap rows 9,023, spike-to-target normally 16% | — |
| PALLADIUM | cheap rows 1,788, spike-to-target normally 16% | cheap rows 2,433, spike-to-target normally 13% | — |
| PLATINUM | cheap rows 1,708, spike-to-target normally 17% | cheap rows 4,168, spike-to-target normally 15% | — |

**All weeks:** cheap rows 13,781, spike-to-target normally 17%

**All months:** cheap rows 58,916, spike-to-target normally 18%
