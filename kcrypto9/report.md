# Kalshi crypto 15-min model report
Trained 2026-11-28 02:53 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 91556

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 597 windows · right 74% vs Kalshi 74% · logloss 0.5181 vs 0.5184 · edge bets 34: won 56%, ROI -0% | 1525 windows · right 76% vs Kalshi 76% · logloss 0.481 vs 0.4833 · edge bets 16: won 75%, ROI +42% | — |
| XRP | 597 windows · right 73% vs Kalshi 74% · logloss 0.5189 vs 0.5179 · edge bets 19: won 32%, ROI -40% | 1526 windows · right 76% vs Kalshi 76% · logloss 0.4887 vs 0.4888 · edge bets 1: won 0%, ROI -100% | — |
| ETH | 598 windows · right 73% vs Kalshi 73% · logloss 0.5266 vs 0.5258 · edge bets 19: won 58%, ROI +5% | 1530 windows · right 76% vs Kalshi 76% · logloss 0.4959 vs 0.4947 · edge bets 1: won 100%, ROI +96% | — |
| BTC | 598 windows · right 73% vs Kalshi 74% · logloss 0.52 vs 0.5182 · edge bets 31: won 52%, ROI -8% | 1529 windows · right 73% vs Kalshi 73% · logloss 0.5226 vs 0.524 · edge bets 26: won 69%, ROI +22% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.5048 vs 0.5053 · edge bets 16: won 69%, ROI +23% | 1530 windows · right 76% vs Kalshi 76% · logloss 0.4908 vs 0.4907 · edge bets 2: won 50%, ROI -4% | — |
| NEAR | 598 windows · right 75% vs Kalshi 76% · logloss 0.4961 vs 0.4971 · edge bets 19: won 68%, ROI +30% | 1527 windows · right 74% vs Kalshi 74% · logloss 0.5065 vs 0.5077 · edge bets 4: won 75%, ROI +37% | — |
| HYPE | 597 windows · right 74% vs Kalshi 74% · logloss 0.5162 vs 0.5177 · edge bets 23: won 52%, ROI -6% | 1527 windows · right 75% vs Kalshi 75% · logloss 0.5043 vs 0.5059 · edge bets 4: won 100%, ROI +70% | — |
| BNB | 598 windows · right 74% vs Kalshi 74% · logloss 0.5191 vs 0.5195 · edge bets 39: won 67%, ROI +21% | 1524 windows · right 76% vs Kalshi 76% · logloss 0.4915 vs 0.4939 · edge bets 35: won 60%, ROI +9% | ✅ |
| ZEC | 597 windows · right 75% vs Kalshi 75% · logloss 0.5022 vs 0.5016 · edge bets 24: won 58%, ROI +6% | 1373 windows · right 75% vs Kalshi 75% · logloss 0.5035 vs 0.5044 · edge bets 1: won 0%, ROI -100% | — |

**All weeks:** 5378 windows · right 74% vs Kalshi 74% · logloss 0.5136 vs 0.5135 · edge bets 224: won 57%, ROI +4%

**All months:** 13591 windows · right 75% vs Kalshi 75% · logloss 0.4983 vs 0.4993 · edge bets 90: won 67%, ROI +21%

| Month | Result |
|---|---|
| 2026-09 | 822 windows · right 76% vs Kalshi 76% · logloss 0.4799 vs 0.4813 · edge bets 6: won 33%, ROI -32% |
| 2026-10 | 8744 windows · right 76% vs Kalshi 75% · logloss 0.4947 vs 0.4954 · edge bets 57: won 70%, ROI +26% |
| 2026-11 | 4025 windows · right 75% vs Kalshi 75% · logloss 0.5099 vs 0.5114 · edge bets 27: won 67%, ROI +19% |

Strongest signals: `sgap` +0.069, `sr1` +0.036, `s_US` -0.034, `s_EU` +0.032, `dmid5` +0.031

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,269, target reached normally 24% | setups 6,834, target reached normally 21% | — |
| XRP | setups 2,493, target reached normally 25% | setups 6,807, target reached normally 21% | — |
| ETH | setups 2,314, target reached normally 23% | setups 6,304, target reached normally 23% | — |
| BTC | setups 2,249, target reached normally 21% | setups 6,118, target reached normally 21% | — |
| SOL | setups 2,389, target reached normally 23% | setups 6,552, target reached normally 22% | — |
| NEAR | setups 2,457, target reached normally 24% | setups 6,504, target reached normally 22% | — |
| HYPE | setups 2,305, target reached normally 21% | setups 6,475, target reached normally 24% | — |
| BNB | setups 2,344, target reached normally 23% | setups 6,363, target reached normally 22% | — |
| ZEC | setups 2,390, target reached normally 19% | setups 6,072, target reached normally 22% | — |

**All weeks:** setups 21,210, target reached normally 22%

**All months:** setups 58,029, target reached normally 22%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,228, target reached normally 58% | setups 14,350, target reached normally 55% | — |
| XRP | setups 5,834, target reached normally 57% | setups 14,420, target reached normally 55% | — |
| ETH | setups 6,107, target reached normally 57% | setups 14,910, target reached normally 56% | — |
| BTC | setups 6,179, target reached normally 57% | setups 15,467, target reached normally 57% | — |
| SOL | setups 6,036, target reached normally 56% | setups 14,571, target reached normally 56% | — |
| NEAR | setups 5,895, target reached normally 57% | setups 14,550, target reached normally 56% | — |
| HYPE | setups 6,064, target reached normally 57% | setups 14,392, target reached normally 56% | — |
| BNB | setups 5,967, target reached normally 58% | setups 14,458, target reached normally 55% | — |
| ZEC | setups 5,844, target reached normally 56% | setups 12,806, target reached normally 56% | — |
