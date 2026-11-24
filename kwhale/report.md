# Kalshi commodity 15-min model report
Trained 2026-11-23 23:08 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 24975

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 401 windows · right 74% vs Kalshi 74% · logloss 0.5004 vs 0.5008 | 3530 windows · right 74% vs Kalshi 74% · logloss 0.505 vs 0.5045 | — |
| SILVER | 400 windows · right 76% vs Kalshi 76% · logloss 0.4928 vs 0.4918 · edge bets 1: won 0%, ROI -100% | 3515 windows · right 74% vs Kalshi 74% · logloss 0.5058 vs 0.5065 | — |
| WTI | 449 windows · right 74% vs Kalshi 75% · logloss 0.499 vs 0.502 | 3723 windows · right 75% vs Kalshi 75% · logloss 0.5073 vs 0.5074 | — |
| BRENT | 449 windows · right 77% vs Kalshi 76% · logloss 0.473 vs 0.475 · edge bets 4: won 50%, ROI -8% | 827 windows · right 74% vs Kalshi 75% · logloss 0.5083 vs 0.5077 · edge bets 5: won 60%, ROI +10% | — |
| COPPER | 400 windows · right 73% vs Kalshi 73% · logloss 0.5293 vs 0.5274 | 3032 windows · right 76% vs Kalshi 76% · logloss 0.4973 vs 0.4975 | — |
| NATGAS | 450 windows · right 76% vs Kalshi 75% · logloss 0.4931 vs 0.495 · edge bets 2: won 0%, ROI -100% | 3246 windows · right 75% vs Kalshi 75% · logloss 0.4989 vs 0.498 · edge bets 126: won 50%, ROI -8% | — |
| PALLADIUM | 401 windows · right 73% vs Kalshi 73% · logloss 0.5239 vs 0.5236 | 1811 windows · right 75% vs Kalshi 75% · logloss 0.5069 vs 0.5081 | — |
| PLATINUM | 401 windows · right 75% vs Kalshi 75% · logloss 0.5037 vs 0.504 | 2166 windows · right 75% vs Kalshi 75% · logloss 0.5048 vs 0.5056 | — |

**All weeks:** 3351 windows · right 75% vs Kalshi 75% · logloss 0.5012 vs 0.5019 · edge bets 7: won 29%, ROI -46%

**All months:** 21850 windows · right 75% vs Kalshi 75% · logloss 0.5038 vs 0.5039 · edge bets 131: won 50%, ROI -8%

| Month | Result |
|---|---|
| 2026-08 | 2072 windows · right 76% vs Kalshi 76% · logloss 0.4878 vs 0.488 · edge bets 1: won 0%, ROI -100% |
| 2026-09 | 6734 windows · right 75% vs Kalshi 74% · logloss 0.5083 vs 0.5083 · edge bets 31: won 48%, ROI -12% |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.5052 vs 0.5055 · edge bets 96: won 52%, ROI -5% |
| 2026-11 | 898 windows · right 76% vs Kalshi 76% · logloss 0.4872 vs 0.4857 · edge bets 3: won 33%, ROI -36% |

Strongest signals: `s_ASIA` -0.037, `s_EU` +0.027, `m_BRENT` +0.024, `ofi3` +0.024, `m_NATGAS` +0.023

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,670, target reached normally 20% | setups 14,399, target reached normally 19% | — |
| SILVER | setups 1,747, target reached normally 22% | setups 14,450, target reached normally 21% | — |
| WTI | setups 1,811, target reached normally 22% | setups 15,409, target reached normally 21% | — |
| BRENT | setups 2,110, target reached normally 18% | setups 3,519, target reached normally 14% | — |
| COPPER | setups 1,996, target reached normally 20% | setups 13,608, target reached normally 15% | — |
| NATGAS | setups 1,818, target reached normally 15% | setups 14,503, target reached normally 16% | — |
| PALLADIUM | setups 1,662, target reached normally 17% | setups 7,151, target reached normally 14% | — |
| PLATINUM | setups 2,033, target reached normally 19% | setups 8,765, target reached normally 15% | — |

**All weeks:** setups 14,847, target reached normally 19%

**All months:** setups 91,804, target reached normally 18%
