# Kalshi crypto 15-min model report
Trained 2026-11-17 10:55 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 200855

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 75% vs Kalshi 75% · logloss 0.497 vs 0.4972 · edge bets 5: won 20%, ROI -64% | 2894 windows · right 75% vs Kalshi 75% · logloss 0.4994 vs 0.499 · edge bets 19: won 53%, ROI -6% | — |
| ETH | 598 windows · right 75% vs Kalshi 75% · logloss 0.5077 vs 0.5057 · edge bets 7: won 29%, ROI -45% | 2740 windows · right 77% vs Kalshi 77% · logloss 0.4752 vs 0.4745 · edge bets 15: won 33%, ROI -35% | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.4883 vs 0.4892 · edge bets 2: won 50%, ROI -2% | 2740 windows · right 76% vs Kalshi 76% · logloss 0.4862 vs 0.4859 · edge bets 7: won 57%, ROI +10% | — |
| XRP | 598 windows · right 77% vs Kalshi 77% · logloss 0.4773 vs 0.4757 · edge bets 42: won 55%, ROI -1% | 2737 windows · right 76% vs Kalshi 76% · logloss 0.4802 vs 0.4802 · edge bets 112: won 55%, ROI +2% | — |
| DOGE | 598 windows · right 73% vs Kalshi 73% · logloss 0.5194 vs 0.5228 · edge bets 13: won 54%, ROI -7% | 2738 windows · right 76% vs Kalshi 76% · logloss 0.4781 vs 0.4793 · edge bets 22: won 59%, ROI +10% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.4979 vs 0.4981 · edge bets 69: won 49%, ROI -11%

**All months:** 13849 windows · right 76% vs Kalshi 76% · logloss 0.4841 vs 0.4841 · edge bets 175: won 53%, ROI -1%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4633 vs 0.4642 · edge bets 23: won 65%, ROI +24% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4718 vs 0.4719 · edge bets 59: won 48%, ROI -13% |
| 2026-10 | 7490 windows · right 75% vs Kalshi 75% · logloss 0.4967 vs 0.4963 · edge bets 93: won 54%, ROI +1% |

Strongest signals: `sgap` +0.061, `s_EU` +0.033, `tleft` -0.027, `sr5` +0.021, `m_XRP` +0.020

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,443, target reached normally 22% | setups 11,614, target reached normally 19% | — |
| ETH | setups 2,391, target reached normally 26% | setups 11,558, target reached normally 20% | — |
| SOL | setups 2,492, target reached normally 23% | setups 11,758, target reached normally 21% | — |
| XRP | setups 2,544, target reached normally 22% | setups 12,053, target reached normally 20% | — |
| DOGE | setups 2,564, target reached normally 24% | setups 11,769, target reached normally 20% | — |

**All weeks:** setups 12,434, target reached normally 23%

**All months:** setups 58,752, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,809, target reached normally 57% | setups 29,812, target reached normally 55% | — |
| ETH | setups 5,677, target reached normally 57% | setups 26,483, target reached normally 54% | — |
| SOL | setups 5,721, target reached normally 56% | setups 26,304, target reached normally 55% | — |
| XRP | setups 5,546, target reached normally 54% | setups 26,394, target reached normally 55% | — |
| DOGE | setups 5,545, target reached normally 58% | setups 26,171, target reached normally 56% | — |
