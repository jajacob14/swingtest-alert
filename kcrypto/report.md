# Kalshi crypto 15-min model report
Trained 2026-11-16 11:53 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 179744

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 75% vs Kalshi 75% · logloss 0.5007 vs 0.5017 · edge bets 3: won 0%, ROI -100% | 2802 windows · right 75% vs Kalshi 75% · logloss 0.4991 vs 0.499 · edge bets 8: won 38%, ROI -37% | — |
| ETH | 598 windows · right 74% vs Kalshi 74% · logloss 0.5142 vs 0.5125 · edge bets 2: won 0%, ROI -100% | 2648 windows · right 77% vs Kalshi 77% · logloss 0.4721 vs 0.4717 | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.4895 vs 0.4915 · edge bets 2: won 50%, ROI -2% | 2648 windows · right 76% vs Kalshi 76% · logloss 0.4838 vs 0.4839 · edge bets 1: won 100%, ROI +96% | — |
| XRP | 598 windows · right 77% vs Kalshi 77% · logloss 0.4835 vs 0.4812 · edge bets 41: won 51%, ROI -6% | 2645 windows · right 77% vs Kalshi 77% · logloss 0.4747 vs 0.4752 · edge bets 25: won 64%, ROI +18% | — |
| DOGE | 597 windows · right 74% vs Kalshi 74% · logloss 0.5146 vs 0.5163 · edge bets 7: won 57%, ROI -2% | 2646 windows · right 77% vs Kalshi 76% · logloss 0.4768 vs 0.4782 · edge bets 4: won 100%, ROI +79% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.5005 vs 0.5007 · edge bets 55: won 47%, ROI -14%

**All months:** 13389 windows · right 76% vs Kalshi 76% · logloss 0.4816 vs 0.4819 · edge bets 38: won 63%, ROI +14%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4633 vs 0.4642 · edge bets 6: won 50%, ROI -7% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4715 vs 0.4719 · edge bets 15: won 60%, ROI +6% |
| 2026-10 | 7030 windows · right 76% vs Kalshi 76% · logloss 0.4929 vs 0.4929 · edge bets 17: won 71%, ROI +28% |

Strongest signals: `sgap` +0.060, `s_EU` +0.030, `tleft` -0.030, `s_US` -0.021, `sr5` +0.019

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,477, target reached normally 24% | setups 11,273, target reached normally 19% | — |
| ETH | setups 2,437, target reached normally 27% | setups 11,224, target reached normally 20% | — |
| SOL | setups 2,516, target reached normally 21% | setups 11,406, target reached normally 21% | — |
| XRP | setups 2,553, target reached normally 21% | setups 11,679, target reached normally 20% | — |
| DOGE | setups 2,599, target reached normally 24% | setups 11,407, target reached normally 20% | — |

**All weeks:** setups 12,582, target reached normally 23%

**All months:** setups 56,989, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,745, target reached normally 57% | setups 28,906, target reached normally 55% | — |
| ETH | setups 5,660, target reached normally 57% | setups 25,548, target reached normally 54% | — |
| SOL | setups 5,695, target reached normally 56% | setups 25,390, target reached normally 56% | — |
| XRP | setups 5,586, target reached normally 54% | setups 25,508, target reached normally 55% | — |
| DOGE | setups 5,530, target reached normally 57% | setups 25,286, target reached normally 56% | — |
