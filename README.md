# Commodity Swing Alerts (Brent · WTI · NatGas)

Sends phone alerts **before** and **at the start of** big moves in `BZ=F`, `CL=F`, `NG=F`.

| Alert | Meaning | Action |
|---|---|---|
| 👀 Squeeze building | Volatility coiled (Bollinger inside Keltner ≥6 bars) | Get ready, no trade yet |
| 🚀 ENTRY LONG/SHORT | Squeeze released + momentum + 50-EMA trend + volume | Enter; stop/targets included |
| 🔔 TAKE PARTIAL | Hit T1 (2×ATR) | Sell half, stop → breakeven |
| 🔔 EXIT | Stop, T2 (4×ATR), 3×ATR trailing stop, or momentum flip | Close |
| ⚠️ Event soon | EIA crude (Wed 10:30 ET) / gas storage (Thu 10:30 ET) / your OPEC dates | Expect spikes |

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
