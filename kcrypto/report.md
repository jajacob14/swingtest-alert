# Kalshi crypto 15-min model report
Trained 2026-11-21 22:50 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 301920

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5109 vs 0.5107 · edge bets 2: won 100%, ROI +71% | 3318 windows · right 75% vs Kalshi 75% · logloss 0.5014 vs 0.5015 · edge bets 2: won 50%, ROI -8% | — |
| ETH | 598 windows · right 74% vs Kalshi 74% · logloss 0.513 vs 0.5113 · edge bets 3: won 67%, ROI +27% | 3164 windows · right 77% vs Kalshi 77% · logloss 0.479 vs 0.4783 | — |
| SOL | 597 windows · right 74% vs Kalshi 74% · logloss 0.5094 vs 0.5088 · edge bets 9: won 33%, ROI -40% | 3164 windows · right 76% vs Kalshi 76% · logloss 0.4874 vs 0.4873 | — |
| XRP | 597 windows · right 75% vs Kalshi 75% · logloss 0.5134 vs 0.5122 · edge bets 26: won 54%, ROI -2% | 3161 windows · right 76% vs Kalshi 76% · logloss 0.4827 vs 0.4828 · edge bets 17: won 59%, ROI +10% | — |
| DOGE | 598 windows · right 75% vs Kalshi 75% · logloss 0.5012 vs 0.5006 · edge bets 18: won 56%, ROI +5% | 3162 windows · right 76% vs Kalshi 76% · logloss 0.4782 vs 0.4792 · edge bets 5: won 100%, ROI +91% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5096 vs 0.5087 · edge bets 58: won 53%, ROI -2%

**All months:** 15969 windows · right 76% vs Kalshi 76% · logloss 0.4859 vs 0.486 · edge bets 24: won 67%, ROI +25%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4632 vs 0.4642 · edge bets 4: won 75%, ROI +37% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4718 vs 0.4719 · edge bets 8: won 50%, ROI -4% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.497 vs 0.4969 · edge bets 12: won 75%, ROI +40% |
| 2026-11 | 80 windows · right 75% vs Kalshi 75% · logloss 0.5034 vs 0.5045 |

Strongest signals: `sgap` +0.049, `s_EU` +0.033, `dmid5` +0.027, `m_XRP` +0.019, `tleft` -0.019

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,489, target reached normally 23% | setups 13,342, target reached normally 20% | — |
| ETH | setups 2,442, target reached normally 25% | setups 13,296, target reached normally 20% | — |
| SOL | setups 2,515, target reached normally 22% | setups 13,517, target reached normally 21% | — |
| XRP | setups 2,554, target reached normally 25% | setups 13,808, target reached normally 20% | — |
| DOGE | setups 2,513, target reached normally 22% | setups 13,577, target reached normally 20% | — |

**All weeks:** setups 12,513, target reached normally 23%

**All months:** setups 67,540, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,862, target reached normally 58% | setups 34,130, target reached normally 56% | — |
| ETH | setups 5,717, target reached normally 58% | setups 30,680, target reached normally 55% | — |
| SOL | setups 5,682, target reached normally 56% | setups 30,314, target reached normally 56% | — |
| XRP | setups 5,412, target reached normally 57% | setups 30,493, target reached normally 56% | — |
| DOGE | setups 5,614, target reached normally 56% | setups 30,296, target reached normally 56% | — |
