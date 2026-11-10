# Kalshi crypto 15-min model report
Trained 2026-11-09 18:36 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 39852

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 75% vs Kalshi 75% · logloss 0.506 vs 0.5069 · edge bets 38: won 74%, ROI +26% | 2165 windows · right 75% vs Kalshi 76% · logloss 0.4943 vs 0.4942 · edge bets 23: won 65%, ROI +7% | — |
| ETH | 597 windows · right 76% vs Kalshi 76% · logloss 0.496 vs 0.495 · edge bets 16: won 44%, ROI -24% | 2011 windows · right 78% vs Kalshi 78% · logloss 0.4615 vs 0.461 · edge bets 3: won 33%, ROI -43% | — |
| SOL | 598 windows · right 74% vs Kalshi 74% · logloss 0.5236 vs 0.5224 · edge bets 37: won 46%, ROI -15% | 2011 windows · right 77% vs Kalshi 77% · logloss 0.4801 vs 0.4801 · edge bets 4: won 25%, ROI -59% | — |
| XRP | 597 windows · right 74% vs Kalshi 74% · logloss 0.5273 vs 0.5246 · edge bets 19: won 47%, ROI -15% | 2008 windows · right 77% vs Kalshi 77% · logloss 0.4686 vs 0.4696 · edge bets 20: won 50%, ROI -4% | — |
| DOGE | 598 windows · right 76% vs Kalshi 77% · logloss 0.4872 vs 0.4857 · edge bets 68: won 56%, ROI +4% | 2009 windows · right 78% vs Kalshi 78% · logloss 0.4627 vs 0.464 · edge bets 12: won 67%, ROI +24% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.508 vs 0.5069 · edge bets 178: won 56%, ROI +0%

**All months:** 10204 windows · right 77% vs Kalshi 77% · logloss 0.4739 vs 0.4742 · edge bets 62: won 56%, ROI -0%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4634 vs 0.4642 · edge bets 7: won 57%, ROI +6% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4713 vs 0.4719 · edge bets 28: won 61%, ROI +6% |
| 2026-10 | 3845 windows · right 76% vs Kalshi 76% · logloss 0.4817 vs 0.4813 · edge bets 27: won 52%, ROI -9% |

Strongest signals: `sgap` +0.060, `dmid5` +0.031, `dmid1` -0.029, `sr1` +0.026, `s_EU` +0.026

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,371, target reached normally 22% | setups 8,779, target reached normally 18% | — |
| ETH | setups 2,501, target reached normally 22% | setups 8,681, target reached normally 18% | — |
| SOL | setups 2,492, target reached normally 24% | setups 8,837, target reached normally 20% | — |
| XRP | setups 2,487, target reached normally 23% | setups 8,936, target reached normally 19% | — |
| DOGE | setups 2,638, target reached normally 20% | setups 8,780, target reached normally 19% | — |

**All weeks:** setups 12,489, target reached normally 22%

**All months:** setups 44,013, target reached normally 19%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 6,107, target reached normally 56% | setups 22,462, target reached normally 55% | — |
| ETH | setups 5,844, target reached normally 56% | setups 19,369, target reached normally 53% | — |
| SOL | setups 5,775, target reached normally 57% | setups 19,199, target reached normally 55% | — |
| XRP | setups 5,611, target reached normally 56% | setups 19,404, target reached normally 54% | — |
| DOGE | setups 5,664, target reached normally 55% | setups 19,042, target reached normally 55% | — |
