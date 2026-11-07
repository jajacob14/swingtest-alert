# Kalshi commodity 15-min model report
Trained 2026-11-06 22:25 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 4740

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 392 windows · right 74% vs Kalshi 75% · logloss 0.5108 vs 0.5112 · edge bets 17: won 53%, ROI -15% | 2870 windows · right 74% vs Kalshi 74% · logloss 0.5093 vs 0.5095 · edge bets 55: won 53%, ROI -16% | — |
| SILVER | 392 windows · right 74% vs Kalshi 74% · logloss 0.5168 vs 0.5169 · edge bets 11: won 73%, ROI +16% | 2861 windows · right 74% vs Kalshi 74% · logloss 0.5136 vs 0.5139 · edge bets 50: won 58%, ROI -5% | — |
| WTI | 433 windows · right 76% vs Kalshi 76% · logloss 0.4969 vs 0.4977 · edge bets 12: won 50%, ROI -23% | 2968 windows · right 75% vs Kalshi 75% · logloss 0.4979 vs 0.4985 · edge bets 52: won 52%, ROI -16% | — |
| BRENT | 434 windows · right 77% vs Kalshi 78% · logloss 0.4844 vs 0.4851 · edge bets 10: won 70%, ROI +9% | no data | — |
| COPPER | 393 windows · right 77% vs Kalshi 77% · logloss 0.4689 vs 0.4696 · edge bets 1: won 100%, ROI +96% | 2028 windows · right 75% vs Kalshi 75% · logloss 0.4996 vs 0.4997 · edge bets 46: won 65%, ROI +10% | — |
| NATGAS | 433 windows · right 76% vs Kalshi 76% · logloss 0.4855 vs 0.4856 · edge bets 7: won 14%, ROI -76% | 2135 windows · right 75% vs Kalshi 75% · logloss 0.4976 vs 0.4977 · edge bets 14: won 71%, ROI +17% | — |
| PALLADIUM | 392 windows · right 77% vs Kalshi 76% · logloss 0.4781 vs 0.478 · edge bets 46: won 65%, ROI +12% | 807 windows · right 74% vs Kalshi 74% · logloss 0.5145 vs 0.5159 · edge bets 94: won 57%, ROI +1% | — |
| PLATINUM | 393 windows · right 74% vs Kalshi 74% · logloss 0.5155 vs 0.5155 · edge bets 5: won 80%, ROI +36% | 1162 windows · right 75% vs Kalshi 75% · logloss 0.5041 vs 0.505 · edge bets 40: won 68%, ROI +15% | — |

**All weeks:** 3262 windows · right 76% vs Kalshi 76% · logloss 0.4942 vs 0.4946 · edge bets 109: won 61%, ROI -0%

**All months:** 14831 windows · right 75% vs Kalshi 75% · logloss 0.5047 vs 0.5051 · edge bets 351: won 59%, ROI -2%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4981 vs 0.4983 · edge bets 51: won 55%, ROI -12% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5084 vs 0.5083 · edge bets 123: won 57%, ROI -5% |
| 2026-10 | 4975 windows · right 75% vs Kalshi 75% · logloss 0.5038 vs 0.505 · edge bets 177: won 61%, ROI +4% |

Strongest signals: `dmid5` +0.054, `s_ASIA` -0.053, `s_EU` +0.036, `ofi3` +0.032, `bigc` -0.029

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | cheap rows 1,566, spike-to-target normally 23% | cheap rows 11,971, spike-to-target normally 19% | — |
| SILVER | cheap rows 1,625, spike-to-target normally 23% | cheap rows 12,083, spike-to-target normally 21% | — |
| WTI | cheap rows 1,660, spike-to-target normally 20% | cheap rows 12,406, spike-to-target normally 19% | — |
| BRENT | cheap rows 1,897, spike-to-target normally 17% | no data | — |
| COPPER | cheap rows 1,965, spike-to-target normally 14% | cheap rows 9,129, spike-to-target normally 17% | — |
| NATGAS | cheap rows 1,869, spike-to-target normally 16% | cheap rows 9,646, spike-to-target normally 16% | — |
| PALLADIUM | cheap rows 1,777, spike-to-target normally 16% | cheap rows 2,930, spike-to-target normally 14% | — |
| PLATINUM | cheap rows 1,729, spike-to-target normally 17% | cheap rows 4,739, spike-to-target normally 15% | — |

**All weeks:** cheap rows 14,088, spike-to-target normally 18%

**All months:** cheap rows 62,904, spike-to-target normally 18%
