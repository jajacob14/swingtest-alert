# Kalshi crypto 15-min model report
Trained 2026-11-19 20:31 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 254542

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 75% vs Kalshi 75% · logloss 0.5064 vs 0.5069 · edge bets 2: won 0%, ROI -100% | 3117 windows · right 75% vs Kalshi 75% · logloss 0.5018 vs 0.5018 · edge bets 4: won 25%, ROI -56% | — |
| ETH | 598 windows · right 75% vs Kalshi 75% · logloss 0.5074 vs 0.5052 · edge bets 4: won 50%, ROI -8% | 2963 windows · right 77% vs Kalshi 77% · logloss 0.48 vs 0.4796 | — |
| SOL | 598 windows · right 74% vs Kalshi 73% · logloss 0.5236 vs 0.5234 · edge bets 4: won 25%, ROI -52% | 2963 windows · right 76% vs Kalshi 76% · logloss 0.4866 vs 0.4865 | — |
| XRP | 597 windows · right 74% vs Kalshi 75% · logloss 0.5144 vs 0.5101 · edge bets 52: won 46%, ROI -15% | 2960 windows · right 76% vs Kalshi 76% · logloss 0.4815 vs 0.4818 · edge bets 16: won 56%, ROI +4% | — |
| DOGE | 598 windows · right 73% vs Kalshi 74% · logloss 0.5159 vs 0.5167 · edge bets 17: won 59%, ROI +6% | 2961 windows · right 77% vs Kalshi 76% · logloss 0.4766 vs 0.4778 · edge bets 2: won 100%, ROI +87% | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5135 vs 0.5125 · edge bets 79: won 47%, ROI -14%

**All months:** 14964 windows · right 76% vs Kalshi 76% · logloss 0.4856 vs 0.4857 · edge bets 22: won 55%, ROI +0%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4639 vs 0.4642 · edge bets 5: won 60%, ROI +13% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4717 vs 0.4719 · edge bets 9: won 44%, ROI -16% |
| 2026-10 | 8605 windows · right 75% vs Kalshi 75% · logloss 0.4976 vs 0.4977 · edge bets 8: won 62%, ROI +10% |

Strongest signals: `sgap` +0.056, `s_US` -0.026, `dmid5` +0.026, `s_EU` +0.025, `tleft` -0.023

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,483, target reached normally 23% | setups 12,532, target reached normally 19% | — |
| ETH | setups 2,517, target reached normally 26% | setups 12,487, target reached normally 20% | — |
| SOL | setups 2,495, target reached normally 23% | setups 12,676, target reached normally 21% | — |
| XRP | setups 2,537, target reached normally 25% | setups 13,021, target reached normally 20% | — |
| DOGE | setups 2,542, target reached normally 22% | setups 12,745, target reached normally 20% | — |

**All weeks:** setups 12,574, target reached normally 24%

**All months:** setups 63,461, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,850, target reached normally 58% | setups 32,079, target reached normally 56% | — |
| ETH | setups 5,610, target reached normally 57% | setups 28,683, target reached normally 55% | — |
| SOL | setups 5,756, target reached normally 58% | setups 28,421, target reached normally 56% | — |
| XRP | setups 5,528, target reached normally 56% | setups 28,488, target reached normally 55% | — |
| DOGE | setups 5,629, target reached normally 57% | setups 28,258, target reached normally 56% | — |
