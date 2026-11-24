"""Read-only: Kalshi's official result for the last few closed 15-min windows of each market (to check the results pushes)."""
import datetime as dt, requests, kalshi_whale as K
ET = dt.timezone(dt.timedelta(hours=-5))
for c in K.COMMS:
    r = requests.get(f"{K.API}/markets", params={"series_ticker": K.K15[c], "limit": 12, "status": "settled"}, timeout=20).json()
    ms = sorted(r.get("markets", []), key=lambda m: m.get("close_time", ""))[-8:]
    print(c, " · ".join(f"{dt.datetime.fromisoformat(m['close_time'].replace('Z', '+00:00')).astimezone(ET):%H:%M} {str(m.get('result')).upper()}"
                        f" ({m.get('expiration_value')} vs {m.get('floor_strike')})" for m in ms))
