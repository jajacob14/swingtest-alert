# Kalshi commodity 15-min model report
Trained 2026-11-11 17:48 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 10320

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | 400 windows · right 75% vs Kalshi 76% · logloss 0.4989 vs 0.4988 · edge bets 6: won 50%, ROI -15% | 3145 windows · right 74% vs Kalshi 74% · logloss 0.5063 vs 0.5068 · edge bets 1: won 0%, ROI -100% | — |
| SILVER | 401 windows · right 76% vs Kalshi 77% · logloss 0.4886 vs 0.4893 | 3136 windows · right 74% vs Kalshi 74% · logloss 0.5105 vs 0.5114 · edge bets 12: won 67%, ROI +9% | — |
| WTI | 446 windows · right 76% vs Kalshi 77% · logloss 0.4751 vs 0.4741 · edge bets 6: won 17%, ROI -74% | 3262 windows · right 75% vs Kalshi 75% · logloss 0.5002 vs 0.5007 · edge bets 3: won 67%, ROI +1% | — |
| BRENT | 447 windows · right 76% vs Kalshi 76% · logloss 0.4823 vs 0.4814 · edge bets 2: won 100%, ROI +64% | 10 windows · right 78% vs Kalshi 76% · logloss 0.4418 vs 0.4509 | — |
| COPPER | 401 windows · right 77% vs Kalshi 78% · logloss 0.4694 vs 0.469 · edge bets 10: won 20%, ROI -62% | 2303 windows · right 75% vs Kalshi 75% · logloss 0.5056 vs 0.5056 · edge bets 13: won 38%, ROI -34% | — |
| NATGAS | 446 windows · right 75% vs Kalshi 75% · logloss 0.5039 vs 0.504 · edge bets 2: won 50%, ROI -17% | 2429 windows · right 75% vs Kalshi 75% · logloss 0.4979 vs 0.4982 · edge bets 1: won 100%, ROI +45% | — |
| PALLADIUM | 401 windows · right 78% vs Kalshi 78% · logloss 0.4605 vs 0.4595 · edge bets 21: won 43%, ROI -26% | 1082 windows · right 74% vs Kalshi 74% · logloss 0.5144 vs 0.5167 · edge bets 47: won 64%, ROI +13% | — |
| PLATINUM | 401 windows · right 76% vs Kalshi 76% · logloss 0.491 vs 0.4899 · edge bets 5: won 40%, ROI -29% | 1437 windows · right 75% vs Kalshi 75% · logloss 0.4997 vs 0.5008 · edge bets 20: won 60%, ROI +8% | — |

**All weeks:** 3343 windows · right 76% vs Kalshi 77% · logloss 0.4839 vs 0.4835 · edge bets 52: won 38%, ROI -34%

**All months:** 16804 windows · right 75% vs Kalshi 75% · logloss 0.5045 vs 0.5051 · edge bets 97: won 60%, ROI +4%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4978 vs 0.4983 · edge bets 5: won 60%, ROI -1% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5083 vs 0.5083 · edge bets 18: won 67%, ROI +11% |
| 2026-10 | 6948 windows · right 75% vs Kalshi 75% · logloss 0.5038 vs 0.5051 · edge bets 74: won 58%, ROI +2% |

Strongest signals: `s_ASIA` -0.050, `dmid5` +0.047, `s_EU` +0.035, `ofi3` +0.030, `spread` +0.022

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| GOLD | setups 1,680, target reached normally 24% | setups 13,097, target reached normally 19% | — |
| SILVER | setups 1,692, target reached normally 23% | setups 13,228, target reached normally 21% | — |
| WTI | setups 1,765, target reached normally 16% | setups 13,591, target reached normally 19% | — |
| BRENT | setups 2,058, target reached normally 16% | setups 36, target reached normally 8% | — |
| COPPER | setups 2,084, target reached normally 15% | setups 10,232, target reached normally 17% | — |
| NATGAS | setups 1,962, target reached normally 16% | setups 10,781, target reached normally 16% | — |
| PALLADIUM | setups 1,836, target reached normally 16% | setups 4,040, target reached normally 14% | — |
| PLATINUM | setups 1,763, target reached normally 18% | setups 5,891, target reached normally 15% | — |

**All weeks:** setups 14,840, target reached normally 18%

**All months:** setups 70,896, target reached normally 18%
