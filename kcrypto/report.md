# Kalshi crypto 15-min model report
Trained 2026-11-15 01:20 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 149566

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 76% vs Kalshi 76% · logloss 0.4884 vs 0.489 · edge bets 9: won 22%, ROI -61% | 2664 windows · right 75% vs Kalshi 75% · logloss 0.4989 vs 0.4988 · edge bets 19: won 84%, ROI +36% | — |
| ETH | 596 windows · right 76% vs Kalshi 76% · logloss 0.4987 vs 0.499 · edge bets 2: won 50%, ROI -1% | 2510 windows · right 77% vs Kalshi 77% · logloss 0.4709 vs 0.4704 · edge bets 4: won 0%, ROI -100% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.4967 vs 0.4982 · edge bets 5: won 20%, ROI -61% | 2510 windows · right 76% vs Kalshi 76% · logloss 0.4832 vs 0.4831 · edge bets 1: won 100%, ROI +79% | — |
| XRP | 598 windows · right 77% vs Kalshi 77% · logloss 0.4874 vs 0.4851 · edge bets 19: won 63%, ROI +14% | 2507 windows · right 76% vs Kalshi 77% · logloss 0.4753 vs 0.4759 · edge bets 39: won 56%, ROI +2% | — |
| DOGE | 598 windows · right 74% vs Kalshi 74% · logloss 0.5027 vs 0.504 · edge bets 7: won 57%, ROI -5% | 2508 windows · right 77% vs Kalshi 76% · logloss 0.4754 vs 0.4768 · edge bets 7: won 100%, ROI +90% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.4948 vs 0.4951 · edge bets 42: won 48%, ROI -15%

**All months:** 12699 windows · right 76% vs Kalshi 76% · logloss 0.4811 vs 0.4813 · edge bets 70: won 66%, ROI +16%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4634 vs 0.4642 · edge bets 11: won 55%, ROI -3% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4716 vs 0.4719 · edge bets 33: won 64%, ROI +10% |
| 2026-10 | 6340 windows · right 76% vs Kalshi 76% · logloss 0.493 vs 0.4929 · edge bets 26: won 73%, ROI +33% |

Strongest signals: `sgap` +0.062, `s_EU` +0.036, `tleft` -0.033, `dmid5` +0.028, `s_US` -0.026

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,518, target reached normally 22% | setups 10,717, target reached normally 19% | — |
| ETH | setups 2,462, target reached normally 25% | setups 10,688, target reached normally 19% | — |
| SOL | setups 2,559, target reached normally 21% | setups 10,840, target reached normally 21% | — |
| XRP | setups 2,571, target reached normally 23% | setups 11,096, target reached normally 20% | — |
| DOGE | setups 2,628, target reached normally 23% | setups 10,830, target reached normally 20% | — |

**All weeks:** setups 12,738, target reached normally 23%

**All months:** setups 54,171, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,590, target reached normally 55% | setups 27,534, target reached normally 55% | — |
| ETH | setups 5,610, target reached normally 56% | setups 24,176, target reached normally 54% | — |
| SOL | setups 5,600, target reached normally 56% | setups 24,072, target reached normally 55% | — |
| XRP | setups 5,495, target reached normally 53% | setups 24,163, target reached normally 55% | — |
| DOGE | setups 5,495, target reached normally 56% | setups 23,921, target reached normally 56% | — |
