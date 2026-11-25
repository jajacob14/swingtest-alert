# Kalshi crypto 15-min model report
Trained 2026-11-24 22:06 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 364804

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 73% vs Kalshi 73% · logloss 0.5222 vs 0.5232 · edge bets 5: won 40%, ROI -30% | 3603 windows · right 75% vs Kalshi 75% · logloss 0.5034 vs 0.5039 · edge bets 44: won 66%, ROI +11% | — |
| ETH | 597 windows · right 73% vs Kalshi 73% · logloss 0.5249 vs 0.5236 · edge bets 7: won 57%, ROI +4% | 3449 windows · right 77% vs Kalshi 77% · logloss 0.4803 vs 0.4798 · edge bets 1: won 100%, ROI +45% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.4961 vs 0.497 · edge bets 1: won 100%, ROI +85% | 3449 windows · right 76% vs Kalshi 76% · logloss 0.4868 vs 0.4872 · edge bets 1: won 100%, ROI +96% | — |
| XRP | 598 windows · right 74% vs Kalshi 74% · logloss 0.5215 vs 0.5209 · edge bets 4: won 75%, ROI +45% | 3446 windows · right 76% vs Kalshi 76% · logloss 0.4827 vs 0.4834 · edge bets 8: won 62%, ROI +6% | — |
| DOGE | 597 windows · right 75% vs Kalshi 75% · logloss 0.507 vs 0.5072 · edge bets 13: won 54%, ROI -6% | 3447 windows · right 77% vs Kalshi 76% · logloss 0.4771 vs 0.4786 · edge bets 24: won 71%, ROI +32% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5143 vs 0.5143 · edge bets 30: won 57%, ROI +1%

**All months:** 17394 windows · right 76% vs Kalshi 76% · logloss 0.4863 vs 0.4868 · edge bets 78: won 68%, ROI +18%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4638 vs 0.4642 · edge bets 5: won 60%, ROI +11% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4713 vs 0.4719 · edge bets 21: won 71%, ROI +16% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4965 vs 0.4969 · edge bets 45: won 71%, ROI +26% |
| 2026-11 | 1505 windows · right 76% vs Kalshi 76% · logloss 0.495 vs 0.4963 · edge bets 7: won 43%, ROI -22% |

Strongest signals: `sgap` +0.075, `dmid5` +0.032, `s_EU` +0.030, `sr1` +0.024, `dmid1` -0.019

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,414, target reached normally 23% | setups 14,500, target reached normally 20% | — |
| ETH | setups 2,415, target reached normally 25% | setups 14,571, target reached normally 20% | — |
| SOL | setups 2,445, target reached normally 20% | setups 14,751, target reached normally 21% | — |
| XRP | setups 2,517, target reached normally 26% | setups 15,026, target reached normally 20% | — |
| DOGE | setups 2,396, target reached normally 22% | setups 14,899, target reached normally 20% | — |

**All weeks:** setups 12,187, target reached normally 23%

**All months:** setups 73,747, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,952, target reached normally 58% | setups 37,069, target reached normally 56% | — |
| ETH | setups 5,994, target reached normally 57% | setups 33,312, target reached normally 55% | — |
| SOL | setups 5,918, target reached normally 55% | setups 32,882, target reached normally 56% | — |
| XRP | setups 5,691, target reached normally 57% | setups 33,168, target reached normally 55% | — |
| DOGE | setups 5,966, target reached normally 57% | setups 32,805, target reached normally 56% | — |
