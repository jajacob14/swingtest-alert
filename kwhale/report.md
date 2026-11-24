# Kalshi commodity 15-min model report
Trained 2026-11-24 10:34 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 25705

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 403 windows · right 74% vs Kalshi 75% · logloss 0.4992 vs 0.499 | 3576 windows · right 74% vs Kalshi 74% · logloss 0.5056 vs 0.5052 | — |
| SILVER | 402 windows · right 76% vs Kalshi 76% · logloss 0.4876 vs 0.4857 | 3561 windows · right 74% vs Kalshi 74% · logloss 0.5055 vs 0.5063 | — |
| WTI | 447 windows · right 75% vs Kalshi 75% · logloss 0.4959 vs 0.4973 | 3769 windows · right 75% vs Kalshi 75% · logloss 0.5067 vs 0.5069 | — |
| BRENT | 447 windows · right 76% vs Kalshi 76% · logloss 0.4782 vs 0.4788 · edge bets 4: won 50%, ROI -7% | 873 windows · right 75% vs Kalshi 75% · logloss 0.5022 vs 0.5021 | — |
| COPPER | 402 windows · right 73% vs Kalshi 73% · logloss 0.5226 vs 0.5212 | 3078 windows · right 76% vs Kalshi 76% · logloss 0.4967 vs 0.4971 | — |
| NATGAS | 446 windows · right 75% vs Kalshi 75% · logloss 0.4887 vs 0.4923 · edge bets 2: won 50%, ROI -6% | 3292 windows · right 75% vs Kalshi 75% · logloss 0.4989 vs 0.4978 · edge bets 28: won 43%, ROI -21% | — |
| PALLADIUM | 402 windows · right 73% vs Kalshi 73% · logloss 0.527 vs 0.5255 | 1857 windows · right 75% vs Kalshi 74% · logloss 0.5089 vs 0.5101 | — |
| PLATINUM | 402 windows · right 75% vs Kalshi 75% · logloss 0.5023 vs 0.5021 | 2212 windows · right 75% vs Kalshi 75% · logloss 0.5052 vs 0.5061 | — |

**All weeks:** 3351 windows · right 75% vs Kalshi 75% · logloss 0.4997 vs 0.4998 · edge bets 6: won 50%, ROI -7%

**All months:** 22218 windows · right 75% vs Kalshi 75% · logloss 0.5036 vs 0.5038 · edge bets 28: won 43%, ROI -21%

| Month | Result |
|---|---|
| 2026-08 | 2072 windows · right 76% vs Kalshi 76% · logloss 0.4879 vs 0.488 |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5082 vs 0.5083 · edge bets 6: won 17%, ROI -70% |
| 2026-10 | 12146 windows · right 75% vs Kalshi 75% · logloss 0.5052 vs 0.5055 · edge bets 21: won 52%, ROI -3% |
| 2026-11 | 1266 windows · right 76% vs Kalshi 76% · logloss 0.4888 vs 0.4891 · edge bets 1: won 0%, ROI -100% |

Strongest signals: `s_ASIA` -0.037, `m_NATGAS` +0.028, `s_EU` +0.024, `tleft` -0.023, `ofi3` +0.022

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,676, target reached normally 20% | setups 14,589, target reached normally 19% | — |
| SILVER | setups 1,744, target reached normally 21% | setups 14,652, target reached normally 21% | — |
| WTI | setups 1,827, target reached normally 22% | setups 15,609, target reached normally 20% | — |
| BRENT | setups 2,119, target reached normally 18% | setups 3,734, target reached normally 14% | — |
| COPPER | setups 1,998, target reached normally 20% | setups 13,823, target reached normally 16% | — |
| NATGAS | setups 1,873, target reached normally 15% | setups 14,742, target reached normally 16% | — |
| PALLADIUM | setups 1,648, target reached normally 17% | setups 7,381, target reached normally 14% | — |
| PLATINUM | setups 1,980, target reached normally 18% | setups 8,969, target reached normally 15% | — |

**All weeks:** setups 14,865, target reached normally 19%

**All months:** setups 93,499, target reached normally 18%
