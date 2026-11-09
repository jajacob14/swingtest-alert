# Kalshi commodity 15-min model report
Trained 2026-11-08 20:27 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 4930

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 390 windows · right 74% vs Kalshi 75% · logloss 0.5083 vs 0.5085 · edge bets 16: won 50%, ROI -19% | 2882 windows · right 74% vs Kalshi 74% · logloss 0.5088 vs 0.509 · edge bets 65: won 55%, ROI -11% | — |
| SILVER | 390 windows · right 74% vs Kalshi 75% · logloss 0.5138 vs 0.5141 · edge bets 11: won 73%, ROI +18% | 2873 windows · right 74% vs Kalshi 74% · logloss 0.5143 vs 0.5147 · edge bets 49: won 57%, ROI -6% | — |
| WTI | 438 windows · right 76% vs Kalshi 76% · logloss 0.4906 vs 0.492 · edge bets 8: won 62%, ROI -3% | 2984 windows · right 75% vs Kalshi 75% · logloss 0.4979 vs 0.4985 · edge bets 60: won 55%, ROI -11% | — |
| BRENT | 438 windows · right 78% vs Kalshi 78% · logloss 0.4791 vs 0.4803 · edge bets 5: won 60%, ROI -2% | no data | — |
| COPPER | 389 windows · right 77% vs Kalshi 78% · logloss 0.4649 vs 0.4658 | 2040 windows · right 75% vs Kalshi 75% · logloss 0.5007 vs 0.5004 · edge bets 95: won 66%, ROI +13% | — |
| NATGAS | 438 windows · right 76% vs Kalshi 75% · logloss 0.4883 vs 0.4889 · edge bets 9: won 22%, ROI -62% | 2151 windows · right 75% vs Kalshi 75% · logloss 0.4973 vs 0.4973 · edge bets 27: won 74%, ROI +23% | — |
| PALLADIUM | 389 windows · right 77% vs Kalshi 76% · logloss 0.4766 vs 0.4771 · edge bets 41: won 63%, ROI +7% | 819 windows · right 74% vs Kalshi 74% · logloss 0.519 vs 0.5205 · edge bets 88: won 60%, ROI +6% | ✅ |
| PLATINUM | 389 windows · right 73% vs Kalshi 73% · logloss 0.5157 vs 0.5153 · edge bets 5: won 80%, ROI +36% | 1174 windows · right 75% vs Kalshi 75% · logloss 0.5026 vs 0.5033 · edge bets 56: won 62%, ROI +6% | — |

**All weeks:** 3261 windows · right 76% vs Kalshi 76% · logloss 0.4917 vs 0.4923 · edge bets 95: won 59%, ROI -2%

**All months:** 14923 windows · right 75% vs Kalshi 75% · logloss 0.505 vs 0.5053 · edge bets 440: won 61%, ROI +2%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4981 vs 0.4983 · edge bets 54: won 56%, ROI -10% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5085 vs 0.5083 · edge bets 163: won 60%, ROI -1% |
| 2026-10 | 5067 windows · right 75% vs Kalshi 75% · logloss 0.5045 vs 0.5056 · edge bets 223: won 63%, ROI +7% |

Strongest signals: `s_ASIA` -0.053, `dmid5` +0.053, `s_EU` +0.036, `ofi3` +0.034, `bigc` -0.031

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,571, target reached normally 24% | setups 12,022, target reached normally 19% | — |
| SILVER | setups 1,620, target reached normally 23% | setups 12,129, target reached normally 21% | — |
| WTI | setups 1,698, target reached normally 19% | setups 12,470, target reached normally 19% | — |
| BRENT | setups 1,917, target reached normally 17% | no data | — |
| COPPER | setups 1,970, target reached normally 14% | setups 9,172, target reached normally 17% | — |
| NATGAS | setups 1,885, target reached normally 16% | setups 9,731, target reached normally 16% | — |
| PALLADIUM | setups 1,779, target reached normally 16% | setups 2,979, target reached normally 14% | — |
| PLATINUM | setups 1,730, target reached normally 16% | setups 4,794, target reached normally 15% | — |

**All weeks:** setups 14,170, target reached normally 18%

**All months:** setups 63,297, target reached normally 18%
