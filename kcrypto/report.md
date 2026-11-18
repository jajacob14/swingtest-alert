# Kalshi crypto 15-min model report
Trained 2026-11-18 09:58 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 221981

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 76% vs Kalshi 76% · logloss 0.4909 vs 0.4916 · edge bets 5: won 20%, ROI -63% | 2986 windows · right 75% vs Kalshi 75% · logloss 0.5017 vs 0.5019 · edge bets 6: won 50%, ROI -15% | — |
| ETH | 597 windows · right 75% vs Kalshi 75% · logloss 0.5006 vs 0.4989 · edge bets 16: won 50%, ROI -5% | 2832 windows · right 77% vs Kalshi 77% · logloss 0.4784 vs 0.4777 · edge bets 7: won 14%, ROI -72% | — |
| SOL | 598 windows · right 75% vs Kalshi 75% · logloss 0.5035 vs 0.5038 · edge bets 4: won 25%, ROI -52% | 2832 windows · right 76% vs Kalshi 76% · logloss 0.4859 vs 0.486 | — |
| XRP | 598 windows · right 76% vs Kalshi 76% · logloss 0.4954 vs 0.4929 · edge bets 42: won 50%, ROI -7% | 2829 windows · right 76% vs Kalshi 76% · logloss 0.4812 vs 0.4812 · edge bets 44: won 52%, ROI -1% | — |
| DOGE | 598 windows · right 73% vs Kalshi 73% · logloss 0.5245 vs 0.5273 · edge bets 19: won 63%, ROI +10% | 2830 windows · right 77% vs Kalshi 76% · logloss 0.477 vs 0.4781 · edge bets 5: won 80%, ROI +49% | — |

**All weeks:** 2988 windows · right 75% vs Kalshi 75% · logloss 0.503 vs 0.5029 · edge bets 86: won 50%, ROI -8%

**All months:** 14309 windows · right 76% vs Kalshi 76% · logloss 0.4851 vs 0.4853 · edge bets 62: won 50%, ROI -6%

| Month | Result |
|---|---|
| 2026-08 | 1616 windows · right 78% vs Kalshi 78% · logloss 0.4629 vs 0.4642 · edge bets 8: won 62%, ROI +18% |
| 2026-09 | 4743 windows · right 77% vs Kalshi 77% · logloss 0.4716 vs 0.4719 · edge bets 23: won 48%, ROI -11% |
| 2026-10 | 7950 windows · right 75% vs Kalshi 75% · logloss 0.498 vs 0.4978 · edge bets 31: won 48%, ROI -9% |

Strongest signals: `sgap` +0.060, `s_EU` +0.029, `tleft` -0.024, `dmid5` +0.023, `m_XRP` +0.021

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,455, target reached normally 21% | setups 11,970, target reached normally 20% | — |
| ETH | setups 2,456, target reached normally 26% | setups 11,928, target reached normally 20% | — |
| SOL | setups 2,500, target reached normally 24% | setups 12,102, target reached normally 21% | — |
| XRP | setups 2,552, target reached normally 23% | setups 12,444, target reached normally 20% | — |
| DOGE | setups 2,511, target reached normally 24% | setups 12,168, target reached normally 20% | — |

**All weeks:** setups 12,474, target reached normally 24%

**All months:** setups 60,612, target reached normally 20%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 5,792, target reached normally 56% | setups 30,789, target reached normally 55% | — |
| ETH | setups 5,583, target reached normally 56% | setups 27,405, target reached normally 55% | — |
| SOL | setups 5,729, target reached normally 56% | setups 27,214, target reached normally 56% | — |
| XRP | setups 5,512, target reached normally 55% | setups 27,279, target reached normally 55% | — |
| DOGE | setups 5,583, target reached normally 57% | setups 27,038, target reached normally 56% | — |
