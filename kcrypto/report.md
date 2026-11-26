# Kalshi crypto 15-min model report
Trained 2026-11-26 07:52 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 395144

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 597 windows · right 74% vs Kalshi 74% · logloss 0.5223 vs 0.5218 · edge bets 26: won 46%, ROI -17% | 3574 windows · right 76% vs Kalshi 76% · logloss 0.4785 vs 0.48 · edge bets 21: won 62%, ROI +14% | — |
| XRP | 597 windows · right 75% vs Kalshi 74% · logloss 0.5141 vs 0.5131 · edge bets 7: won 43%, ROI -17% | 3573 windows · right 76% vs Kalshi 76% · logloss 0.4848 vs 0.4851 · edge bets 8: won 62%, ROI +6% | — |
| ETH | 598 windows · right 72% vs Kalshi 73% · logloss 0.5308 vs 0.5299 · edge bets 16: won 50%, ROI -8% | 3576 windows · right 77% vs Kalshi 77% · logloss 0.4819 vs 0.4812 · edge bets 4: won 25%, ROI -55% | — |
| BTC | 598 windows · right 73% vs Kalshi 73% · logloss 0.5194 vs 0.5186 · edge bets 13: won 54%, ROI -5% | 3710 windows · right 75% vs Kalshi 75% · logloss 0.503 vs 0.5033 · edge bets 40: won 68%, ROI +13% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.4991 vs 0.4993 · edge bets 15: won 53%, ROI -2% | 3576 windows · right 76% vs Kalshi 76% · logloss 0.489 vs 0.4894 · edge bets 2: won 100%, ROI +87% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5171 vs 0.5165 · edge bets 77: won 49%, ROI -10%

**All months:** 18009 windows · right 76% vs Kalshi 76% · logloss 0.4876 vs 0.488 · edge bets 75: won 64%, ROI +11%

| Month | Result |
|---|---|
| 2026-08 | 1596 windows · right 78% vs Kalshi 78% · logloss 0.4643 vs 0.4645 · edge bets 5: won 40%, ROI -26% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4715 vs 0.4719 · edge bets 24: won 62%, ROI +3% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4966 vs 0.4969 · edge bets 40: won 70%, ROI +23% |
| 2026-11 | 2140 windows · right 75% vs Kalshi 75% · logloss 0.5024 vs 0.5033 · edge bets 6: won 50%, ROI -9% |

Strongest signals: `sgap` +0.069, `dmid5` +0.034, `s_EU` +0.032, `sr1` +0.026, `s_US` -0.020

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,323, target reached normally 23% | setups 15,496, target reached normally 20% | — |
| XRP | setups 2,535, target reached normally 26% | setups 15,581, target reached normally 20% | — |
| ETH | setups 2,387, target reached normally 24% | setups 15,121, target reached normally 20% | — |
| BTC | setups 2,359, target reached normally 21% | setups 14,987, target reached normally 20% | — |
| SOL | setups 2,432, target reached normally 21% | setups 15,314, target reached normally 21% | — |

**All weeks:** setups 12,036, target reached normally 23%

**All months:** setups 76,499, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,098, target reached normally 58% | setups 33,995, target reached normally 56% | — |
| XRP | setups 5,745, target reached normally 57% | setups 34,328, target reached normally 56% | — |
| ETH | setups 6,035, target reached normally 58% | setups 34,485, target reached normally 55% | — |
| BTC | setups 6,023, target reached normally 57% | setups 38,066, target reached normally 56% | — |
| SOL | setups 5,924, target reached normally 56% | setups 34,062, target reached normally 56% | — |
