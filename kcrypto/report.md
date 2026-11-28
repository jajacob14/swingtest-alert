# Kalshi crypto 15-min model report
Trained 2026-11-28 02:51 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 439414

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 598 windows · right 74% vs Kalshi 74% · logloss 0.5181 vs 0.5183 · edge bets 22: won 55%, ROI -2% | 3746 windows · right 76% vs Kalshi 76% · logloss 0.4802 vs 0.4815 · edge bets 7: won 57%, ROI +5% | — |
| XRP | 597 windows · right 74% vs Kalshi 74% · logloss 0.5189 vs 0.5179 · edge bets 9: won 56%, ROI +1% | 3745 windows · right 76% vs Kalshi 76% · logloss 0.487 vs 0.4871 · edge bets 1: won 100%, ROI +41% | — |
| ETH | 598 windows · right 73% vs Kalshi 73% · logloss 0.5264 vs 0.5258 · edge bets 15: won 67%, ROI +20% | 3748 windows · right 76% vs Kalshi 76% · logloss 0.4831 vs 0.4825 · edge bets 2: won 0%, ROI -100% | — |
| BTC | 598 windows · right 73% vs Kalshi 74% · logloss 0.5194 vs 0.5182 · edge bets 22: won 50%, ROI -11% | 3826 windows · right 74% vs Kalshi 74% · logloss 0.5059 vs 0.5061 · edge bets 14: won 64%, ROI +7% | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.5045 vs 0.5055 · edge bets 17: won 71%, ROI +34% | 3748 windows · right 76% vs Kalshi 76% · logloss 0.4888 vs 0.4893 · edge bets 1: won 100%, ROI +108% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5175 vs 0.5172 · edge bets 85: won 59%, ROI +7%

**All months:** 18813 windows · right 76% vs Kalshi 76% · logloss 0.4892 vs 0.4895 · edge bets 25: won 60%, ROI +4%

| Month | Result |
|---|---|
| 2026-08 | 1540 windows · right 78% vs Kalshi 78% · logloss 0.4626 vs 0.4627 · edge bets 2: won 50%, ROI -3% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4716 vs 0.4719 · edge bets 8: won 62%, ROI +6% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4967 vs 0.4969 · edge bets 12: won 67%, ROI +18% |
| 2026-11 | 3000 windows · right 75% vs Kalshi 75% · logloss 0.5078 vs 0.5087 · edge bets 3: won 33%, ROI -48% |

Strongest signals: `sgap` +0.051, `dmid5` +0.035, `s_EU` +0.034, `s_US` -0.025, `sr1` +0.025

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,269, target reached normally 24% | setups 16,186, target reached normally 20% | — |
| XRP | setups 2,493, target reached normally 25% | setups 16,270, target reached normally 21% | — |
| ETH | setups 2,320, target reached normally 23% | setups 15,793, target reached normally 20% | — |
| BTC | setups 2,255, target reached normally 21% | setups 15,377, target reached normally 20% | — |
| SOL | setups 2,389, target reached normally 23% | setups 16,000, target reached normally 21% | — |

**All weeks:** setups 11,726, target reached normally 23%

**All months:** setups 79,626, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,219, target reached normally 58% | setups 35,749, target reached normally 56% | — |
| XRP | setups 5,834, target reached normally 57% | setups 36,015, target reached normally 56% | — |
| ETH | setups 6,118, target reached normally 57% | setups 36,259, target reached normally 55% | — |
| BTC | setups 6,179, target reached normally 57% | setups 39,369, target reached normally 56% | — |
| SOL | setups 6,036, target reached normally 56% | setups 35,821, target reached normally 56% | — |
