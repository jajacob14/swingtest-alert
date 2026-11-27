# Kalshi crypto 15-min model report
Trained 2026-11-27 03:48 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 415677

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 598 windows · right 74% vs Kalshi 74% · logloss 0.5233 vs 0.5236 · edge bets 9: won 56%, ROI +2% | 3654 windows · right 76% vs Kalshi 76% · logloss 0.4803 vs 0.4816 · edge bets 8: won 75%, ROI +37% | — |
| XRP | 597 windows · right 74% vs Kalshi 74% · logloss 0.5156 vs 0.5156 · edge bets 4: won 50%, ROI -7% | 3653 windows · right 76% vs Kalshi 76% · logloss 0.4853 vs 0.4856 · edge bets 3: won 67%, ROI +12% | — |
| ETH | 597 windows · right 74% vs Kalshi 74% · logloss 0.5204 vs 0.5195 · edge bets 9: won 67%, ROI +19% | 3656 windows · right 76% vs Kalshi 76% · logloss 0.4827 vs 0.4822 · edge bets 1: won 0%, ROI -100% | — |
| BTC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5192 vs 0.5192 · edge bets 5: won 40%, ROI -21% | 3764 windows · right 75% vs Kalshi 75% · logloss 0.504 vs 0.5046 · edge bets 15: won 60%, ROI +0% | — |
| SOL | 598 windows · right 76% vs Kalshi 76% · logloss 0.4975 vs 0.4977 · edge bets 11: won 46%, ROI -14% | 3656 windows · right 76% vs Kalshi 76% · logloss 0.4891 vs 0.4896 | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5152 vs 0.5151 · edge bets 38: won 53%, ROI -2%

**All months:** 18383 windows · right 76% vs Kalshi 76% · logloss 0.4885 vs 0.4889 · edge bets 27: won 63%, ROI +9%

| Month | Result |
|---|---|
| 2026-08 | 1570 windows · right 78% vs Kalshi 78% · logloss 0.4634 vs 0.4635 · edge bets 1: won 100%, ROI +82% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4714 vs 0.4719 · edge bets 10: won 60%, ROI +1% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4966 vs 0.4969 · edge bets 15: won 67%, ROI +18% |
| 2026-11 | 2540 windows · right 75% vs Kalshi 75% · logloss 0.5065 vs 0.5076 · edge bets 1: won 0%, ROI -100% |

Strongest signals: `sgap` +0.059, `dmid5` +0.038, `s_EU` +0.032, `sr1` +0.026, `s_US` -0.021

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,323, target reached normally 23% | setups 15,816, target reached normally 20% | — |
| XRP | setups 2,550, target reached normally 26% | setups 15,895, target reached normally 20% | — |
| ETH | setups 2,356, target reached normally 23% | setups 15,444, target reached normally 20% | — |
| BTC | setups 2,282, target reached normally 21% | setups 15,197, target reached normally 20% | — |
| SOL | setups 2,456, target reached normally 22% | setups 15,663, target reached normally 21% | — |

**All weeks:** setups 11,967, target reached normally 23%

**All months:** setups 78,015, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,197, target reached normally 59% | setups 34,798, target reached normally 56% | — |
| XRP | setups 5,799, target reached normally 57% | setups 35,123, target reached normally 56% | — |
| ETH | setups 6,097, target reached normally 57% | setups 35,281, target reached normally 55% | — |
| BTC | setups 6,136, target reached normally 58% | setups 38,622, target reached normally 56% | — |
| SOL | setups 5,981, target reached normally 55% | setups 34,875, target reached normally 56% | — |
