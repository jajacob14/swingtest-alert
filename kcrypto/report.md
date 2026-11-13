# Kalshi crypto 15-min model report
Trained 2026-11-13 14:47 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 114920

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 76% vs Kalshi 76% · logloss 0.4848 vs 0.485 · edge bets 21: won 62%, ROI +8% | 2526 windows · right 75% vs Kalshi 76% · logloss 0.4947 vs 0.4949 · edge bets 5: won 60%, ROI +4% | — |
| ETH | 597 windows · right 75% vs Kalshi 75% · logloss 0.506 vs 0.5058 · edge bets 6: won 50%, ROI -6% | 2372 windows · right 78% vs Kalshi 78% · logloss 0.4662 vs 0.4659 | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.4983 vs 0.4983 · edge bets 14: won 43%, ROI -21% | 2372 windows · right 77% vs Kalshi 76% · logloss 0.4821 vs 0.4821 | — |
| XRP | 598 windows · right 76% vs Kalshi 76% · logloss 0.5024 vs 0.4994 · edge bets 20: won 75%, ROI +39% | 2369 windows · right 77% vs Kalshi 77% · logloss 0.4702 vs 0.4707 · edge bets 32: won 56%, ROI +5% | — |
| DOGE | 597 windows · right 76% vs Kalshi 76% · logloss 0.4958 vs 0.4949 · edge bets 18: won 56%, ROI +5% | 2370 windows · right 77% vs Kalshi 77% · logloss 0.4724 vs 0.4736 · edge bets 3: won 100%, ROI +83% | — |

**All weeks:** 2988 windows · right 76% vs Kalshi 76% · logloss 0.4974 vs 0.4966 · edge bets 79: won 60%, ROI +9%

**All months:** 12009 windows · right 77% vs Kalshi 77% · logloss 0.4774 vs 0.4777 · edge bets 40: won 60%, ROI +11%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4632 vs 0.4642 · edge bets 6: won 50%, ROI -8% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4716 vs 0.4719 · edge bets 18: won 61%, ROI +12% |
| 2026-10 | 5650 windows · right 76% vs Kalshi 76% · logloss 0.4866 vs 0.4867 · edge bets 16: won 62%, ROI +16% |

Strongest signals: `sgap` +0.053, `s_EU` +0.034, `tleft` -0.028, `m_XRP` +0.022, `dmid5` +0.021

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,450, target reached normally 22% | setups 10,253, target reached normally 19% | — |
| ETH | setups 2,408, target reached normally 24% | setups 10,179, target reached normally 19% | — |
| SOL | setups 2,540, target reached normally 22% | setups 10,307, target reached normally 21% | — |
| XRP | setups 2,550, target reached normally 24% | setups 10,493, target reached normally 20% | — |
| DOGE | setups 2,611, target reached normally 24% | setups 10,296, target reached normally 20% | — |

**All weeks:** setups 12,559, target reached normally 23%

**All months:** setups 51,528, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,718, target reached normally 55% | setups 26,032, target reached normally 55% | — |
| ETH | setups 5,743, target reached normally 56% | setups 22,817, target reached normally 54% | — |
| SOL | setups 5,609, target reached normally 56% | setups 22,739, target reached normally 56% | — |
| XRP | setups 5,507, target reached normally 54% | setups 22,817, target reached normally 55% | — |
| DOGE | setups 5,537, target reached normally 55% | setups 22,532, target reached normally 55% | — |
