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

# Kalshi Whale Scanner + 15-min Outlook (`kalshi_whale.py`)

**Reports only. It never places trades and needs no Kalshi API key** (it reads Kalshi's public trade feed).
It sends to its **own ntfy topic** (`KW_NTFY_TOPIC`), separate from the commodity alerts above.

| Push | What it tells you |
|---|---|
| 🐋 Whale | ≥ $5k order (sliced prints merged), side and price, whether it's chasing or fading the move, how past whales in the same category and price band did after 15m/1h and at settlement (after fees), how often an opposite whale (likely cash-out) followed, and the 15-min outlook for that market |
| ⚡ Spike | ≥ 5¢ in 2 min, whale-driven or not, how often spikes in that category kept going or snapped back |
| 📈 15-min outlook | at :00/:15/:30/:45 ET: top UP/DOWN calls for the next 15 min, last quarter's score, 24h record, and 24h whale-flow trends (flow vs price divergence) |
| 📊 Digest | every 6h: volume, live accuracy, most confident misses, best whale-follow cells, what the model leans on |

**How it learns:** every 15 min it snapshots up to 150 active markets (momentum, whale flow, order-flow imbalance,
activity burst, price level, spread, time to close, category) and grades each one 15 min later. Every 6h it
retrains on the last 30 days. Recent rows and its own confident misses count more. It trains on the older 70%,
leaves a 15-min gap, and tests on the newest 30%. Calls are labelled **PROVEN** only when confident calls hit
≥56% on unseen data **and** beat a plain momentum rule by 2+ pts. If the live record drops below 52% over 3
days, it goes on probation and tightens its threshold.

## Setup
1. In the ntfy app, subscribe to a **new** hard-to-guess topic, e.g. `kalshi-whales-q8x3m`.
2. Repo → Settings → Secrets → Actions → add `KW_NTFY_TOPIC`.
3. Actions → **kalshi-whale** → Run workflow → `cmd=testnotify` (check your phone), then `cmd=backfill`, `arg=3`
   (replays 3 days of trades so the model starts with data), then `cmd=live`. From then on it chains itself 24/7.
4. Optional repo **variables**: `KW_ALERT_WHALE` (default 5000), `KW_MIN_WHALE` (1000), `KW_CONF` (0.60),
   `KW_TOPN` (6), `KW_SKIP` (ticker prefixes to ignore; default `KXMVE` = multi-leg parlays).

Local: `pip install -r requirements.txt && KW_NTFY_TOPIC=... python kalshi_whale.py live` (`selftest` runs offline).

## What the research says (read before betting)
- Kalshi takers lose on average and makers win: about −32% vs −10% average returns (Bürgi, Deng & Whelan); takers are
  negative at 80 of 99 price levels (Becker, 72M trades). A whale's market order is **not** automatically smart money.
  That's why every whale stat here is measured against what actually happened next, after fees.
- Favorite-longshot bias: contracts under ~15¢ lose the most. Cheap "lottery" whale buys are usually bad to follow.
- Kalshi trades are anonymous, so "this whale usually cashes out" can't be tracked per person. The scanner measures
  it per category instead (an opposite-side whale following a whale). Polymarket has public wallets, so per-trader
  profiles are a possible next step.
- On Polymarket, 1% of users take 76.5% of profits, mostly by **providing** liquidity with limit orders (Akey et al., 2026).
  If you act on a signal, a limit order at or inside the spread beats paying the ask.
