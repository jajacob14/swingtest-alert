# Kalshi commodity 15-min model report
Trained 2026-11-09 19:44 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 6883

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 392 windows · right 77% vs Kalshi 77% · logloss 0.4783 vs 0.4791 · edge bets 15: won 53%, ROI -13% | 2970 windows · right 74% vs Kalshi 74% · logloss 0.5078 vs 0.5079 · edge bets 63: won 59%, ROI -6% | — |
| SILVER | 393 windows · right 75% vs Kalshi 75% · logloss 0.5062 vs 0.5078 · edge bets 10: won 70%, ROI +11% | 2961 windows · right 74% vs Kalshi 74% · logloss 0.5114 vs 0.512 · edge bets 53: won 55%, ROI -11% | — |
| WTI | 442 windows · right 75% vs Kalshi 75% · logloss 0.4965 vs 0.4974 · edge bets 8: won 50%, ROI -29% | 3077 windows · right 75% vs Kalshi 75% · logloss 0.4988 vs 0.4994 · edge bets 60: won 48%, ROI -20% | — |
| BRENT | 442 windows · right 76% vs Kalshi 76% · logloss 0.4897 vs 0.4896 · edge bets 3: won 100%, ROI +60% | no data | — |
| COPPER | 393 windows · right 78% vs Kalshi 79% · logloss 0.4509 vs 0.4522 · edge bets 3: won 67%, ROI +15% | 2128 windows · right 75% vs Kalshi 75% · logloss 0.5017 vs 0.5013 · edge bets 152: won 64%, ROI +10% | — |
| NATGAS | 441 windows · right 76% vs Kalshi 75% · logloss 0.4901 vs 0.4916 · edge bets 12: won 42%, ROI -26% | 2244 windows · right 75% vs Kalshi 75% · logloss 0.4986 vs 0.4984 · edge bets 35: won 63%, ROI +5% | — |
| PALLADIUM | 393 windows · right 79% vs Kalshi 79% · logloss 0.4469 vs 0.4472 · edge bets 46: won 59%, ROI +3% | 907 windows · right 74% vs Kalshi 74% · logloss 0.5146 vs 0.5162 · edge bets 95: won 58%, ROI +1% | ✅ |
| PLATINUM | 393 windows · right 75% vs Kalshi 75% · logloss 0.4944 vs 0.4953 · edge bets 11: won 55%, ROI -2% | 1262 windows · right 75% vs Kalshi 75% · logloss 0.5008 vs 0.5015 · edge bets 103: won 55%, ROI -6% | — |

**All weeks:** 3289 windows · right 76% vs Kalshi 76% · logloss 0.4821 vs 0.483 · edge bets 108: won 57%, ROI -3%

**All months:** 15549 windows · right 75% vs Kalshi 75% · logloss 0.5044 vs 0.5047 · edge bets 561: won 58%, ROI -2%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4981 vs 0.4983 · edge bets 61: won 51%, ROI -17% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5085 vs 0.5083 · edge bets 199: won 59%, ROI -1% |
| 2026-10 | 5693 windows · right 75% vs Kalshi 75% · logloss 0.5029 vs 0.5039 · edge bets 301: won 59%, ROI +0% |

Strongest signals: `s_ASIA` -0.058, `dmid5` +0.050, `s_EU` +0.042, `ofi3` +0.038, `spread` +0.024

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,584, target reached normally 23% | setups 12,395, target reached normally 19% | — |
| SILVER | setups 1,610, target reached normally 25% | setups 12,508, target reached normally 21% | — |
| WTI | setups 1,693, target reached normally 18% | setups 12,856, target reached normally 19% | — |
| BRENT | setups 1,985, target reached normally 16% | no data | — |
| COPPER | setups 2,046, target reached normally 13% | setups 9,540, target reached normally 16% | — |
| NATGAS | setups 1,877, target reached normally 15% | setups 10,061, target reached normally 16% | — |
| PALLADIUM | setups 1,793, target reached normally 15% | setups 3,335, target reached normally 14% | — |
| PLATINUM | setups 1,754, target reached normally 16% | setups 5,156, target reached normally 15% | — |

**All weeks:** setups 14,342, target reached normally 17%

**All months:** setups 65,851, target reached normally 18%
