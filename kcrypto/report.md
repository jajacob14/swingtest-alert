# Kalshi crypto 15-min model report
Trained 2026-11-22 13:20 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 313025

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 74% vs Kalshi 74% · logloss 0.5065 vs 0.506 · edge bets 5: won 100%, ROI +68% | 3376 windows · right 75% vs Kalshi 75% · logloss 0.5007 vs 0.501 · edge bets 3: won 33%, ROI -45% | — |
| ETH | 597 windows · right 74% vs Kalshi 74% · logloss 0.5148 vs 0.5129 · edge bets 3: won 100%, ROI +95% | 3222 windows · right 77% vs Kalshi 77% · logloss 0.4777 vs 0.4772 | — |
| SOL | 598 windows · right 74% vs Kalshi 74% · logloss 0.511 vs 0.5089 · edge bets 15: won 47%, ROI -21% | 3222 windows · right 76% vs Kalshi 76% · logloss 0.487 vs 0.4871 | — |
| XRP | 598 windows · right 75% vs Kalshi 74% · logloss 0.5179 vs 0.5159 · edge bets 19: won 53%, ROI -3% | 3219 windows · right 76% vs Kalshi 76% · logloss 0.4813 vs 0.4815 · edge bets 4: won 75%, ROI +33% | — |
| DOGE | 598 windows · right 76% vs Kalshi 76% · logloss 0.4988 vs 0.4975 · edge bets 17: won 47%, ROI -12% | 3220 windows · right 77% vs Kalshi 76% · logloss 0.4768 vs 0.4778 · edge bets 3: won 100%, ROI +86% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5097 vs 0.5082 · edge bets 59: won 56%, ROI +1%

**All months:** 16259 windows · right 76% vs Kalshi 76% · logloss 0.4849 vs 0.4852 · edge bets 10: won 70%, ROI +23%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4631 vs 0.4642 |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4716 vs 0.4719 · edge bets 2: won 50%, ROI -6% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4969 vs 0.4969 · edge bets 7: won 71%, ROI +22% |
| 2026-11 | 370 windows · right 79% vs Kalshi 79% · logloss 0.4492 vs 0.4496 · edge bets 1: won 100%, ROI +85% |

Strongest signals: `sgap` +0.046, `s_EU` +0.028, `dmid5` +0.027, `m_XRP` +0.017, `sr1` +0.016

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,482, target reached normally 22% | setups 13,570, target reached normally 20% | — |
| ETH | setups 2,434, target reached normally 25% | setups 13,556, target reached normally 20% | — |
| SOL | setups 2,479, target reached normally 22% | setups 13,749, target reached normally 21% | — |
| XRP | setups 2,527, target reached normally 26% | setups 14,078, target reached normally 20% | — |
| DOGE | setups 2,455, target reached normally 22% | setups 13,855, target reached normally 20% | — |

**All weeks:** setups 12,377, target reached normally 24%

**All months:** setups 68,808, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,861, target reached normally 57% | setups 34,735, target reached normally 56% | — |
| ETH | setups 5,796, target reached normally 58% | setups 31,214, target reached normally 55% | — |
| SOL | setups 5,802, target reached normally 57% | setups 30,825, target reached normally 56% | — |
| XRP | setups 5,486, target reached normally 58% | setups 30,998, target reached normally 56% | — |
| DOGE | setups 5,716, target reached normally 57% | setups 30,783, target reached normally 56% | — |
