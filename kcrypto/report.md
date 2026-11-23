# Kalshi crypto 15-min model report
Trained 2026-11-23 09:51 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 330878

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5101 vs 0.5103 · edge bets 4: won 75%, ROI +22% | 3458 windows · right 75% vs Kalshi 75% · logloss 0.5021 vs 0.5024 · edge bets 17: won 53%, ROI -10% | — |
| ETH | 598 windows · right 74% vs Kalshi 74% · logloss 0.5131 vs 0.5113 | 3304 windows · right 77% vs Kalshi 77% · logloss 0.4779 vs 0.4774 | — |
| SOL | 598 windows · right 74% vs Kalshi 74% · logloss 0.5122 vs 0.5118 · edge bets 12: won 33%, ROI -42% | 3304 windows · right 76% vs Kalshi 76% · logloss 0.4876 vs 0.4878 · edge bets 2: won 100%, ROI +90% | — |
| XRP | 597 windows · right 74% vs Kalshi 74% · logloss 0.5202 vs 0.5188 · edge bets 20: won 55%, ROI +2% | 3301 windows · right 76% vs Kalshi 76% · logloss 0.4817 vs 0.4821 · edge bets 15: won 60%, ROI +9% | — |
| DOGE | 597 windows · right 76% vs Kalshi 76% · logloss 0.4892 vs 0.4892 · edge bets 16: won 69%, ROI +29% | 3302 windows · right 77% vs Kalshi 76% · logloss 0.4755 vs 0.4766 · edge bets 25: won 68%, ROI +28% | ✅ |

**All weeks:** 2988 windows · right 74% vs Kalshi 75% · logloss 0.5089 vs 0.5082 · edge bets 52: won 56%, ROI +1%

**All months:** 16669 windows · right 76% vs Kalshi 76% · logloss 0.4852 vs 0.4855 · edge bets 59: won 63%, ROI +14%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4632 vs 0.4642 · edge bets 7: won 57%, ROI +8% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4716 vs 0.4719 · edge bets 21: won 52%, ROI -9% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4968 vs 0.4969 · edge bets 25: won 76%, ROI +40% |
| 2026-11 | 780 windows · right 77% vs Kalshi 76% · logloss 0.4756 vs 0.4763 · edge bets 6: won 50%, ROI -8% |

Strongest signals: `sgap` +0.064, `dmid5` +0.030, `s_EU` +0.030, `sr1` +0.018, `tleft` -0.017

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,460, target reached normally 22% | setups 13,913, target reached normally 20% | — |
| ETH | setups 2,446, target reached normally 24% | setups 13,916, target reached normally 20% | — |
| SOL | setups 2,453, target reached normally 22% | setups 14,102, target reached normally 21% | — |
| XRP | setups 2,540, target reached normally 26% | setups 14,429, target reached normally 20% | — |
| DOGE | setups 2,427, target reached normally 21% | setups 14,257, target reached normally 20% | — |

**All weeks:** setups 12,326, target reached normally 23%

**All months:** setups 70,617, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,916, target reached normally 57% | setups 35,569, target reached normally 56% | — |
| ETH | setups 5,837, target reached normally 56% | setups 31,981, target reached normally 55% | — |
| SOL | setups 5,824, target reached normally 56% | setups 31,567, target reached normally 56% | — |
| XRP | setups 5,533, target reached normally 56% | setups 31,773, target reached normally 56% | — |
| DOGE | setups 5,778, target reached normally 56% | setups 31,486, target reached normally 56% | — |
