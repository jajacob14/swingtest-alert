# Kalshi crypto 15-min model report
Trained 2026-11-24 05:25 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 0

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| ETH | 592 windows · right 74% vs Kalshi 74% · logloss 0.5098 vs 0.5075 | 1164 windows · right 76% vs Kalshi 76% · logloss 0.4949 vs 0.4934 · edge bets 5: won 80%, ROI +49% | — |
| BTC | 592 windows · right 74% vs Kalshi 74% · logloss 0.5092 vs 0.5103 · edge bets 2: won 50%, ROI -29% | 1163 windows · right 74% vs Kalshi 74% · logloss 0.5202 vs 0.521 · edge bets 28: won 64%, ROI +8% | — |
| SOL | 595 windows · right 75% vs Kalshi 75% · logloss 0.51 vs 0.5108 | 1164 windows · right 77% vs Kalshi 76% · logloss 0.4853 vs 0.4846 · edge bets 1: won 0%, ROI -100% | — |
| XRP | 593 windows · right 75% vs Kalshi 75% · logloss 0.5179 vs 0.5166 · edge bets 1: won 100%, ROI +104% | 1160 windows · right 77% vs Kalshi 77% · logloss 0.4774 vs 0.4779 · edge bets 3: won 67%, ROI +23% | — |
| NEAR | 596 windows · right 77% vs Kalshi 76% · logloss 0.4833 vs 0.4856 · edge bets 12: won 58%, ROI +8% | 1161 windows · right 74% vs Kalshi 74% · logloss 0.506 vs 0.5083 · edge bets 9: won 78%, ROI +35% | — |
| HYPE | 596 windows · right 74% vs Kalshi 73% · logloss 0.5302 vs 0.5309 · edge bets 7: won 71%, ROI +26% | 1161 windows · right 75% vs Kalshi 75% · logloss 0.5029 vs 0.505 · edge bets 13: won 69%, ROI +27% | — |
| DOGE | 598 windows · right 76% vs Kalshi 76% · logloss 0.4932 vs 0.4925 · edge bets 26: won 69%, ROI +27% | 1159 windows · right 77% vs Kalshi 76% · logloss 0.4757 vs 0.4778 · edge bets 36: won 64%, ROI +19% | — |
| BNB | 599 windows · right 77% vs Kalshi 76% · logloss 0.4769 vs 0.4776 · edge bets 16: won 81%, ROI +54% | 1158 windows · right 76% vs Kalshi 75% · logloss 0.4915 vs 0.4946 · edge bets 70: won 66%, ROI +20% | ✅ |
| ZEC | 600 windows · right 73% vs Kalshi 73% · logloss 0.5069 vs 0.5057 · edge bets 8: won 38%, ROI -28% | 1007 windows · right 75% vs Kalshi 75% · logloss 0.5066 vs 0.506 · edge bets 6: won 50%, ROI -5% | — |

**All weeks:** 5361 windows · right 75% vs Kalshi 75% · logloss 0.5042 vs 0.5042 · edge bets 72: won 67%, ROI +23%

**All months:** 10297 windows · right 76% vs Kalshi 75% · logloss 0.4955 vs 0.4964 · edge bets 171: won 66%, ROI +18%

| Month | Result |
|---|---|
| 2026-09 | 822 windows · right 76% vs Kalshi 76% · logloss 0.48 vs 0.4813 · edge bets 13: won 54%, ROI +5% |
| 2026-10 | 8744 windows · right 76% vs Kalshi 75% · logloss 0.495 vs 0.4954 · edge bets 141: won 65%, ROI +18% |
| 2026-11 | 731 windows · right 74% vs Kalshi 74% · logloss 0.5193 vs 0.5258 · edge bets 17: won 76%, ROI +29% |

Strongest signals: `sgap` +0.094, `sr1` +0.047, `s_EU` +0.035, `tleft` -0.032, `dmid5` +0.028

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| ETH | setups 2,435, target reached normally 24% | setups 4,785, target reached normally 22% | — |
| BTC | setups 2,423, target reached normally 23% | setups 4,682, target reached normally 20% | — |
| SOL | setups 2,484, target reached normally 22% | setups 5,011, target reached normally 21% | — |
| XRP | setups 2,527, target reached normally 26% | setups 5,292, target reached normally 20% | — |
| NEAR | setups 2,596, target reached normally 23% | setups 4,857, target reached normally 21% | — |
| HYPE | setups 2,432, target reached normally 24% | setups 4,926, target reached normally 24% | — |
| DOGE | setups 2,450, target reached normally 22% | setups 5,251, target reached normally 21% | — |
| BNB | setups 2,517, target reached normally 21% | setups 4,809, target reached normally 22% | — |
| ZEC | setups 2,338, target reached normally 21% | setups 4,471, target reached normally 22% | — |

**All weeks:** setups 22,202, target reached normally 23%

**All months:** setups 44,084, target reached normally 22%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| ETH | setups 5,822, target reached normally 56% | setups 11,325, target reached normally 56% | — |
| BTC | setups 5,874, target reached normally 58% | setups 11,670, target reached normally 56% | — |
| SOL | setups 5,802, target reached normally 56% | setups 11,012, target reached normally 56% | — |
| XRP | setups 5,543, target reached normally 56% | setups 10,942, target reached normally 55% | — |
| NEAR | setups 5,638, target reached normally 56% | setups 11,087, target reached normally 56% | — |
| HYPE | setups 5,810, target reached normally 57% | setups 10,908, target reached normally 56% | — |
| DOGE | setups 5,811, target reached normally 56% | setups 10,807, target reached normally 55% | — |
| BNB | setups 5,660, target reached normally 54% | setups 10,987, target reached normally 55% | — |
| ZEC | setups 5,948, target reached normally 57% | setups 9,352, target reached normally 56% | — |
