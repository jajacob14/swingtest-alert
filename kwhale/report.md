# Kalshi commodity 15-min model report
Trained 2026-11-07 21:24 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 4820

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 390 windows · right 74% vs Kalshi 75% · logloss 0.5089 vs 0.5091 · edge bets 17: won 53%, ROI -15% | 2870 windows · right 74% vs Kalshi 74% · logloss 0.5093 vs 0.5095 · edge bets 59: won 54%, ROI -14% | — |
| SILVER | 390 windows · right 74% vs Kalshi 74% · logloss 0.5155 vs 0.5156 · edge bets 11: won 73%, ROI +16% | 2861 windows · right 74% vs Kalshi 74% · logloss 0.5136 vs 0.5139 · edge bets 53: won 58%, ROI -4% | — |
| WTI | 439 windows · right 76% vs Kalshi 76% · logloss 0.4979 vs 0.4988 · edge bets 8: won 62%, ROI -8% | 2971 windows · right 75% vs Kalshi 75% · logloss 0.4979 vs 0.4985 · edge bets 50: won 54%, ROI -12% | — |
| BRENT | 438 windows · right 77% vs Kalshi 78% · logloss 0.4824 vs 0.4831 · edge bets 9: won 67%, ROI +5% | no data | — |
| COPPER | 391 windows · right 77% vs Kalshi 77% · logloss 0.4677 vs 0.4688 · edge bets 1: won 100%, ROI +96% | 2028 windows · right 75% vs Kalshi 75% · logloss 0.4996 vs 0.4997 · edge bets 48: won 65%, ROI +8% | — |
| NATGAS | 438 windows · right 76% vs Kalshi 76% · logloss 0.4849 vs 0.4855 · edge bets 7: won 14%, ROI -76% | 2138 windows · right 75% vs Kalshi 75% · logloss 0.4976 vs 0.4976 · edge bets 21: won 71%, ROI +16% | — |
| PALLADIUM | 391 windows · right 76% vs Kalshi 76% · logloss 0.4777 vs 0.4778 · edge bets 42: won 64%, ROI +10% | 807 windows · right 74% vs Kalshi 74% · logloss 0.5145 vs 0.5159 · edge bets 93: won 58%, ROI +2% | ✅ |
| PLATINUM | 390 windows · right 74% vs Kalshi 74% · logloss 0.5163 vs 0.5164 · edge bets 5: won 80%, ROI +36% | 1162 windows · right 75% vs Kalshi 75% · logloss 0.5042 vs 0.505 · edge bets 40: won 68%, ROI +15% | — |

**All weeks:** 3267 windows · right 76% vs Kalshi 76% · logloss 0.4935 vs 0.494 · edge bets 100: won 61%, ROI +0%

**All months:** 14837 windows · right 75% vs Kalshi 75% · logloss 0.5047 vs 0.5051 · edge bets 364: won 60%, ROI -0%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4981 vs 0.4983 · edge bets 53: won 57%, ROI -9% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5084 vs 0.5083 · edge bets 130: won 57%, ROI -6% |
| 2026-10 | 4981 windows · right 75% vs Kalshi 75% · logloss 0.5038 vs 0.505 · edge bets 181: won 62%, ROI +6% |

Strongest signals: `s_ASIA` -0.054, `dmid5` +0.054, `s_EU` +0.037, `ofi3` +0.033, `bigc` -0.030

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,565, target reached normally 23% | setups 11,971, target reached normally 19% | — |
| SILVER | setups 1,625, target reached normally 23% | setups 12,083, target reached normally 21% | — |
| WTI | setups 1,680, target reached normally 19% | setups 12,411, target reached normally 19% | — |
| BRENT | setups 1,934, target reached normally 17% | no data | — |
| COPPER | setups 1,960, target reached normally 14% | setups 9,129, target reached normally 17% | — |
| NATGAS | setups 1,874, target reached normally 16% | setups 9,656, target reached normally 16% | — |
| PALLADIUM | setups 1,772, target reached normally 16% | setups 2,930, target reached normally 14% | — |
| PLATINUM | setups 1,722, target reached normally 17% | setups 4,739, target reached normally 15% | — |

**All weeks:** setups 14,132, target reached normally 18%

**All months:** setups 62,919, target reached normally 18%
