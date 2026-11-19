# Kalshi crypto 15-min model report
Trained 2026-11-19 09:00 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 242722

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 598 windows · right 75% vs Kalshi 75% · logloss 0.502 vs 0.5019 · edge bets 1: won 0%, ROI -100% | 3071 windows · right 75% vs Kalshi 75% · logloss 0.5017 vs 0.5017 · edge bets 3: won 33%, ROI -44% | — |
| ETH | 597 windows · right 75% vs Kalshi 75% · logloss 0.5013 vs 0.4994 · edge bets 7: won 71%, ROI +32% | 2917 windows · right 77% vs Kalshi 77% · logloss 0.4787 vs 0.4782 | — |
| SOL | 597 windows · right 74% vs Kalshi 74% · logloss 0.5179 vs 0.5181 · edge bets 2: won 0%, ROI -100% | 2917 windows · right 76% vs Kalshi 76% · logloss 0.4864 vs 0.4864 | — |
| XRP | 597 windows · right 75% vs Kalshi 75% · logloss 0.5074 vs 0.5016 · edge bets 74: won 50%, ROI -9% | 2914 windows · right 76% vs Kalshi 76% · logloss 0.4822 vs 0.4824 · edge bets 12: won 50%, ROI -6% | — |
| DOGE | 598 windows · right 73% vs Kalshi 73% · logloss 0.5257 vs 0.5274 · edge bets 10: won 70%, ROI +24% | 2915 windows · right 76% vs Kalshi 76% · logloss 0.4776 vs 0.4788 | — |

**All weeks:** 2987 windows · right 74% vs Kalshi 74% · logloss 0.5109 vs 0.5097 · edge bets 94: won 52%, ROI -6%

**All months:** 14734 windows · right 76% vs Kalshi 76% · logloss 0.4856 vs 0.4858 · edge bets 15: won 47%, ROI -15%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4636 vs 0.4642 · edge bets 5: won 60%, ROI +13% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4717 vs 0.4719 · edge bets 6: won 33%, ROI -35% |
| 2026-10 | 8375 windows · right 75% vs Kalshi 75% · logloss 0.498 vs 0.4981 · edge bets 4: won 50%, ROI -20% |

Strongest signals: `sgap` +0.052, `dmid5` +0.024, `tleft` -0.023, `s_EU` +0.023, `s_US` -0.020

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,455, target reached normally 22% | setups 12,320, target reached normally 19% | — |
| ETH | setups 2,483, target reached normally 26% | setups 12,282, target reached normally 20% | — |
| SOL | setups 2,487, target reached normally 24% | setups 12,463, target reached normally 21% | — |
| XRP | setups 2,522, target reached normally 23% | setups 12,798, target reached normally 20% | — |
| DOGE | setups 2,512, target reached normally 23% | setups 12,539, target reached normally 20% | — |

**All weeks:** setups 12,459, target reached normally 24%

**All months:** setups 62,402, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,851, target reached normally 57% | setups 31,642, target reached normally 56% | — |
| ETH | setups 5,621, target reached normally 57% | setups 28,250, target reached normally 55% | — |
| SOL | setups 5,730, target reached normally 57% | setups 28,020, target reached normally 56% | — |
| XRP | setups 5,509, target reached normally 55% | setups 28,093, target reached normally 56% | — |
| DOGE | setups 5,605, target reached normally 58% | setups 27,863, target reached normally 56% | — |
