# Kalshi crypto 15-min model report
Trained 2026-11-11 16:43 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 74182

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 75% vs Kalshi 74% · logloss 0.51 vs 0.5097 · edge bets 37: won 65%, ROI +11% | 2349 windows · right 75% vs Kalshi 75% · logloss 0.4953 vs 0.4954 · edge bets 20: won 65%, ROI +8% | — |
| ETH | 597 windows · right 75% vs Kalshi 76% · logloss 0.5013 vs 0.5002 · edge bets 13: won 31%, ROI -42% | 2195 windows · right 78% vs Kalshi 78% · logloss 0.4632 vs 0.4628 · edge bets 2: won 50%, ROI -21% | — |
| SOL | 598 windows · right 74% vs Kalshi 74% · logloss 0.5089 vs 0.5089 · edge bets 36: won 44%, ROI -16% | 2195 windows · right 77% vs Kalshi 77% · logloss 0.479 vs 0.4789 · edge bets 3: won 0%, ROI -100% | — |
| XRP | 598 windows · right 74% vs Kalshi 74% · logloss 0.5274 vs 0.5248 · edge bets 15: won 67%, ROI +21% | 2192 windows · right 77% vs Kalshi 77% · logloss 0.4683 vs 0.4691 · edge bets 18: won 50%, ROI -6% | — |
| DOGE | 598 windows · right 77% vs Kalshi 77% · logloss 0.479 vs 0.4785 · edge bets 38: won 63%, ROI +22% | 2193 windows · right 77% vs Kalshi 77% · logloss 0.466 vs 0.4672 · edge bets 8: won 75%, ROI +40% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.5053 vs 0.5044 · edge bets 139: won 56%, ROI +4%

**All months:** 11124 windows · right 77% vs Kalshi 77% · logloss 0.4748 vs 0.4751 · edge bets 51: won 57%, ROI +0%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4634 vs 0.4642 · edge bets 7: won 43%, ROI -20% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4714 vs 0.4719 · edge bets 25: won 60%, ROI +6% |
| 2026-10 | 4765 windows · right 76% vs Kalshi 76% · logloss 0.4822 vs 0.482 · edge bets 19: won 58%, ROI -0% |

Strongest signals: `sgap` +0.059, `s_EU` +0.032, `dmid5` +0.026, `sr1` +0.023, `dmid1` -0.023

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,399, target reached normally 23% | setups 9,534, target reached normally 19% | — |
| ETH | setups 2,491, target reached normally 23% | setups 9,461, target reached normally 19% | — |
| SOL | setups 2,525, target reached normally 22% | setups 9,601, target reached normally 21% | — |
| XRP | setups 2,510, target reached normally 23% | setups 9,733, target reached normally 20% | — |
| DOGE | setups 2,653, target reached normally 20% | setups 9,578, target reached normally 20% | — |

**All weeks:** setups 12,578, target reached normally 22%

**All months:** setups 47,907, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,976, target reached normally 56% | setups 24,269, target reached normally 55% | — |
| ETH | setups 5,835, target reached normally 56% | setups 21,061, target reached normally 53% | — |
| SOL | setups 5,716, target reached normally 57% | setups 20,995, target reached normally 55% | — |
| XRP | setups 5,592, target reached normally 55% | setups 21,129, target reached normally 55% | — |
| DOGE | setups 5,608, target reached normally 53% | setups 20,788, target reached normally 55% | — |
