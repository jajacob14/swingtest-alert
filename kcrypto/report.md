# Kalshi crypto 15-min model report
Trained 2026-11-25 20:21 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 385601

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 597 windows · right 74% vs Kalshi 74% · logloss 0.5151 vs 0.5151 · edge bets 9: won 44%, ROI -22% | 3536 windows · right 76% vs Kalshi 76% · logloss 0.4791 vs 0.4807 · edge bets 15: won 67%, ROI +22% | — |
| XRP | 598 windows · right 75% vs Kalshi 74% · logloss 0.5129 vs 0.5128 · edge bets 2: won 0%, ROI -100% | 3535 windows · right 76% vs Kalshi 76% · logloss 0.4839 vs 0.4844 · edge bets 5: won 60%, ROI +8% | — |
| ETH | 598 windows · right 72% vs Kalshi 72% · logloss 0.5377 vs 0.537 · edge bets 12: won 58%, ROI +10% | 3538 windows · right 77% vs Kalshi 77% · logloss 0.4815 vs 0.481 · edge bets 1: won 100%, ROI +45% | — |
| BTC | 598 windows · right 73% vs Kalshi 73% · logloss 0.5214 vs 0.5207 · edge bets 7: won 57%, ROI +7% | 3688 windows · right 75% vs Kalshi 75% · logloss 0.5043 vs 0.5047 · edge bets 36: won 69%, ROI +17% | — |
| SOL | 597 windows · right 76% vs Kalshi 76% · logloss 0.493 vs 0.4932 · edge bets 8: won 50%, ROI -5% | 3538 windows · right 76% vs Kalshi 76% · logloss 0.4885 vs 0.4887 · edge bets 1: won 100%, ROI +96% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.516 vs 0.5158 · edge bets 38: won 50%, ROI -7%

**All months:** 17835 windows · right 76% vs Kalshi 76% · logloss 0.4877 vs 0.4882 · edge bets 58: won 69%, ROI +19%

| Month | Result |
|---|---|
| 2026-08 | 1612 windows · right 78% vs Kalshi 78% · logloss 0.4641 vs 0.4645 · edge bets 3: won 33%, ROI -35% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4714 vs 0.4719 · edge bets 18: won 72%, ROI +15% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4965 vs 0.4969 · edge bets 32: won 72%, ROI +29% |
| 2026-11 | 1950 windows · right 75% vs Kalshi 75% · logloss 0.505 vs 0.5063 · edge bets 5: won 60%, ROI +6% |

Strongest signals: `sgap` +0.072, `dmid5` +0.033, `s_EU` +0.032, `sr1` +0.024, `s_US` -0.020

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,403, target reached normally 23% | setups 15,304, target reached normally 20% | — |
| XRP | setups 2,548, target reached normally 25% | setups 15,395, target reached normally 20% | — |
| ETH | setups 2,412, target reached normally 26% | setups 14,926, target reached normally 20% | — |
| BTC | setups 2,384, target reached normally 22% | setups 14,857, target reached normally 20% | — |
| SOL | setups 2,451, target reached normally 21% | setups 15,133, target reached normally 21% | — |

**All weeks:** setups 12,198, target reached normally 23%

**All months:** setups 75,615, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,005, target reached normally 58% | setups 33,635, target reached normally 56% | — |
| XRP | setups 5,701, target reached normally 57% | setups 34,007, target reached normally 56% | — |
| ETH | setups 5,987, target reached normally 58% | setups 34,158, target reached normally 55% | — |
| BTC | setups 5,980, target reached normally 58% | setups 37,895, target reached normally 56% | — |
| SOL | setups 5,909, target reached normally 55% | setups 33,714, target reached normally 56% | — |
