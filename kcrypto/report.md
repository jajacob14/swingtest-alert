# Kalshi crypto 15-min model report
Trained 2026-11-25 08:50 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 373422

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 597 windows · right 74% vs Kalshi 74% · logloss 0.5165 vs 0.5166 · edge bets 7: won 43%, ROI -27% | 3490 windows · right 76% vs Kalshi 76% · logloss 0.4786 vs 0.4802 · edge bets 22: won 68%, ROI +28% | — |
| XRP | 598 windows · right 74% vs Kalshi 74% · logloss 0.5182 vs 0.5174 · edge bets 4: won 50%, ROI -3% | 3489 windows · right 76% vs Kalshi 76% · logloss 0.4832 vs 0.4837 · edge bets 7: won 57%, ROI -2% | — |
| ETH | 597 windows · right 73% vs Kalshi 73% · logloss 0.5311 vs 0.5304 · edge bets 11: won 64%, ROI +16% | 3492 windows · right 77% vs Kalshi 77% · logloss 0.4807 vs 0.4802 · edge bets 1: won 100%, ROI +45% | — |
| BTC | 598 windows · right 73% vs Kalshi 74% · logloss 0.5178 vs 0.5176 · edge bets 7: won 57%, ROI +4% | 3646 windows · right 75% vs Kalshi 75% · logloss 0.5037 vs 0.5043 · edge bets 44: won 64%, ROI +8% | — |
| SOL | 598 windows · right 76% vs Kalshi 75% · logloss 0.4946 vs 0.495 · edge bets 4: won 50%, ROI -5% | 3492 windows · right 76% vs Kalshi 76% · logloss 0.4875 vs 0.4878 · edge bets 1: won 100%, ROI +96% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5156 vs 0.5154 · edge bets 33: won 55%, ROI -1%

**All months:** 17609 windows · right 76% vs Kalshi 76% · logloss 0.487 vs 0.4875 · edge bets 75: won 65%, ROI +14%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4637 vs 0.4642 · edge bets 4: won 50%, ROI -0% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4714 vs 0.4719 · edge bets 21: won 71%, ROI +17% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4966 vs 0.4969 · edge bets 43: won 67%, ROI +20% |
| 2026-11 | 1720 windows · right 75% vs Kalshi 75% · logloss 0.5005 vs 0.502 · edge bets 7: won 43%, ROI -22% |

Strongest signals: `sgap` +0.074, `dmid5` +0.034, `s_EU` +0.034, `sr1` +0.025, `dmid1` -0.019

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,379, target reached normally 22% | setups 15,092, target reached normally 20% | — |
| XRP | setups 2,528, target reached normally 26% | setups 15,212, target reached normally 20% | — |
| ETH | setups 2,399, target reached normally 25% | setups 14,744, target reached normally 20% | — |
| BTC | setups 2,396, target reached normally 22% | setups 14,697, target reached normally 20% | — |
| SOL | setups 2,435, target reached normally 21% | setups 14,937, target reached normally 21% | — |

**All weeks:** setups 12,137, target reached normally 23%

**All months:** setups 74,682, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,017, target reached normally 58% | setups 33,204, target reached normally 56% | — |
| XRP | setups 5,747, target reached normally 57% | setups 33,559, target reached normally 55% | — |
| ETH | setups 6,017, target reached normally 58% | setups 33,718, target reached normally 55% | — |
| BTC | setups 5,966, target reached normally 58% | setups 37,478, target reached normally 56% | — |
| SOL | setups 5,941, target reached normally 56% | setups 33,265, target reached normally 56% | — |
