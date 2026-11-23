# Kalshi crypto 15-min model report
Trained 2026-11-23 16:18 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 336315

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5088 vs 0.5096 · edge bets 5: won 60%, ROI +0% | 3484 windows · right 75% vs Kalshi 75% · logloss 0.5026 vs 0.503 · edge bets 12: won 50%, ROI -17% | — |
| ETH | 598 windows · right 74% vs Kalshi 74% · logloss 0.5115 vs 0.5099 | 3330 windows · right 77% vs Kalshi 77% · logloss 0.4788 vs 0.4781 · edge bets 2: won 0%, ROI -100% | — |
| SOL | 598 windows · right 74% vs Kalshi 74% · logloss 0.5129 vs 0.5129 · edge bets 14: won 43%, ROI -25% | 3330 windows · right 76% vs Kalshi 76% · logloss 0.4864 vs 0.4865 | — |
| XRP | 597 windows · right 74% vs Kalshi 74% · logloss 0.522 vs 0.5197 · edge bets 21: won 43%, ROI -19% | 3327 windows · right 76% vs Kalshi 76% · logloss 0.4821 vs 0.4825 · edge bets 14: won 64%, ROI +17% | — |
| DOGE | 597 windows · right 76% vs Kalshi 76% · logloss 0.4947 vs 0.4942 · edge bets 20: won 65%, ROI +22% | 3328 windows · right 77% vs Kalshi 76% · logloss 0.476 vs 0.477 · edge bets 25: won 64%, ROI +21% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.51 vs 0.5092 · edge bets 60: won 52%, ROI -5%

**All months:** 16799 windows · right 76% vs Kalshi 76% · logloss 0.4854 vs 0.4857 · edge bets 53: won 58%, ROI +6%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4634 vs 0.4642 · edge bets 6: won 67%, ROI +28% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4716 vs 0.4719 · edge bets 18: won 44%, ROI -20% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4969 vs 0.4969 · edge bets 24: won 67%, ROI +21% |
| 2026-11 | 910 windows · right 76% vs Kalshi 76% · logloss 0.4799 vs 0.481 · edge bets 5: won 60%, ROI +8% |

Strongest signals: `sgap` +0.062, `s_EU` +0.031, `dmid5` +0.029, `tleft` -0.019, `sr1` +0.019

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,450, target reached normally 23% | setups 14,013, target reached normally 20% | — |
| ETH | setups 2,431, target reached normally 25% | setups 14,036, target reached normally 20% | — |
| SOL | setups 2,468, target reached normally 22% | setups 14,240, target reached normally 21% | — |
| XRP | setups 2,545, target reached normally 26% | setups 14,538, target reached normally 20% | — |
| DOGE | setups 2,429, target reached normally 22% | setups 14,375, target reached normally 20% | — |

**All weeks:** setups 12,323, target reached normally 24%

**All months:** setups 71,202, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,906, target reached normally 58% | setups 35,848, target reached normally 56% | — |
| ETH | setups 5,837, target reached normally 56% | setups 32,218, target reached normally 55% | — |
| SOL | setups 5,835, target reached normally 56% | setups 31,792, target reached normally 56% | — |
| XRP | setups 5,583, target reached normally 56% | setups 32,034, target reached normally 55% | — |
| DOGE | setups 5,822, target reached normally 56% | setups 31,734, target reached normally 56% | — |
