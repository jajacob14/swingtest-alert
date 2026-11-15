# Kalshi crypto 15-min model report
Trained 2026-11-15 12:51 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 158753

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 76% vs Kalshi 76% · logloss 0.4894 vs 0.4905 · edge bets 5: won 20%, ROI -66% | 2710 windows · right 75% vs Kalshi 75% · logloss 0.4982 vs 0.4979 · edge bets 13: won 77%, ROI +27% | — |
| ETH | 596 windows · right 75% vs Kalshi 75% · logloss 0.5009 vs 0.5004 · edge bets 1: won 100%, ROI +117% | 2556 windows · right 77% vs Kalshi 77% · logloss 0.4707 vs 0.4702 · edge bets 1: won 0%, ROI -100% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.4904 vs 0.4926 · edge bets 3: won 33%, ROI -36% | 2556 windows · right 76% vs Kalshi 76% · logloss 0.4831 vs 0.4829 · edge bets 4: won 50%, ROI -10% | — |
| XRP | 598 windows · right 78% vs Kalshi 77% · logloss 0.477 vs 0.4759 · edge bets 13: won 46%, ROI -15% | 2553 windows · right 76% vs Kalshi 77% · logloss 0.4753 vs 0.4759 · edge bets 32: won 53%, ROI -3% | — |
| DOGE | 598 windows · right 74% vs Kalshi 74% · logloss 0.497 vs 0.4989 · edge bets 6: won 67%, ROI +12% | 2554 windows · right 77% vs Kalshi 77% · logloss 0.4747 vs 0.476 · edge bets 8: won 100%, ROI +90% | — |

**All weeks:** 2988 windows · right 76% vs Kalshi 76% · logloss 0.491 vs 0.4917 · edge bets 28: won 46%, ROI -16%

**All months:** 12929 windows · right 76% vs Kalshi 76% · logloss 0.4807 vs 0.4808 · edge bets 58: won 64%, ROI +14%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4637 vs 0.4642 · edge bets 10: won 50%, ROI -11% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4716 vs 0.4719 · edge bets 28: won 68%, ROI +18% |
| 2026-10 | 6570 windows · right 76% vs Kalshi 76% · logloss 0.4917 vs 0.4916 · edge bets 20: won 65%, ROI +21% |

Strongest signals: `sgap` +0.059, `s_EU` +0.038, `tleft` -0.031, `s_US` -0.028, `dmid5` +0.025

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,517, target reached normally 23% | setups 10,897, target reached normally 19% | — |
| ETH | setups 2,459, target reached normally 26% | setups 10,866, target reached normally 19% | — |
| SOL | setups 2,547, target reached normally 21% | setups 11,037, target reached normally 21% | — |
| XRP | setups 2,565, target reached normally 23% | setups 11,291, target reached normally 20% | — |
| DOGE | setups 2,603, target reached normally 23% | setups 11,024, target reached normally 20% | — |

**All weeks:** setups 12,691, target reached normally 23%

**All months:** setups 55,115, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,651, target reached normally 56% | setups 27,966, target reached normally 55% | — |
| ETH | setups 5,632, target reached normally 56% | setups 24,620, target reached normally 54% | — |
| SOL | setups 5,640, target reached normally 56% | setups 24,503, target reached normally 55% | — |
| XRP | setups 5,494, target reached normally 53% | setups 24,595, target reached normally 55% | — |
| DOGE | setups 5,534, target reached normally 56% | setups 24,342, target reached normally 56% | — |
