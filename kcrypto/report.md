# Kalshi crypto 15-min model report
Trained 2026-11-09 00:55 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 31028

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 73% vs Kalshi 74% · logloss 0.5182 vs 0.5187 · edge bets 57: won 65%, ROI +14% | 2094 windows · right 75% vs Kalshi 76% · logloss 0.4936 vs 0.4933 · edge bets 37: won 60%, ROI -2% | — |
| ETH | 598 windows · right 75% vs Kalshi 75% · logloss 0.512 vs 0.5107 · edge bets 25: won 48%, ROI -17% | 1940 windows · right 78% vs Kalshi 78% · logloss 0.4616 vs 0.4608 · edge bets 7: won 43%, ROI -20% | — |
| SOL | 597 windows · right 74% vs Kalshi 74% · logloss 0.5155 vs 0.515 · edge bets 44: won 50%, ROI -8% | 1940 windows · right 76% vs Kalshi 76% · logloss 0.4804 vs 0.4802 · edge bets 7: won 43%, ROI -28% | — |
| XRP | 598 windows · right 73% vs Kalshi 74% · logloss 0.5274 vs 0.5249 · edge bets 19: won 42%, ROI -24% | 1937 windows · right 77% vs Kalshi 77% · logloss 0.4693 vs 0.4699 · edge bets 38: won 53%, ROI -2% | — |
| DOGE | 598 windows · right 75% vs Kalshi 76% · logloss 0.5043 vs 0.5035 · edge bets 77: won 56%, ROI +3% | 1938 windows · right 78% vs Kalshi 78% · logloss 0.4594 vs 0.4603 · edge bets 22: won 68%, ROI +25% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5155 vs 0.5146 · edge bets 222: won 55%, ROI -1%

**All months:** 9849 windows · right 77% vs Kalshi 77% · logloss 0.4733 vs 0.4734 · edge bets 111: won 57%, ROI +0%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4633 vs 0.4642 · edge bets 15: won 47%, ROI -12% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4715 vs 0.4719 · edge bets 50: won 58%, ROI -0% |
| 2026-10 | 3490 windows · right 76% vs Kalshi 76% · logloss 0.4806 vs 0.4796 · edge bets 46: won 59%, ROI +5% |

Strongest signals: `sgap` +0.064, `dmid5` +0.033, `s_EU` +0.031, `dmid1` -0.029, `s_US` -0.027

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,374, target reached normally 22% | setups 8,464, target reached normally 18% | — |
| ETH | setups 2,510, target reached normally 23% | setups 8,365, target reached normally 18% | — |
| SOL | setups 2,510, target reached normally 24% | setups 8,522, target reached normally 20% | — |
| XRP | setups 2,460, target reached normally 22% | setups 8,616, target reached normally 19% | — |
| DOGE | setups 2,599, target reached normally 21% | setups 8,481, target reached normally 19% | — |

**All weeks:** setups 12,453, target reached normally 22%

**All months:** setups 42,448, target reached normally 19%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 6,200, target reached normally 57% | setups 21,800, target reached normally 55% | — |
| ETH | setups 5,849, target reached normally 56% | setups 18,748, target reached normally 53% | — |
| SOL | setups 5,752, target reached normally 57% | setups 18,565, target reached normally 55% | — |
| XRP | setups 5,727, target reached normally 56% | setups 18,786, target reached normally 54% | — |
| DOGE | setups 5,695, target reached normally 55% | setups 18,392, target reached normally 54% | — |
