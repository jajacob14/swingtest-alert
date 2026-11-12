# Kalshi crypto 15-min model report
Trained 2026-11-12 15:45 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 92163

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 75% vs Kalshi 75% · logloss 0.4987 vs 0.4981 · edge bets 30: won 73%, ROI +24% | 2434 windows · right 75% vs Kalshi 76% · logloss 0.4945 vs 0.4946 · edge bets 14: won 64%, ROI +6% | — |
| ETH | 597 windows · right 75% vs Kalshi 76% · logloss 0.5029 vs 0.5024 · edge bets 12: won 42%, ROI -23% | 2280 windows · right 78% vs Kalshi 78% · logloss 0.464 vs 0.4637 · edge bets 1: won 0%, ROI -100% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.5005 vs 0.501 · edge bets 18: won 56%, ROI +2% | 2280 windows · right 77% vs Kalshi 77% · logloss 0.4803 vs 0.4805 · edge bets 2: won 0%, ROI -100% | — |
| XRP | 597 windows · right 74% vs Kalshi 74% · logloss 0.5218 vs 0.5197 · edge bets 21: won 71%, ROI +31% | 2277 windows · right 77% vs Kalshi 77% · logloss 0.4683 vs 0.469 · edge bets 20: won 50%, ROI -6% | — |
| DOGE | 598 windows · right 77% vs Kalshi 77% · logloss 0.478 vs 0.4771 · edge bets 28: won 57%, ROI +10% | 2278 windows · right 77% vs Kalshi 77% · logloss 0.4693 vs 0.4706 · edge bets 5: won 80%, ROI +53% | — |

**All weeks:** 2987 windows · right 75% vs Kalshi 76% · logloss 0.5003 vs 0.4996 · edge bets 109: won 62%, ROI +13%

**All months:** 11549 windows · right 77% vs Kalshi 77% · logloss 0.4756 vs 0.476 · edge bets 42: won 55%, ROI -2%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4634 vs 0.4642 · edge bets 7: won 43%, ROI -20% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4715 vs 0.4719 · edge bets 23: won 61%, ROI +8% |
| 2026-10 | 5190 windows · right 76% vs Kalshi 76% · logloss 0.4834 vs 0.4836 · edge bets 12: won 50%, ROI -11% |

Strongest signals: `sgap` +0.060, `tleft` -0.028, `s_EU` +0.028, `m_XRP` +0.024, `dmid5` +0.024

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,427, target reached normally 23% | setups 9,888, target reached normally 19% | — |
| ETH | setups 2,453, target reached normally 22% | setups 9,808, target reached normally 19% | — |
| SOL | setups 2,529, target reached normally 22% | setups 9,926, target reached normally 21% | — |
| XRP | setups 2,520, target reached normally 24% | setups 10,100, target reached normally 20% | — |
| DOGE | setups 2,668, target reached normally 21% | setups 9,887, target reached normally 20% | — |

**All weeks:** setups 12,597, target reached normally 22%

**All months:** setups 49,609, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,891, target reached normally 56% | setups 25,082, target reached normally 55% | — |
| ETH | setups 5,762, target reached normally 55% | setups 21,907, target reached normally 54% | — |
| SOL | setups 5,653, target reached normally 56% | setups 21,828, target reached normally 56% | — |
| XRP | setups 5,576, target reached normally 55% | setups 21,958, target reached normally 55% | — |
| DOGE | setups 5,528, target reached normally 53% | setups 21,642, target reached normally 55% | — |
