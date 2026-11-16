# Kalshi crypto 15-min model report
Trained 2026-11-16 00:22 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 170420

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 75% vs Kalshi 75% · logloss 0.5013 vs 0.5022 · edge bets 3: won 0%, ROI -100% | 2756 windows · right 75% vs Kalshi 75% · logloss 0.4988 vs 0.4986 · edge bets 21: won 57%, ROI -3% | — |
| ETH | 598 windows · right 75% vs Kalshi 75% · logloss 0.5107 vs 0.5103 · edge bets 1: won 100%, ROI +117% | 2602 windows · right 77% vs Kalshi 77% · logloss 0.4715 vs 0.471 · edge bets 6: won 17%, ROI -71% | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.4889 vs 0.4911 · edge bets 2: won 50%, ROI -2% | 2602 windows · right 76% vs Kalshi 76% · logloss 0.4841 vs 0.4842 · edge bets 3: won 100%, ROI +91% | — |
| XRP | 598 windows · right 77% vs Kalshi 77% · logloss 0.4866 vs 0.4861 · edge bets 14: won 43%, ROI -21% | 2599 windows · right 76% vs Kalshi 77% · logloss 0.4752 vs 0.4759 · edge bets 31: won 55%, ROI -0% | — |
| DOGE | 597 windows · right 74% vs Kalshi 74% · logloss 0.5065 vs 0.5084 · edge bets 5: won 80%, ROI +30% | 2600 windows · right 77% vs Kalshi 76% · logloss 0.4764 vs 0.4779 · edge bets 10: won 70%, ROI +31% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.4988 vs 0.4996 · edge bets 25: won 48%, ROI -14%

**All months:** 13159 windows · right 76% vs Kalshi 76% · logloss 0.4815 vs 0.4818 · edge bets 71: won 56%, ROI +0%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4635 vs 0.4642 · edge bets 9: won 56%, ROI -3% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4715 vs 0.4719 · edge bets 33: won 58%, ROI +2% |
| 2026-10 | 6800 windows · right 76% vs Kalshi 76% · logloss 0.4931 vs 0.4931 · edge bets 29: won 55%, ROI -0% |

Strongest signals: `sgap` +0.067, `s_EU` +0.036, `tleft` -0.030, `s_US` -0.025, `dmid5` +0.023

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,515, target reached normally 24% | setups 11,097, target reached normally 19% | — |
| ETH | setups 2,477, target reached normally 27% | setups 11,054, target reached normally 19% | — |
| SOL | setups 2,553, target reached normally 22% | setups 11,234, target reached normally 21% | — |
| XRP | setups 2,591, target reached normally 22% | setups 11,484, target reached normally 20% | — |
| DOGE | setups 2,625, target reached normally 24% | setups 11,220, target reached normally 20% | — |

**All weeks:** setups 12,761, target reached normally 24%

**All months:** setups 56,089, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,706, target reached normally 57% | setups 28,432, target reached normally 55% | — |
| ETH | setups 5,617, target reached normally 57% | setups 25,066, target reached normally 54% | — |
| SOL | setups 5,662, target reached normally 56% | setups 24,941, target reached normally 55% | — |
| XRP | setups 5,530, target reached normally 54% | setups 25,065, target reached normally 55% | — |
| DOGE | setups 5,523, target reached normally 56% | setups 24,821, target reached normally 56% | — |
