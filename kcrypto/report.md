# Kalshi crypto 15-min model report
Trained 2026-11-20 08:02 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 265606

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 75% vs Kalshi 75% · logloss 0.4988 vs 0.4991 · edge bets 2: won 0%, ROI -100% | 3163 windows · right 75% vs Kalshi 75% · logloss 0.5008 vs 0.5007 · edge bets 4: won 25%, ROI -56% | — |
| ETH | 597 windows · right 74% vs Kalshi 74% · logloss 0.5161 vs 0.5134 · edge bets 9: won 56%, ROI +2% | 3009 windows · right 77% vs Kalshi 77% · logloss 0.4803 vs 0.4796 | — |
| SOL | 597 windows · right 74% vs Kalshi 74% · logloss 0.5198 vs 0.5196 · edge bets 6: won 33%, ROI -38% | 3009 windows · right 76% vs Kalshi 76% · logloss 0.4856 vs 0.4855 | — |
| XRP | 598 windows · right 75% vs Kalshi 74% · logloss 0.5155 vs 0.5119 · edge bets 52: won 52%, ROI -4% | 3006 windows · right 76% vs Kalshi 76% · logloss 0.4821 vs 0.4824 · edge bets 16: won 56%, ROI +4% | — |
| DOGE | 598 windows · right 74% vs Kalshi 74% · logloss 0.5132 vs 0.5136 · edge bets 15: won 53%, ROI -0% | 3007 windows · right 76% vs Kalshi 76% · logloss 0.4771 vs 0.4782 · edge bets 3: won 100%, ROI +86% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5126 vs 0.5115 · edge bets 84: won 50%, ROI -7%

**All months:** 15194 windows · right 76% vs Kalshi 76% · logloss 0.4854 vs 0.4855 · edge bets 23: won 56%, ROI +4%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4636 vs 0.4642 · edge bets 5: won 60%, ROI +13% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4718 vs 0.4719 · edge bets 8: won 50%, ROI -7% |
| 2026-10 | 8835 windows · right 75% vs Kalshi 75% · logloss 0.497 vs 0.497 · edge bets 10: won 60%, ROI +8% |

Strongest signals: `sgap` +0.057, `tleft` -0.024, `dmid5` +0.024, `s_US` -0.023, `kvol` -0.023

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,513, target reached normally 23% | setups 12,726, target reached normally 19% | — |
| ETH | setups 2,478, target reached normally 26% | setups 12,667, target reached normally 20% | — |
| SOL | setups 2,476, target reached normally 23% | setups 12,880, target reached normally 21% | — |
| XRP | setups 2,525, target reached normally 26% | setups 13,203, target reached normally 20% | — |
| DOGE | setups 2,527, target reached normally 23% | setups 12,916, target reached normally 20% | — |

**All weeks:** setups 12,519, target reached normally 24%

**All months:** setups 64,392, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,812, target reached normally 57% | setups 32,515, target reached normally 55% | — |
| ETH | setups 5,630, target reached normally 57% | setups 29,150, target reached normally 55% | — |
| SOL | setups 5,756, target reached normally 58% | setups 28,831, target reached normally 56% | — |
| XRP | setups 5,488, target reached normally 56% | setups 28,940, target reached normally 56% | — |
| DOGE | setups 5,613, target reached normally 56% | setups 28,731, target reached normally 56% | — |
