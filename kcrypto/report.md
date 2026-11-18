# Kalshi crypto 15-min model report
Trained 2026-11-17 22:26 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 212236

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 76% vs Kalshi 75% · logloss 0.4908 vs 0.492 · edge bets 5: won 40%, ROI -28% | 2940 windows · right 75% vs Kalshi 75% · logloss 0.5017 vs 0.5015 · edge bets 14: won 43%, ROI -23% | — |
| ETH | 598 windows · right 75% vs Kalshi 75% · logloss 0.5021 vs 0.5003 · edge bets 19: won 53%, ROI -3% | 2786 windows · right 77% vs Kalshi 77% · logloss 0.4788 vs 0.4779 · edge bets 29: won 38%, ROI -30% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.4924 vs 0.4927 · edge bets 4: won 25%, ROI -54% | 2786 windows · right 76% vs Kalshi 76% · logloss 0.486 vs 0.4858 · edge bets 7: won 57%, ROI +10% | — |
| XRP | 598 windows · right 77% vs Kalshi 77% · logloss 0.4824 vs 0.4807 · edge bets 42: won 52%, ROI -4% | 2783 windows · right 76% vs Kalshi 76% · logloss 0.4811 vs 0.4809 · edge bets 86: won 57%, ROI +6% | — |
| DOGE | 597 windows · right 73% vs Kalshi 73% · logloss 0.5206 vs 0.5241 · edge bets 17: won 53%, ROI -8% | 2784 windows · right 76% vs Kalshi 76% · logloss 0.4773 vs 0.4784 · edge bets 18: won 50%, ROI -6% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.4976 vs 0.498 · edge bets 87: won 51%, ROI -8%

**All months:** 14079 windows · right 76% vs Kalshi 76% · logloss 0.4852 vs 0.4852 · edge bets 154: won 51%, ROI -5%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4629 vs 0.4642 · edge bets 19: won 58%, ROI +7% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4717 vs 0.4719 · edge bets 53: won 47%, ROI -15% |
| 2026-10 | 7720 windows · right 75% vs Kalshi 75% · logloss 0.4986 vs 0.498 · edge bets 82: won 52%, ROI -1% |

Strongest signals: `sgap` +0.060, `s_EU` +0.033, `tleft` -0.023, `dmid5` +0.023, `m_XRP` +0.020

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,462, target reached normally 22% | setups 11,781, target reached normally 19% | — |
| ETH | setups 2,426, target reached normally 26% | setups 11,732, target reached normally 20% | — |
| SOL | setups 2,479, target reached normally 23% | setups 11,932, target reached normally 21% | — |
| XRP | setups 2,527, target reached normally 23% | setups 12,254, target reached normally 20% | — |
| DOGE | setups 2,542, target reached normally 24% | setups 11,976, target reached normally 20% | — |

**All weeks:** setups 12,436, target reached normally 24%

**All months:** setups 59,675, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,810, target reached normally 56% | setups 30,315, target reached normally 55% | — |
| ETH | setups 5,647, target reached normally 57% | setups 26,953, target reached normally 55% | — |
| SOL | setups 5,761, target reached normally 56% | setups 26,801, target reached normally 56% | — |
| XRP | setups 5,575, target reached normally 55% | setups 26,833, target reached normally 55% | — |
| DOGE | setups 5,583, target reached normally 57% | setups 26,596, target reached normally 56% | — |
