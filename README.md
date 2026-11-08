# Commodity Swing Alerts (Brent · WTI · NatGas)

Sends phone alerts **before** and **at the start of** big moves in `BZ=F`, `CL=F`, `NG=F`.

Colors: 🟢 Brent (BNO) · 🟠 WTI (USO) · 🔵 NatGas (UNG)

| Alert | Meaning |
|---|---|
| 🚀 BUY / SELL SHORT now | Entry with stop, target, trailing stop, max hold, share size (1% risk) and backtest stats |
| 🔔 EXIT | Stop, target, trail or time limit hit, with % result |
| 👀 coiling | Volatility squeeze: breakout likely soon |
| ⚠️ Event soon | EIA crude (Wed 10:30 ET) / gas storage (Thu 10:30 ET) / `EXTRA_EVENTS` |
| 📊 Energy brief | ~7:40am and ~1:50pm ET weekdays: price, trend, RSI, expected move, range, open trades |

Each market uses the strategy the weekly optimizer picked (breakout, squeeze, fade, RSI-2 pullback; 15m or 1h),
trained on 70% of history and accepted only if it also profits on the unseen 30%. See `params.json`.
Set repo **variables** `ACCOUNT_SIZE` (default 10000) and `RISK_PCT` (default 1) for position sizing.

## Setup (5 min, free)
1. Install the **ntfy** app on your phone and subscribe to a hard-to-guess topic, e.g. `oil-alerts-x7k2q`.
2. Push this folder to a **private** GitHub repo. Settings → Secrets → Actions: add `NTFY_TOPIC`.
   Optional: `EIA_API_KEY` (free at eia.gov/opendata), `TELEGRAM_TOKEN`+`TELEGRAM_CHAT_ID`, `DISCORD_WEBHOOK`.
   Optional variable `EXTRA_EVENTS` = `2026-11-30 OPEC+ meeting,2026-12-10 FOMC`.
3. It runs every 30 min via GitHub Actions. Or run locally: `pip install -r requirements.txt && python swing_alert.py scan`.

## Validate before risking money
```
python swing_alert.py backtest   # 2y hourly + 15y daily, per market, after fees
```
Tune `P` in `swing_alert.py` (e.g. `INTERVAL=1d` for slower swings) and only trade what shows profit factor > 1.3 out of sample.

## Data notes
Yahoo futures data is free but ~10 min delayed and switches contracts at roll. For real-time accuracy use your broker's
feed (IBKR via `ib_insync`, or Databento/Polygon paid). EIA is the official source for inventory data.

## Upgrade paths (reviewed GitHub repos)
- `polakowo/vectorbt` (9.6k★): fast parameter sweeps for these rules.
- `hackingthemarkets/ttm-squeeze`: the squeeze idea this is built on.
- `xgboosted/pandas-ta-classic`: 130+ extra indicators.
- `thomastu/pyEIA`: fuller EIA client.
- `freqtrade/freqtrade` (56k★): best open-source bot framework, but crypto-only, so not usable for oil/gas futures directly.

⚠️ Not financial advice. No system reliably predicts swings, and oil and gas futures are leveraged. Size each trade so a stop costs ≤1% of your account.

---

# Kalshi Commodity Scanner (`kalshi_whale.py`)

**Reports only. It never trades and needs no Kalshi key.** It covers commodities only: WTI, Brent, NatGas, gold, silver,
copper, platinum and palladium, on Kalshi's 15-min up/down markets plus the hourly and daily ones. It pushes to its
own ntfy topic, `KW_NTFY_TOPIC`.

| Push | What it tells you |
|---|---|
| 📈 15-min board | once per window: each commodity's UP/DOWN odds vs Kalshi's price, edge after fees, whale flow, PROVEN or not |
| 🎯 Edge call | model beats Kalshi's ask by 4+ pts after fees (ask ≤ 70¢), only on markets proven on both weeks and months |
| ✅/❌ Result | every edge call graded at settlement; a market's calls pause if its live record turns negative |
| 🐋 Whale | ≥ $2k merged order on any commodity market: bullish/bearish, chasing/fading, what past whales did next, likely cash-outs |
| ⚡ Spike | fast jump on a commodity market (15¢/2m on 15-min contracts, 5¢/2m elsewhere) |
| 📊 Digest | every 6h: live accuracy vs Kalshi, edge-call ROI, whale flow per commodity |

**Data (all combined):** the commodity bot's 3-week Kalshi cache, fresh pulls of the last 3 weeks and the past 90 days
(every 3rd window older than 3 weeks), every window's trades (order flow and $100+ big-money flow), and the whale history
this scanner records live.

**Model:** `p = σ(logit(Kalshi mid) + w·x)`. It learns only what Kalshi's own price misses: quote changes over 1/3/5 min,
spread, volume, order-flow imbalance, big-money flow, time left, session and market. It is trained on the older 70% of
the last 3 weeks and tested on the newest 30%, then re-checked on past months it never saw (month by month).
**PROVEN** = lower log-loss than Kalshi and a profitable edge-bet test on both. It retrains every 6h, recent windows weigh
more, and windows where a live edge call lost count 1.5×. Full results: `kwhale/report.md`.

## Setup
1. Repo secret `KW_NTFY_TOPIC` = a long lowercase topic, subscribed in the ntfy app with the exact same name.
2. Actions → **kalshi-whale** → Run workflow → `cmd=build`. It pulls about 3 months, trains, pushes the comparison,
   then starts `live`, which chains itself 24/7.
3. Optional variables: `KW_ALERT_WHALE` (2000), `KW_MIN_WHALE` (500), `KW_EDGE` (0.04).
   `cmd=doctor` checks push delivery.

## Switches (no restart needed)
Edit `kwhale/switches.json` on GitHub (pencil icon → commit). The live bot re-reads it every 5 min.
- `"pause_all": true` mutes every push.
- `"markets": {"NATGAS": false}` mutes one commodity.
- `"alerts": {"spikes": false}` mutes one alert type: `board`, `edge_calls`, `results`, `whales`, `spikes`, `digest`, `open_close`.

Data collection and learning keep running while things are switched off. When a commodity's 15-min market stops
trading (daily break, weekend, halt), you get one 🔕 push and its predictions and calls pause. You get 🔔 when it reopens.

## What the research says
- Kalshi takers lose on average and makers win (Bürgi, Deng & Whelan; Becker, 72M trades), so big market orders are not
  automatically smart money. Every whale stat here is checked against what happened next.
- Contracts under ~15¢ lose the most (favorite-longshot bias), so the scanner never suggests them, and never anything over 70¢.
- Kalshi trades are anonymous, so cash-outs are measured per commodity (an opposite whale following a whale), not per person.
- If you act on a call, a limit order at or inside the spread beats paying the ask: liquidity providers take most profits
  (Akey et al., 2026).

# Kalshi Crypto Scanner (`kalshi-crypto` workflow)
Same engine as the commodity scanner (`kalshi_whale.py` with `KW_PROFILE=crypto`), on Kalshi's 15-min crypto markets:
BTC, ETH, SOL, XRP, DOGE. Reports only, never trades. Pushes go to its own ntfy topic (`KC_NTFY_TOPIC`).

- **Same pushes:** 📈 board (🟢 BET / 🔴 NO BET, settles-at-close odds vs Kalshi), 🔄 9-min update, 🎯 results (leans vs bets),
  🐋 whales (15-min markets, $10k+ default), ⚡ spikes, 🚀 cheap-spike odds, 📊 digest, 🔕/🔔 market closed/reopened.
- **Extra crypto inputs:** live Coinbase spot (a constituent of the CF Benchmarks index Kalshi settles on, 60-s average):
  - `sgap`: digital fair value N(ln(S/K) / (σ√h)) vs Kalshi's price (h = minutes left − 0.5), in log-odds
  - `sr1/sr3/sr5`: spot returns over 1/3/5 min in σ units; `svz`: log of 30-min realized σ; `sok`: spot available
- **Same safeguards:** model = Kalshi's own price + what it misses; trained on 3 weeks, tested on the newest 30% and on
  past months; 🎯 calls only on markets PROVEN in both. Per-window trade pulls are off (`KW_FLOW=0`) because crypto
  windows have too many trades; spot carries the signal.
- **Setup:** add repo secret `KC_NTFY_TOPIC` (e.g. `kalshicrypto-jj7342`), subscribe to it in the ntfy app (server
  ntfy.sh), run `kalshi-crypto` with `cmd=build` once (it chains into live). Switches: `kcrypto/switches.json`.
- **Research basis:** settlement on CF Benchmarks real-time indexes (60-s average); N(d2) digital pricing with realized
  vol (Paradigm; arXiv 2606.19517 on prediction-market vs option prices); practitioner reports of short crypto prediction
  markets lagging spot by 30-90 s (unverified, so it must pass the same PROVEN test); minute-level order flow alone is weak.
