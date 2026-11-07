# Kalshi crypto 15-min model report
Trained 2026-11-07 04:36 ET

Model = Kalshi's own price + what it misses (quote changes, spread, volume, order flow, big-money flow, time left, session, market).
**Weeks** = trained on the older 70% of the last 3 weeks, tested on the newest 30%. **Months** = trained on the 3 weeks, tested on older months it never saw. Edge bets buy at the ask + fee when the model beats it by 4+ pts (≤70¢), held to settlement.
Order-flow coverage: 0% of rows · commodity whale events on file: 0

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | 592 windows · right 72% vs Kalshi 72% · logloss 0.5286 vs 0.5294 · edge bets 31: won 55%, ROI -6% | 1917 windows · right 76% vs Kalshi 76% · logloss 0.4934 vs 0.494 · edge bets 59: won 63%, ROI +4% | — |
| ETH | 595 windows · right 75% vs Kalshi 75% · logloss 0.5102 vs 0.5088 · edge bets 30: won 57%, ROI +1% | 1763 windows · right 78% vs Kalshi 78% · logloss 0.4618 vs 0.4609 · edge bets 22: won 41%, ROI -30% | — |
| SOL | 593 windows · right 75% vs Kalshi 75% · logloss 0.5014 vs 0.5005 · edge bets 18: won 44%, ROI -19% | 1763 windows · right 77% vs Kalshi 77% · logloss 0.4798 vs 0.4801 · edge bets 21: won 52%, ROI -9% | — |
| XRP | 595 windows · right 75% vs Kalshi 75% · logloss 0.5118 vs 0.5103 · edge bets 3: won 33%, ROI -36% | 1760 windows · right 77% vs Kalshi 77% · logloss 0.4664 vs 0.4671 · edge bets 40: won 52%, ROI -4% | — |
| DOGE | 596 windows · right 76% vs Kalshi 76% · logloss 0.4905 vs 0.4932 · edge bets 48: won 54%, ROI +2% | 1761 windows · right 78% vs Kalshi 78% · logloss 0.4603 vs 0.4612 · edge bets 41: won 76%, ROI +40% | ✅ |
| BNB | 597 windows · right 75% vs Kalshi 75% · logloss 0.5023 vs 0.5068 · edge bets 55: won 62%, ROI +11% | 1759 windows · right 76% vs Kalshi 76% · logloss 0.4937 vs 0.4954 · edge bets 146: won 61%, ROI +9% | ✅ |
| HYPE | 599 windows · right 75% vs Kalshi 75% · logloss 0.5074 vs 0.5092 · edge bets 26: won 73%, ROI +32% | 1609 windows · right 75% vs Kalshi 74% · logloss 0.4974 vs 0.5001 · edge bets 34: won 74%, ROI +33% | ✅ |

**All weeks:** 4167 windows · right 75% vs Kalshi 75% · logloss 0.5075 vs 0.5084 · edge bets 211: won 58%, ROI +4%

**All months:** 12332 windows · right 76% vs Kalshi 76% · logloss 0.4789 vs 0.4797 · edge bets 363: won 61%, ROI +9%

| Month | Result |
|---|---|
| 2026-08 | 2051 windows · right 77% vs Kalshi 77% · logloss 0.4702 vs 0.4713 · edge bets 62: won 55%, ROI -3% |
| 2026-09 | 6640 windows · right 77% vs Kalshi 77% · logloss 0.476 vs 0.4773 · edge bets 181: won 62%, ROI +10% |
| 2026-10 | 3641 windows · right 76% vs Kalshi 76% · logloss 0.4892 vs 0.489 · edge bets 120: won 63%, ROI +14% |

Strongest signals: `sgap` +0.087, `sr1` +0.051, `s_EU` +0.042, `dmid1` -0.037, `m_BNB` +0.031

## Cheap-spike alerts
Contracts at 20¢ or less, 2-13 min left. Buy at the ask + fee, sell at 2x (at least +10¢) if the bid gets there before the close, otherwise hold to settlement. Alert when expected profit ≥ 3¢ per contract.

| Market | Weeks test | Months test | Proven |
|---|---|---|---|
| BTC | cheap rows 2,382, spike-to-target normally 22% | cheap rows 7,791, spike-to-target normally 18% | — |
| ETH | cheap rows 2,509, spike-to-target normally 24% | cheap rows 7,639, spike-to-target normally 18% | — |
| SOL | cheap rows 2,526, spike-to-target normally 22% | cheap rows 7,782, spike-to-target normally 20% | — |
| XRP | cheap rows 2,500, spike-to-target normally 22% | cheap rows 7,843, spike-to-target normally 19% | — |
| DOGE | cheap rows 2,648, spike-to-target normally 21% | cheap rows 7,754, spike-to-target normally 18% | — |
| BNB | cheap rows 2,504, spike-to-target normally 21% | cheap rows 7,523, spike-to-target normally 21% | — |
| HYPE | cheap rows 2,566, spike-to-target normally 22% | cheap rows 7,208, spike-to-target normally 21% | — |

**All weeks:** cheap rows 17,635, spike-to-target normally 22%

**All months:** cheap rows 53,540, spike-to-target normally 19%
