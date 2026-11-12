# Kalshi commodity 15-min model report
Trained 2026-11-12 05:19 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 11003

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 400 windows · right 76% vs Kalshi 76% · logloss 0.4909 vs 0.4917 · edge bets 4: won 50%, ROI -11% | 3183 windows · right 74% vs Kalshi 74% · logloss 0.5066 vs 0.507 · edge bets 2: won 0%, ROI -100% | — |
| SILVER | 400 windows · right 76% vs Kalshi 76% · logloss 0.4928 vs 0.4925 · edge bets 1: won 100%, ROI +52% | 3174 windows · right 74% vs Kalshi 74% · logloss 0.5093 vs 0.5104 · edge bets 5: won 60%, ROI +1% | — |
| WTI | 447 windows · right 77% vs Kalshi 77% · logloss 0.4709 vs 0.4697 · edge bets 4: won 0%, ROI -100% | 3300 windows · right 75% vs Kalshi 75% · logloss 0.5006 vs 0.5012 · edge bets 3: won 67%, ROI +12% | — |
| BRENT | 447 windows · right 78% vs Kalshi 78% · logloss 0.4684 vs 0.4674 | 48 windows · right 81% vs Kalshi 81% · logloss 0.4236 vs 0.4228 | — |
| COPPER | 400 windows · right 77% vs Kalshi 78% · logloss 0.4744 vs 0.4747 · edge bets 6: won 0%, ROI -100% | 2341 windows · right 75% vs Kalshi 75% · logloss 0.5034 vs 0.5038 · edge bets 1: won 0%, ROI -100% | — |
| NATGAS | 447 windows · right 75% vs Kalshi 75% · logloss 0.5062 vs 0.5055 · edge bets 4: won 50%, ROI -23% | 2467 windows · right 75% vs Kalshi 75% · logloss 0.4973 vs 0.4975 · edge bets 1: won 100%, ROI +89% | — |
| PALLADIUM | 400 windows · right 78% vs Kalshi 78% · logloss 0.4659 vs 0.4662 · edge bets 16: won 38%, ROI -35% | 1120 windows · right 74% vs Kalshi 74% · logloss 0.5128 vs 0.5156 · edge bets 37: won 62%, ROI +12% | — |
| PLATINUM | 400 windows · right 76% vs Kalshi 76% · logloss 0.4917 vs 0.4904 · edge bets 8: won 62%, ROI +8% | 1475 windows · right 75% vs Kalshi 75% · logloss 0.5003 vs 0.5018 · edge bets 6: won 83%, ROI +55% | — |

**All weeks:** 3341 windows · right 76% vs Kalshi 77% · logloss 0.4826 vs 0.4822 · edge bets 43: won 37%, ROI -36%

**All months:** 17108 windows · right 75% vs Kalshi 75% · logloss 0.5038 vs 0.5046 · edge bets 55: won 62%, ROI +10%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4978 vs 0.4983 · edge bets 6: won 33%, ROI -40% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5082 vs 0.5083 · edge bets 11: won 73%, ROI +24% |
| 2026-10 | 7252 windows · right 75% vs Kalshi 75% · logloss 0.5023 vs 0.5038 · edge bets 38: won 63%, ROI +14% |

Strongest signals: `s_ASIA` -0.053, `dmid5` +0.042, `s_EU` +0.036, `ofi3` +0.027, `s_US` +0.022

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,700, target reached normally 24% | setups 13,257, target reached normally 19% | — |
| SILVER | setups 1,668, target reached normally 23% | setups 13,394, target reached normally 21% | — |
| WTI | setups 1,802, target reached normally 15% | setups 13,752, target reached normally 19% | — |
| BRENT | setups 2,112, target reached normally 14% | setups 206, target reached normally 14% | — |
| COPPER | setups 2,062, target reached normally 16% | setups 10,408, target reached normally 16% | — |
| NATGAS | setups 1,945, target reached normally 16% | setups 10,961, target reached normally 16% | — |
| PALLADIUM | setups 1,852, target reached normally 16% | setups 4,172, target reached normally 14% | — |
| PLATINUM | setups 1,786, target reached normally 18% | setups 6,032, target reached normally 15% | — |

**All weeks:** setups 14,927, target reached normally 17%

**All months:** setups 72,182, target reached normally 18%
