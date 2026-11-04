# Kalshi commodity 15-min model report
Trained 2026-11-04 15:32 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 546

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| WTI | 426 windows · right 76% vs Kalshi 76% · logloss 0.4999 vs 0.4978 · edge bets 67: won 58%, ROI -4% | 2757 windows · right 76% vs Kalshi 76% · logloss 0.4962 vs 0.4958 · edge bets 93: won 56%, ROI -10% | — |
| BRENT | 427 windows · right 74% vs Kalshi 75% · logloss 0.5135 vs 0.5121 · edge bets 45: won 67%, ROI +8% | no data | — |
| NATGAS | 427 windows · right 74% vs Kalshi 73% · logloss 0.5084 vs 0.5066 · edge bets 10: won 40%, ROI -31% | 1924 windows · right 75% vs Kalshi 76% · logloss 0.4913 vs 0.4918 · edge bets 16: won 62%, ROI +2% | — |
| GOLD | 383 windows · right 75% vs Kalshi 76% · logloss 0.4896 vs 0.4862 · edge bets 30: won 47%, ROI -21% | 2694 windows · right 74% vs Kalshi 74% · logloss 0.5116 vs 0.5115 · edge bets 37: won 60%, ROI -4% | — |
| SILVER | 383 windows · right 74% vs Kalshi 73% · logloss 0.5146 vs 0.5157 · edge bets 13: won 85%, ROI +34% | 2685 windows · right 74% vs Kalshi 74% · logloss 0.5134 vs 0.5138 · edge bets 50: won 54%, ROI -12% | — |
| COPPER | 382 windows · right 77% vs Kalshi 77% · logloss 0.4642 vs 0.4682 · edge bets 6: won 100%, ROI +57% | 1852 windows · right 75% vs Kalshi 75% · logloss 0.5005 vs 0.5002 · edge bets 63: won 65%, ROI +12% | — |
| PLATINUM | 382 windows · right 72% vs Kalshi 72% · logloss 0.5355 vs 0.5353 · edge bets 12: won 83%, ROI +36% | 986 windows · right 75% vs Kalshi 75% · logloss 0.503 vs 0.5029 · edge bets 33: won 58%, ROI -0% | — |
| PALLADIUM | 383 windows · right 75% vs Kalshi 75% · logloss 0.5067 vs 0.5081 · edge bets 48: won 60%, ROI +2% | 631 windows · right 74% vs Kalshi 75% · logloss 0.5104 vs 0.5092 · edge bets 111: won 55%, ROI -4% | — |

**All weeks:** 3193 windows · right 75% vs Kalshi 74% · logloss 0.5042 vs 0.5038 · edge bets 231: won 62%, ROI +2%

**All months:** 13529 windows · right 75% vs Kalshi 75% · logloss 0.5037 vs 0.5037 · edge bets 403: won 58%, ROI -4%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4985 vs 0.4983 · edge bets 68: won 57%, ROI -7% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5086 vs 0.5083 · edge bets 173: won 58%, ROI -4% |
| 2026-10 | 3673 windows · right 75% vs Kalshi 75% · logloss 0.4991 vs 0.4996 · edge bets 162: won 57%, ROI -2% |

Strongest signals: `s_ASIA` -0.056, `dmid5` +0.050, `s_EU` +0.036, `ofi3` +0.029, `m_PALLADIUM` -0.026
