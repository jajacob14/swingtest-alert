# Kalshi commodity 15-min model report
Trained 2026-11-04 08:51 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 100% of rows · commodity whale events on file: 0

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| WTI | 423 windows · right 75% vs Kalshi 75% · logloss 0.5067 vs 0.5062 · edge bets 48: won 58%, ROI -2% | 2730 windows · right 76% vs Kalshi 76% · logloss 0.4951 vs 0.4951 · edge bets 69: won 54%, ROI -15% | — |
| BRENT | 424 windows · right 74% vs Kalshi 75% · logloss 0.5095 vs 0.5082 · edge bets 54: won 67%, ROI +8% | no data | — |
| NATGAS | 424 windows · right 73% vs Kalshi 72% · logloss 0.5115 vs 0.5095 · edge bets 14: won 36%, ROI -40% | 1897 windows · right 75% vs Kalshi 75% · logloss 0.4919 vs 0.4923 · edge bets 16: won 69%, ROI +13% | — |
| GOLD | 380 windows · right 75% vs Kalshi 76% · logloss 0.4879 vs 0.4837 · edge bets 41: won 46%, ROI -21% | 2667 windows · right 74% vs Kalshi 74% · logloss 0.5118 vs 0.5116 · edge bets 48: won 58%, ROI -8% | — |
| SILVER | 381 windows · right 74% vs Kalshi 74% · logloss 0.5145 vs 0.5154 · edge bets 23: won 65%, ROI +6% | 2658 windows · right 74% vs Kalshi 74% · logloss 0.5139 vs 0.5142 · edge bets 57: won 56%, ROI -8% | — |
| COPPER | 381 windows · right 78% vs Kalshi 77% · logloss 0.466 vs 0.4698 · edge bets 9: won 78%, ROI +20% | 1825 windows · right 75% vs Kalshi 75% · logloss 0.5014 vs 0.5011 · edge bets 95: won 63%, ROI +10% | — |
| PLATINUM | 382 windows · right 73% vs Kalshi 72% · logloss 0.5294 vs 0.5288 · edge bets 13: won 85%, ROI +36% | 959 windows · right 75% vs Kalshi 75% · logloss 0.5025 vs 0.5024 · edge bets 37: won 54%, ROI -6% | — |
| PALLADIUM | 383 windows · right 75% vs Kalshi 75% · logloss 0.5079 vs 0.5076 · edge bets 74: won 64%, ROI +10% | 604 windows · right 74% vs Kalshi 75% · logloss 0.5118 vs 0.5102 · edge bets 114: won 55%, ROI -4% | — |

**All weeks:** 3178 windows · right 75% vs Kalshi 74% · logloss 0.5044 vs 0.5039 · edge bets 276: won 61%, ROI +2%

**All months:** 13340 windows · right 75% vs Kalshi 75% · logloss 0.5038 vs 0.5038 · edge bets 436: won 58%, ROI -3%

| Month | Result |
|---|---|
| 2026-08 | 3122 windows · right 75% vs Kalshi 75% · logloss 0.4985 vs 0.4983 · edge bets 65: won 57%, ROI -8% |
| 2026-09 | 6734 windows · right 74% vs Kalshi 74% · logloss 0.5086 vs 0.5083 · edge bets 198: won 57%, ROI -5% |
| 2026-10 | 3484 windows · right 75% vs Kalshi 75% · logloss 0.4994 vs 0.5 · edge bets 173: won 59%, ROI +1% |

Strongest signals: `s_ASIA` -0.056, `dmid5` +0.049, `s_EU` +0.034, `ofi3` +0.031, `s_US` +0.027
