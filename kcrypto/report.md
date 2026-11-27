# Kalshi crypto 15-min model report
Trained 2026-11-27 15:20 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 426790

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | 598 windows · right 74% vs Kalshi 74% · logloss 0.5208 vs 0.5208 · edge bets 11: won 46%, ROI -18% | 3700 windows · right 76% vs Kalshi 76% · logloss 0.4807 vs 0.4818 · edge bets 10: won 60%, ROI +10% | — |
| XRP | 597 windows · right 74% vs Kalshi 74% · logloss 0.5159 vs 0.515 · edge bets 7: won 57%, ROI -2% | 3699 windows · right 76% vs Kalshi 76% · logloss 0.4865 vs 0.4868 · edge bets 2: won 100%, ROI +72% | — |
| ETH | 598 windows · right 73% vs Kalshi 74% · logloss 0.527 vs 0.5263 · edge bets 12: won 58%, ROI +6% | 3702 windows · right 76% vs Kalshi 76% · logloss 0.4833 vs 0.4828 | — |
| BTC | 598 windows · right 74% vs Kalshi 74% · logloss 0.5171 vs 0.5169 · edge bets 11: won 27%, ROI -48% | 3794 windows · right 74% vs Kalshi 74% · logloss 0.5054 vs 0.5059 · edge bets 11: won 64%, ROI +4% | — |
| SOL | 597 windows · right 76% vs Kalshi 76% · logloss 0.4961 vs 0.4968 · edge bets 13: won 69%, ROI +30% | 3702 windows · right 76% vs Kalshi 76% · logloss 0.489 vs 0.4894 | — |

**All weeks:** 2988 windows · right 74% vs Kalshi 74% · logloss 0.5154 vs 0.5152 · edge bets 54: won 52%, ROI -5%

**All months:** 18597 windows · right 76% vs Kalshi 76% · logloss 0.4892 vs 0.4895 · edge bets 23: won 65%, ROI +12%

| Month | Result |
|---|---|
| 2026-08 | 1554 windows · right 78% vs Kalshi 78% · logloss 0.4622 vs 0.4625 · edge bets 2: won 100%, ROI +84% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4716 vs 0.4719 · edge bets 8: won 75%, ROI +26% |
| 2026-10 | 9530 windows · right 75% vs Kalshi 75% · logloss 0.4967 vs 0.4969 · edge bets 11: won 64%, ROI +10% |
| 2026-11 | 2770 windows · right 74% vs Kalshi 74% · logloss 0.5095 vs 0.5107 · edge bets 2: won 0%, ROI -100% |

Strongest signals: `sgap` +0.054, `dmid5` +0.036, `s_EU` +0.034, `sr1` +0.024, `s_US` -0.022

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 2,285, target reached normally 23% | setups 15,988, target reached normally 20% | — |
| XRP | setups 2,513, target reached normally 24% | setups 16,084, target reached normally 21% | — |
| ETH | setups 2,318, target reached normally 23% | setups 15,607, target reached normally 20% | — |
| BTC | setups 2,277, target reached normally 21% | setups 15,298, target reached normally 20% | — |
| SOL | setups 2,438, target reached normally 23% | setups 15,836, target reached normally 21% | — |

**All weeks:** setups 11,831, target reached normally 23%

**All months:** setups 78,813, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| DOGE | setups 6,262, target reached normally 59% | setups 35,292, target reached normally 56% | — |
| XRP | setups 5,861, target reached normally 57% | setups 35,575, target reached normally 56% | — |
| ETH | setups 6,127, target reached normally 58% | setups 35,772, target reached normally 55% | — |
| BTC | setups 6,149, target reached normally 58% | setups 38,967, target reached normally 56% | — |
| SOL | setups 6,026, target reached normally 55% | setups 35,343, target reached normally 56% | — |
