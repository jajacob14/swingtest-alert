# Kalshi crypto 15-min model report
Trained 2026-11-24 10:33 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 351655

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5121 vs 0.5128 · edge bets 2: won 50%, ROI -21% | 3557 windows · right 75% vs Kalshi 75% · logloss 0.5029 vs 0.5035 · edge bets 28: won 61%, ROI +1% | — |
| ETH | 597 windows · right 74% vs Kalshi 74% · logloss 0.5135 vs 0.512 · edge bets 2: won 100%, ROI +63% | 3403 windows · right 76% vs Kalshi 77% · logloss 0.4812 vs 0.4807 · edge bets 1: won 100%, ROI +45% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.5079 vs 0.5085 · edge bets 1: won 100%, ROI +85% | 3403 windows · right 76% vs Kalshi 76% · logloss 0.4864 vs 0.4869 · edge bets 1: won 100%, ROI +96% | — |
| XRP | 598 windows · right 74% vs Kalshi 75% · logloss 0.522 vs 0.5197 · edge bets 3: won 100%, ROI +88% | 3400 windows · right 76% vs Kalshi 76% · logloss 0.4828 vs 0.4834 · edge bets 7: won 57%, ROI -2% | — |
| DOGE | 597 windows · right 76% vs Kalshi 76% · logloss 0.4974 vs 0.4969 · edge bets 14: won 79%, ROI +40% | 3401 windows · right 76% vs Kalshi 76% · logloss 0.4784 vs 0.4796 · edge bets 27: won 63%, ROI +19% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.5105 vs 0.51 · edge bets 22: won 82%, ROI +44%

**All months:** 17164 windows · right 76% vs Kalshi 76% · logloss 0.4866 vs 0.4871 · edge bets 64: won 62%, ROI +10%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4635 vs 0.4642 · edge bets 5: won 40%, ROI -24% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4714 vs 0.4719 · edge bets 20: won 60%, ROI -0% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4966 vs 0.4969 · edge bets 35: won 71%, ROI +28% |
| 2026-11 | 1275 windows · right 75% vs Kalshi 75% · logloss 0.4992 vs 0.5012 · edge bets 4: won 25%, ROI -53% |

Strongest signals: `sgap` +0.071, `dmid5` +0.033, `s_EU` +0.031, `sr1` +0.026, `dmid1` -0.021

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,420, target reached normally 22% | setups 14,316, target reached normally 20% | — |
| ETH | setups 2,432, target reached normally 24% | setups 14,356, target reached normally 20% | — |
| SOL | setups 2,458, target reached normally 21% | setups 14,557, target reached normally 21% | — |
| XRP | setups 2,524, target reached normally 26% | setups 14,833, target reached normally 20% | — |
| DOGE | setups 2,424, target reached normally 22% | setups 14,685, target reached normally 20% | — |

**All weeks:** setups 12,258, target reached normally 23%

**All months:** setups 72,747, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,953, target reached normally 58% | setups 36,583, target reached normally 56% | — |
| ETH | setups 5,951, target reached normally 57% | setups 32,886, target reached normally 55% | — |
| SOL | setups 5,888, target reached normally 56% | setups 32,452, target reached normally 56% | — |
| XRP | setups 5,645, target reached normally 56% | setups 32,744, target reached normally 55% | — |
| DOGE | setups 5,864, target reached normally 57% | setups 32,414, target reached normally 56% | — |
