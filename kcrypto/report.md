# Kalshi crypto 15-min model report
Trained 2026-11-07 05:07 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 0

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 72% vs Kalshi 73% · logloss 0.5267 vs 0.5267 · edge bets 30: won 50%, ROI -16% | 1919 windows · right 76% vs Kalshi 76% · logloss 0.4941 vs 0.4947 · edge bets 54: won 61%, ROI +1% | — |
| ETH | 597 windows · right 75% vs Kalshi 75% · logloss 0.5042 vs 0.5026 · edge bets 32: won 56%, ROI -0% | 1765 windows · right 78% vs Kalshi 78% · logloss 0.4619 vs 0.461 · edge bets 21: won 38%, ROI -35% | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.4997 vs 0.4985 · edge bets 19: won 42%, ROI -25% | 1765 windows · right 77% vs Kalshi 77% · logloss 0.4804 vs 0.4807 · edge bets 20: won 55%, ROI -6% | — |
| XRP | 598 windows · right 75% vs Kalshi 75% · logloss 0.5113 vs 0.5094 · edge bets 4: won 50%, ROI -11% | 1762 windows · right 77% vs Kalshi 77% · logloss 0.4664 vs 0.4672 · edge bets 33: won 52%, ROI -5% | — |
| DOGE | 598 windows · right 76% vs Kalshi 76% · logloss 0.4882 vs 0.4904 · edge bets 48: won 56%, ROI +4% | 1763 windows · right 78% vs Kalshi 78% · logloss 0.4604 vs 0.4613 · edge bets 40: won 72%, ROI +35% | ✅ |
| BNB | 598 windows · right 75% vs Kalshi 75% · logloss 0.5026 vs 0.5073 · edge bets 57: won 61%, ROI +10% | 1761 windows · right 76% vs Kalshi 76% · logloss 0.4935 vs 0.4952 · edge bets 143: won 60%, ROI +8% | ✅ |
| HYPE | 598 windows · right 75% vs Kalshi 75% · logloss 0.5034 vs 0.5053 · edge bets 28: won 71%, ROI +29% | 1611 windows · right 75% vs Kalshi 74% · logloss 0.4981 vs 0.5007 · edge bets 32: won 75%, ROI +36% | ✅ |

**All weeks:** 4184 windows · right 75% vs Kalshi 75% · logloss 0.5053 vs 0.5059 · edge bets 218: won 57%, ROI +2%

**All months:** 12346 windows · right 76% vs Kalshi 76% · logloss 0.4792 vs 0.48 · edge bets 343: won 61%, ROI +8%

| Month | Result |
|---|---|
| 2026-08 | 2051 windows · right 77% vs Kalshi 77% · logloss 0.4702 vs 0.4713 · edge bets 60: won 52%, ROI -9% |
| 2026-09 | 6640 windows · right 77% vs Kalshi 77% · logloss 0.476 vs 0.4773 · edge bets 171: won 63%, ROI +10% |
| 2026-10 | 3655 windows · right 76% vs Kalshi 76% · logloss 0.4902 vs 0.49 · edge bets 112: won 62%, ROI +13% |

Strongest signals: `sgap` +0.085, `sr1` +0.052, `s_EU` +0.041, `dmid1` -0.037, `m_BNB` +0.030

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,385, target reached normally 22% | setups 7,798, target reached normally 18% | — |
| ETH | setups 2,551, target reached normally 23% | setups 7,644, target reached normally 18% | — |
| SOL | setups 2,533, target reached normally 22% | setups 7,789, target reached normally 20% | — |
| XRP | setups 2,513, target reached normally 22% | setups 7,847, target reached normally 19% | — |
| DOGE | setups 2,656, target reached normally 21% | setups 7,756, target reached normally 18% | — |
| BNB | setups 2,520, target reached normally 20% | setups 7,529, target reached normally 21% | — |
| HYPE | setups 2,563, target reached normally 22% | setups 7,218, target reached normally 21% | — |

**All weeks:** setups 17,721, target reached normally 22%

**All months:** setups 53,581, target reached normally 19%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 6,153, target reached normally 58% | setups 19,972, target reached normally 55% | — |
| ETH | setups 5,711, target reached normally 56% | setups 17,091, target reached normally 53% | — |
| SOL | setups 5,606, target reached normally 56% | setups 16,924, target reached normally 55% | — |
| XRP | setups 5,637, target reached normally 55% | setups 17,166, target reached normally 54% | — |
| DOGE | setups 5,566, target reached normally 55% | setups 16,777, target reached normally 54% | — |
| BNB | setups 5,632, target reached normally 54% | setups 16,875, target reached normally 54% | — |
| HYPE | setups 5,659, target reached normally 56% | setups 14,955, target reached normally 56% | — |
