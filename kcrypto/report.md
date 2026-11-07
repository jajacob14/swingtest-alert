# Kalshi crypto 15-min model report
Trained 2026-11-07 16:39 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 6878

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 597 windows · right 72% vs Kalshi 72% · logloss 0.5304 vs 0.5324 · edge bets 42: won 60%, ROI +4% | 1965 windows · right 76% vs Kalshi 75% · logloss 0.496 vs 0.4958 · edge bets 96: won 56%, ROI -4% | — |
| ETH | 598 windows · right 75% vs Kalshi 75% · logloss 0.5082 vs 0.5087 · edge bets 36: won 56%, ROI -4% | 1811 windows · right 78% vs Kalshi 78% · logloss 0.462 vs 0.461 · edge bets 43: won 42%, ROI -27% | — |
| SOL | 597 windows · right 75% vs Kalshi 75% · logloss 0.504 vs 0.5041 · edge bets 28: won 39%, ROI -28% | 1811 windows · right 77% vs Kalshi 76% · logloss 0.4812 vs 0.4809 · edge bets 35: won 46%, ROI -19% | — |
| XRP | 598 windows · right 74% vs Kalshi 75% · logloss 0.516 vs 0.5139 · edge bets 11: won 36%, ROI -33% | 1808 windows · right 77% vs Kalshi 77% · logloss 0.467 vs 0.4675 · edge bets 86: won 54%, ROI -5% | — |
| DOGE | 598 windows · right 76% vs Kalshi 76% · logloss 0.4902 vs 0.4932 · edge bets 77: won 58%, ROI +7% | 1809 windows · right 78% vs Kalshi 78% · logloss 0.4605 vs 0.4612 · edge bets 58: won 71%, ROI +30% | ✅ |
| BNB | 598 windows · right 76% vs Kalshi 75% · logloss 0.4917 vs 0.4968 · edge bets 67: won 66%, ROI +17% | 1807 windows · right 76% vs Kalshi 76% · logloss 0.4918 vs 0.4929 · edge bets 187: won 58%, ROI +4% | ✅ |
| HYPE | 598 windows · right 75% vs Kalshi 75% · logloss 0.5046 vs 0.507 · edge bets 36: won 72%, ROI +28% | 1657 windows · right 74% vs Kalshi 74% · logloss 0.4993 vs 0.5019 · edge bets 56: won 70%, ROI +25% | ✅ |

**All weeks:** 4184 windows · right 75% vs Kalshi 75% · logloss 0.5066 vs 0.5082 · edge bets 297: won 59%, ROI +6%

**All months:** 12668 windows · right 76% vs Kalshi 76% · logloss 0.4796 vs 0.4801 · edge bets 561: won 57%, ROI +2%

| Month | Result |
|---|---|
| 2026-08 | 2051 windows · right 77% vs Kalshi 77% · logloss 0.4706 vs 0.4713 · edge bets 93: won 54%, ROI -6% |
| 2026-09 | 6640 windows · right 77% vs Kalshi 77% · logloss 0.4761 vs 0.4773 · edge bets 276: won 58%, ROI +1% |
| 2026-10 | 3977 windows · right 76% vs Kalshi 76% · logloss 0.4904 vs 0.4894 · edge bets 192: won 58%, ROI +7% |

Strongest signals: `sgap` +0.085, `sr1` +0.049, `s_EU` +0.040, `dmid1` -0.036, `m_BNB` +0.028

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 2,341, target reached normally 23% | setups 7,955, target reached normally 18% | — |
| ETH | setups 2,521, target reached normally 23% | setups 7,831, target reached normally 18% | — |
| SOL | setups 2,548, target reached normally 22% | setups 7,978, target reached normally 20% | — |
| XRP | setups 2,478, target reached normally 22% | setups 8,053, target reached normally 19% | — |
| DOGE | setups 2,646, target reached normally 21% | setups 7,951, target reached normally 18% | — |
| BNB | setups 2,545, target reached normally 20% | setups 7,703, target reached normally 21% | — |
| HYPE | setups 2,572, target reached normally 21% | setups 7,413, target reached normally 21% | — |

**All weeks:** setups 17,651, target reached normally 22%

**All months:** setups 54,884, target reached normally 19%

## Wave alerts (buy near the low, cash out before the close)
Either side at 12-60¢ with 4-13 min left. Buy at the ask + fee, sell when the bid is 12¢ higher, otherwise hold to settlement. Alert when expected profit ≥ 3¢.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | setups 6,244, target reached normally 58% | setups 20,497, target reached normally 55% | — |
| ETH | setups 5,777, target reached normally 56% | setups 17,531, target reached normally 53% | — |
| SOL | setups 5,693, target reached normally 56% | setups 17,355, target reached normally 55% | — |
| XRP | setups 5,698, target reached normally 56% | setups 17,581, target reached normally 54% | — |
| DOGE | setups 5,630, target reached normally 55% | setups 17,195, target reached normally 54% | — |
| BNB | setups 5,620, target reached normally 54% | setups 17,310, target reached normally 54% | — |
| HYPE | setups 5,651, target reached normally 56% | setups 15,397, target reached normally 56% | — |
