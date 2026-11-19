# Kalshi crypto 15-min model report
Trained 2026-11-18 21:29 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 233894

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 75% vs Kalshi 75% · logloss 0.4995 vs 0.5001 · edge bets 3: won 33%, ROI -43% | 3032 windows · right 75% vs Kalshi 75% · logloss 0.5015 vs 0.5015 · edge bets 5: won 40%, ROI -30% | — |
| ETH | 598 windows · right 75% vs Kalshi 75% · logloss 0.5028 vs 0.5014 · edge bets 5: won 60%, ROI +14% | 2878 windows · right 77% vs Kalshi 77% · logloss 0.4785 vs 0.478 · edge bets 3: won 33%, ROI -32% | — |
| SOL | 598 windows · right 74% vs Kalshi 74% · logloss 0.5184 vs 0.5187 · edge bets 2: won 0%, ROI -100% | 2878 windows · right 76% vs Kalshi 76% · logloss 0.4868 vs 0.4869 | — |
| XRP | 598 windows · right 75% vs Kalshi 75% · logloss 0.5089 vs 0.5055 · edge bets 46: won 54%, ROI -0% | 2875 windows · right 76% vs Kalshi 76% · logloss 0.4817 vs 0.482 · edge bets 31: won 55%, ROI +2% | — |
| DOGE | 597 windows · right 73% vs Kalshi 73% · logloss 0.5237 vs 0.5261 · edge bets 11: won 55%, ROI -5% | 2876 windows · right 77% vs Kalshi 76% · logloss 0.477 vs 0.4783 · edge bets 2: won 100%, ROI +87% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5107 vs 0.5103 · edge bets 67: won 52%, ROI -5%

**All months:** 14539 windows · right 76% vs Kalshi 76% · logloss 0.4853 vs 0.4856 · edge bets 41: won 54%, ROI -0%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4633 vs 0.4642 · edge bets 6: won 50%, ROI -7% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4716 vs 0.4719 · edge bets 16: won 50%, ROI -8% |
| 2026-10 | 8180 windows · right 75% vs Kalshi 75% · logloss 0.4979 vs 0.498 · edge bets 19: won 58%, ROI +8% |

Strongest signals: `sgap` +0.056, `s_EU` +0.029, `dmid5` +0.026, `tleft` -0.024, `s_US` -0.023

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,444, target reached normally 22% | setups 12,174, target reached normally 19% | — |
| ETH | setups 2,479, target reached normally 26% | setups 12,131, target reached normally 20% | — |
| SOL | setups 2,482, target reached normally 24% | setups 12,304, target reached normally 21% | — |
| XRP | setups 2,525, target reached normally 23% | setups 12,632, target reached normally 20% | — |
| DOGE | setups 2,527, target reached normally 23% | setups 12,384, target reached normally 20% | — |

**All weeks:** setups 12,457, target reached normally 24%

**All months:** setups 61,625, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,844, target reached normally 57% | setups 31,239, target reached normally 55% | — |
| ETH | setups 5,600, target reached normally 56% | setups 27,856, target reached normally 55% | — |
| SOL | setups 5,745, target reached normally 57% | setups 27,629, target reached normally 56% | — |
| XRP | setups 5,513, target reached normally 55% | setups 27,734, target reached normally 55% | — |
| DOGE | setups 5,617, target reached normally 57% | setups 27,471, target reached normally 56% | — |
