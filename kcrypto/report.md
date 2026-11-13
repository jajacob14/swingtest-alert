# Kalshi crypto 15-min model report
Trained 2026-11-13 03:16 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 104495

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 76% vs Kalshi 76% · logloss 0.4845 vs 0.4844 · edge bets 29: won 66%, ROI +16% | 2480 windows · right 76% vs Kalshi 76% · logloss 0.4948 vs 0.495 · edge bets 8: won 75%, ROI +24% | — |
| ETH | 597 windows · right 76% vs Kalshi 76% · logloss 0.5004 vs 0.5 · edge bets 8: won 25%, ROI -53% | 2326 windows · right 78% vs Kalshi 78% · logloss 0.4662 vs 0.4659 · edge bets 1: won 0%, ROI -100% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.4982 vs 0.4975 · edge bets 14: won 43%, ROI -21% | 2326 windows · right 77% vs Kalshi 77% · logloss 0.4817 vs 0.4817 | — |
| XRP | 598 windows · right 75% vs Kalshi 75% · logloss 0.5091 vs 0.5066 · edge bets 17: won 65%, ROI +22% | 2323 windows · right 77% vs Kalshi 77% · logloss 0.469 vs 0.4697 · edge bets 18: won 56%, ROI +5% | — |
| DOGE | 597 windows · right 77% vs Kalshi 77% · logloss 0.4815 vs 0.4799 · edge bets 28: won 61%, ROI +16% | 2324 windows · right 77% vs Kalshi 77% · logloss 0.4721 vs 0.4734 · edge bets 3: won 100%, ROI +97% | — |

**All weeks:** 2988 windows · right 76% vs Kalshi 76% · logloss 0.4947 vs 0.4936 · edge bets 96: won 57%, ROI +6%

**All months:** 11779 windows · right 77% vs Kalshi 77% · logloss 0.4771 vs 0.4775 · edge bets 30: won 63%, ROI +15%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4632 vs 0.4642 · edge bets 6: won 50%, ROI -7% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4716 vs 0.4719 · edge bets 15: won 60%, ROI +8% |
| 2026-10 | 5420 windows · right 76% vs Kalshi 76% · logloss 0.4863 vs 0.4865 · edge bets 9: won 78%, ROI +43% |

Strongest signals: `sgap` +0.056, `tleft` -0.030, `s_EU` +0.028, `m_XRP` +0.027, `dmid5` +0.022

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,437, target reached normally 22% | setups 10,091, target reached normally 19% | — |
| ETH | setups 2,465, target reached normally 23% | setups 10,007, target reached normally 19% | — |
| SOL | setups 2,544, target reached normally 22% | setups 10,136, target reached normally 21% | — |
| XRP | setups 2,526, target reached normally 23% | setups 10,313, target reached normally 20% | — |
| DOGE | setups 2,642, target reached normally 22% | setups 10,100, target reached normally 20% | — |

**All weeks:** setups 12,614, target reached normally 22%

**All months:** setups 50,647, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,822, target reached normally 55% | setups 25,508, target reached normally 55% | — |
| ETH | setups 5,728, target reached normally 55% | setups 22,320, target reached normally 54% | — |
| SOL | setups 5,618, target reached normally 56% | setups 22,258, target reached normally 55% | — |
| XRP | setups 5,542, target reached normally 55% | setups 22,339, target reached normally 55% | — |
| DOGE | setups 5,520, target reached normally 54% | setups 22,074, target reached normally 55% | — |
