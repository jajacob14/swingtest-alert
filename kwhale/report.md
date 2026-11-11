# Kalshi commodity 15-min model report
Trained 2026-11-10 18:46 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 8596

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 396 windows · right 76% vs Kalshi 76% · logloss 0.4913 vs 0.4919 · edge bets 17: won 59%, ROI -2% | 3058 windows · right 74% vs Kalshi 74% · logloss 0.5062 vs 0.5064 · edge bets 69: won 51%, ROI -17% | — |
| SILVER | 396 windows · right 76% vs Kalshi 76% · logloss 0.4887 vs 0.4909 · edge bets 12: won 67%, ROI +15% | 3049 windows · right 74% vs Kalshi 74% · logloss 0.5102 vs 0.5109 · edge bets 43: won 49%, ROI -20% | — |
| WTI | 444 windows · right 75% vs Kalshi 75% · logloss 0.4951 vs 0.4954 · edge bets 15: won 47%, ROI -28% | 3170 windows · right 75% vs Kalshi 75% · logloss 0.4984 vs 0.4993 · edge bets 43: won 49%, ROI -20% | — |
| BRENT | 445 windows · right 75% vs Kalshi 76% · logloss 0.4993 vs 0.4979 · edge bets 2: won 100%, ROI +71% | no data | — |
| COPPER | 396 windows · right 79% vs Kalshi 79% · logloss 0.4473 vs 0.4493 · edge bets 3: won 0%, ROI -100% | 2216 windows · right 75% vs Kalshi 75% · logloss 0.5038 vs 0.5036 · edge bets 46: won 61%, ROI +3% | — |
| NATGAS | 445 windows · right 75% vs Kalshi 75% · logloss 0.5017 vs 0.5028 · edge bets 4: won 0%, ROI -100% | 2337 windows · right 75% vs Kalshi 75% · logloss 0.4977 vs 0.4975 · edge bets 43: won 63%, ROI +8% | — |
| PALLADIUM | 396 windows · right 79% vs Kalshi 79% · logloss 0.4536 vs 0.4537 · edge bets 40: won 60%, ROI +4% | 995 windows · right 74% vs Kalshi 74% · logloss 0.5133 vs 0.5147 · edge bets 106: won 58%, ROI +3% | ✅ |
| PLATINUM | 397 windows · right 74% vs Kalshi 74% · logloss 0.5112 vs 0.5116 · edge bets 32: won 53%, ROI -3% | 1350 windows · right 75% vs Kalshi 75% · logloss 0.4978 vs 0.4986 · edge bets 80: won 59%, ROI +1% | — |

**All weeks:** 3315 windows · right 76% vs Kalshi 76% · logloss 0.4867 vs 0.4873 · edge bets 125: won 54%, ROI -6%

**All months:** 16175 windows · right 75% vs Kalshi 75% · logloss 0.5036 vs 0.504 · edge bets 430: won 56%, ROI -5%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.498 vs 0.4983 · edge bets 43: won 49%, ROI -20% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5083 vs 0.5083 · edge bets 135: won 56%, ROI -5% |
| 2026-10 | 6319 windows · right 75% vs Kalshi 75% · logloss 0.5013 vs 0.5023 · edge bets 252: won 57%, ROI -2% |

Strongest signals: `s_ASIA` -0.057, `dmid5` +0.048, `ofi3` +0.034, `s_EU` +0.034, `s_US` +0.028

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,654, target reached normally 24% | setups 12,782, target reached normally 19% | — |
| SILVER | setups 1,618, target reached normally 24% | setups 12,887, target reached normally 21% | — |
| WTI | setups 1,659, target reached normally 18% | setups 13,219, target reached normally 19% | — |
| BRENT | setups 1,981, target reached normally 17% | no data | — |
| COPPER | setups 2,125, target reached normally 14% | setups 9,888, target reached normally 17% | — |
| NATGAS | setups 1,916, target reached normally 16% | setups 10,420, target reached normally 16% | — |
| PALLADIUM | setups 1,811, target reached normally 16% | setups 3,716, target reached normally 14% | — |
| PLATINUM | setups 1,752, target reached normally 18% | setups 5,545, target reached normally 15% | — |

**All weeks:** setups 14,516, target reached normally 18%

**All months:** setups 68,457, target reached normally 18%
