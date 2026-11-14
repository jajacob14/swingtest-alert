# Kalshi crypto 15-min model report
Trained 2026-11-14 02:18 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 127268

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 75% vs Kalshi 76% · logloss 0.4914 vs 0.4913 · edge bets 20: won 55%, ROI -7% | 2572 windows · right 75% vs Kalshi 75% · logloss 0.4978 vs 0.4979 · edge bets 10: won 60%, ROI +0% | — |
| ETH | 597 windows · right 75% vs Kalshi 75% · logloss 0.5045 vs 0.5039 · edge bets 6: won 50%, ROI -6% | 2418 windows · right 77% vs Kalshi 77% · logloss 0.4688 vs 0.4685 | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.5031 vs 0.5036 · edge bets 8: won 38%, ROI -30% | 2418 windows · right 76% vs Kalshi 76% · logloss 0.4823 vs 0.4825 | — |
| XRP | 598 windows · right 75% vs Kalshi 75% · logloss 0.51 vs 0.5069 · edge bets 25: won 72%, ROI +32% | 2415 windows · right 77% vs Kalshi 77% · logloss 0.4721 vs 0.4729 · edge bets 28: won 57%, ROI +6% | — |
| DOGE | 598 windows · right 75% vs Kalshi 75% · logloss 0.503 vs 0.5023 · edge bets 5: won 40%, ROI -29% | 2416 windows · right 77% vs Kalshi 77% · logloss 0.4735 vs 0.4748 · edge bets 3: won 100%, ROI +83% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.5024 vs 0.5016 · edge bets 64: won 58%, ROI +4%

**All months:** 12239 windows · right 76% vs Kalshi 76% · logloss 0.4793 vs 0.4797 · edge bets 41: won 61%, ROI +10%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4633 vs 0.4642 · edge bets 6: won 50%, ROI -8% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4714 vs 0.4719 · edge bets 17: won 59%, ROI +6% |
| 2026-10 | 5880 windows · right 76% vs Kalshi 76% · logloss 0.4902 vs 0.4904 · edge bets 18: won 67%, ROI +21% |

Strongest signals: `sgap` +0.057, `s_EU` +0.035, `tleft` -0.027, `dmid5` +0.023, `m_XRP` +0.022

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,493, target reached normally 23% | setups 10,387, target reached normally 19% | — |
| ETH | setups 2,431, target reached normally 25% | setups 10,351, target reached normally 19% | — |
| SOL | setups 2,543, target reached normally 23% | setups 10,502, target reached normally 21% | — |
| XRP | setups 2,556, target reached normally 23% | setups 10,698, target reached normally 20% | — |
| DOGE | setups 2,620, target reached normally 24% | setups 10,455, target reached normally 20% | — |

**All weeks:** setups 12,643, target reached normally 24%

**All months:** setups 52,393, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,632, target reached normally 55% | setups 26,565, target reached normally 55% | — |
| ETH | setups 5,676, target reached normally 56% | setups 23,277, target reached normally 54% | — |
| SOL | setups 5,581, target reached normally 56% | setups 23,166, target reached normally 55% | — |
| XRP | setups 5,492, target reached normally 55% | setups 23,274, target reached normally 55% | — |
| DOGE | setups 5,505, target reached normally 56% | setups 22,997, target reached normally 56% | — |
