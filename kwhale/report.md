# Kalshi commodity 15-min model report
Trained 2026-11-09 08:13 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 5909

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 393 windows · right 76% vs Kalshi 76% · logloss 0.4932 vs 0.4941 · edge bets 16: won 56%, ROI -7% | 2929 windows · right 74% vs Kalshi 74% · logloss 0.5075 vs 0.5075 · edge bets 89: won 62%, ROI -1% | — |
| SILVER | 393 windows · right 75% vs Kalshi 76% · logloss 0.5029 vs 0.505 · edge bets 10: won 80%, ROI +28% | 2920 windows · right 74% vs Kalshi 74% · logloss 0.5129 vs 0.5134 · edge bets 71: won 52%, ROI -15% | — |
| WTI | 437 windows · right 76% vs Kalshi 76% · logloss 0.4866 vs 0.4879 · edge bets 6: won 67%, ROI -4% | 3031 windows · right 75% vs Kalshi 75% · logloss 0.4993 vs 0.5 · edge bets 66: won 53%, ROI -14% | — |
| BRENT | 437 windows · right 78% vs Kalshi 78% · logloss 0.4732 vs 0.4747 · edge bets 5: won 60%, ROI -2% | no data | — |
| COPPER | 393 windows · right 78% vs Kalshi 78% · logloss 0.4461 vs 0.4485 | 2087 windows · right 75% vs Kalshi 75% · logloss 0.5017 vs 0.5012 · edge bets 120: won 65%, ROI +10% | — |
| NATGAS | 437 windows · right 76% vs Kalshi 76% · logloss 0.488 vs 0.4878 · edge bets 24: won 50%, ROI -12% | 2198 windows · right 75% vs Kalshi 75% · logloss 0.4985 vs 0.4981 · edge bets 68: won 56%, ROI -6% | — |
| PALLADIUM | 393 windows · right 77% vs Kalshi 77% · logloss 0.4642 vs 0.4644 · edge bets 42: won 62%, ROI +5% | 866 windows · right 74% vs Kalshi 74% · logloss 0.5188 vs 0.5205 · edge bets 99: won 61%, ROI +6% | ✅ |
| PLATINUM | 392 windows · right 74% vs Kalshi 74% · logloss 0.5083 vs 0.5089 · edge bets 6: won 83%, ROI +45% | 1221 windows · right 75% vs Kalshi 75% · logloss 0.5004 vs 0.5008 · edge bets 100: won 55%, ROI -6% | — |

**All weeks:** 3275 windows · right 76% vs Kalshi 76% · logloss 0.4827 vs 0.4838 · edge bets 109: won 62%, ROI +3%

**All months:** 15252 windows · right 75% vs Kalshi 75% · logloss 0.5049 vs 0.5051 · edge bets 613: won 58%, ROI -2%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4981 vs 0.4983 · edge bets 71: won 49%, ROI -20% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5086 vs 0.5083 · edge bets 225: won 57%, ROI -5% |
| 2026-10 | 5396 windows · right 75% vs Kalshi 75% · logloss 0.5042 vs 0.5051 · edge bets 317: won 61%, ROI +4% |

Strongest signals: `s_ASIA` -0.058, `dmid5` +0.054, `s_EU` +0.044, `ofi3` +0.040, `bigc` -0.024

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,590, target reached normally 23% | setups 12,205, target reached normally 19% | — |
| SILVER | setups 1,623, target reached normally 25% | setups 12,317, target reached normally 21% | — |
| WTI | setups 1,702, target reached normally 18% | setups 12,644, target reached normally 19% | — |
| BRENT | setups 1,952, target reached normally 16% | no data | — |
| COPPER | setups 2,003, target reached normally 14% | setups 9,368, target reached normally 16% | — |
| NATGAS | setups 1,903, target reached normally 17% | setups 9,892, target reached normally 16% | — |
| PALLADIUM | setups 1,805, target reached normally 15% | setups 3,174, target reached normally 14% | — |
| PLATINUM | setups 1,756, target reached normally 17% | setups 5,005, target reached normally 15% | — |

**All weeks:** setups 14,334, target reached normally 18%

**All months:** setups 64,605, target reached normally 18%
