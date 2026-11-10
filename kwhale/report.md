# Kalshi commodity 15-min model report
Trained 2026-11-10 07:16 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 7707

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 396 windows · right 76% vs Kalshi 76% · logloss 0.4851 vs 0.4861 · edge bets 20: won 65%, ROI +7% | 3017 windows · right 74% vs Kalshi 74% · logloss 0.507 vs 0.507 · edge bets 69: won 54%, ROI -14% | — |
| SILVER | 396 windows · right 76% vs Kalshi 76% · logloss 0.4993 vs 0.5009 · edge bets 11: won 64%, ROI +11% | 3008 windows · right 74% vs Kalshi 74% · logloss 0.5103 vs 0.5109 · edge bets 61: won 52%, ROI -14% | — |
| WTI | 440 windows · right 74% vs Kalshi 75% · logloss 0.4966 vs 0.4963 · edge bets 17: won 53%, ROI -17% | 3124 windows · right 75% vs Kalshi 75% · logloss 0.4981 vs 0.4988 · edge bets 50: won 50%, ROI -17% | — |
| BRENT | 440 windows · right 76% vs Kalshi 76% · logloss 0.4909 vs 0.4893 · edge bets 6: won 100%, ROI +69% | no data | — |
| COPPER | 396 windows · right 78% vs Kalshi 79% · logloss 0.4516 vs 0.4517 · edge bets 14: won 50%, ROI -11% | 2175 windows · right 75% vs Kalshi 75% · logloss 0.5045 vs 0.5037 · edge bets 168: won 62%, ROI +8% | — |
| NATGAS | 440 windows · right 75% vs Kalshi 75% · logloss 0.5001 vs 0.5008 · edge bets 22: won 46%, ROI -19% | 2291 windows · right 75% vs Kalshi 75% · logloss 0.4982 vs 0.498 · edge bets 51: won 57%, ROI -2% | — |
| PALLADIUM | 397 windows · right 78% vs Kalshi 79% · logloss 0.4524 vs 0.4517 · edge bets 75: won 57%, ROI +2% | 954 windows · right 75% vs Kalshi 74% · logloss 0.5136 vs 0.5149 · edge bets 112: won 56%, ROI -0% | — |
| PLATINUM | 396 windows · right 74% vs Kalshi 75% · logloss 0.5068 vs 0.5066 · edge bets 57: won 53%, ROI -6% | 1309 windows · right 75% vs Kalshi 75% · logloss 0.4994 vs 0.4999 · edge bets 129: won 57%, ROI -4% | — |

**All weeks:** 3301 windows · right 76% vs Kalshi 76% · logloss 0.4858 vs 0.4858 · edge bets 222: won 56%, ROI -2%

**All months:** 15878 windows · right 75% vs Kalshi 75% · logloss 0.504 vs 0.5043 · edge bets 640: won 57%, ROI -3%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4981 vs 0.4983 · edge bets 62: won 52%, ROI -14% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5085 vs 0.5083 · edge bets 218: won 56%, ROI -5% |
| 2026-10 | 6022 windows · right 75% vs Kalshi 75% · logloss 0.5021 vs 0.5028 · edge bets 360: won 58%, ROI -0% |

Strongest signals: `s_ASIA` -0.056, `dmid5` +0.049, `s_EU` +0.041, `ofi3` +0.036, `spread` +0.025

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,642, target reached normally 22% | setups 12,598, target reached normally 19% | — |
| SILVER | setups 1,629, target reached normally 24% | setups 12,711, target reached normally 21% | — |
| WTI | setups 1,669, target reached normally 18% | setups 13,052, target reached normally 19% | — |
| BRENT | setups 1,981, target reached normally 17% | no data | — |
| COPPER | setups 2,120, target reached normally 13% | setups 9,724, target reached normally 17% | — |
| NATGAS | setups 1,895, target reached normally 16% | setups 10,235, target reached normally 16% | — |
| PALLADIUM | setups 1,821, target reached normally 14% | setups 3,553, target reached normally 14% | — |
| PLATINUM | setups 1,750, target reached normally 16% | setups 5,367, target reached normally 15% | — |

**All weeks:** setups 14,507, target reached normally 17%

**All months:** setups 67,240, target reached normally 18%
