# Kalshi crypto 15-min model report
Trained 2026-11-26 19:23 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 406794

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 598 windows · right 73% vs Kalshi 73% · logloss 0.5285 vs 0.5284 · edge bets 17: won 35%, ROI -36% | 3620 windows · right 76% vs Kalshi 76% · logloss 0.4804 vs 0.4817 · edge bets 14: won 64%, ROI +18% | — |
| XRP | 598 windows · right 74% vs Kalshi 74% · logloss 0.5174 vs 0.5172 · edge bets 6: won 50%, ROI -7% | 3619 windows · right 76% vs Kalshi 76% · logloss 0.4846 vs 0.4847 · edge bets 5: won 60%, ROI +1% | — |
| ETH | 598 windows · right 74% vs Kalshi 74% · logloss 0.5234 vs 0.5222 · edge bets 12: won 58%, ROI +7% | 3622 windows · right 76% vs Kalshi 76% · logloss 0.4834 vs 0.4828 · edge bets 2: won 0%, ROI -100% | — |
| BTC | 597 windows · right 73% vs Kalshi 73% · logloss 0.5197 vs 0.5191 · edge bets 11: won 46%, ROI -16% | 3741 windows · right 75% vs Kalshi 74% · logloss 0.505 vs 0.5055 · edge bets 18: won 61%, ROI +7% | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.5034 vs 0.5036 · edge bets 14: won 50%, ROI -4% | 3622 windows · right 76% vs Kalshi 76% · logloss 0.489 vs 0.4894 · edge bets 1: won 100%, ROI +79% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5185 vs 0.5181 · edge bets 60: won 47%, ROI -14%

**All months:** 18224 windows · right 76% vs Kalshi 76% · logloss 0.4887 vs 0.489 · edge bets 40: won 60%, ROI +7%

| Month | Result |
|---|---|
| 2026-08 | 1581 windows · right 78% vs Kalshi 78% · logloss 0.4647 vs 0.465 · edge bets 2: won 50%, ROI -3% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4715 vs 0.4719 · edge bets 15: won 60%, ROI +1% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4967 vs 0.4969 · edge bets 20: won 65%, ROI +20% |
| 2026-11 | 2370 windows · right 74% vs Kalshi 75% · logloss 0.5083 vs 0.5092 · edge bets 3: won 33%, ROI -40% |

Strongest signals: `sgap` +0.060, `dmid5` +0.039, `s_EU` +0.032, `sr1` +0.027, `kvol` -0.020

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,321, target reached normally 23% | setups 15,667, target reached normally 20% | — |
| XRP | setups 2,547, target reached normally 25% | setups 15,755, target reached normally 20% | — |
| ETH | setups 2,377, target reached normally 24% | setups 15,285, target reached normally 20% | — |
| BTC | setups 2,303, target reached normally 21% | setups 15,085, target reached normally 20% | — |
| SOL | setups 2,423, target reached normally 22% | setups 15,500, target reached normally 21% | — |

**All weeks:** setups 11,971, target reached normally 23%

**All months:** setups 77,292, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,205, target reached normally 59% | setups 34,482, target reached normally 56% | — |
| XRP | setups 5,835, target reached normally 57% | setups 34,799, target reached normally 56% | — |
| ETH | setups 6,089, target reached normally 57% | setups 34,958, target reached normally 55% | — |
| BTC | setups 6,155, target reached normally 57% | setups 38,400, target reached normally 56% | — |
| SOL | setups 6,009, target reached normally 56% | setups 34,546, target reached normally 56% | — |
