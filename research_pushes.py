"""Read-only: the last 24 h of pushes on the scanners' ntfy topics (what actually reached the phone)."""
import json, os, datetime as dt, requests
ET = dt.timezone(dt.timedelta(hours=-5))
for env in ("KC_NTFY_TOPIC", "KW_NTFY_TOPIC"):
    t = os.getenv(env)
    if not t: print(f"##### {env}: not set"); continue
    r = requests.get(f"https://ntfy.sh/{t}/json", params={"poll": 1, "since": os.getenv("SINCE", "24h")}, timeout=60)
    ms = [json.loads(l) for l in r.text.splitlines() if l.strip()]
    ms = [m for m in ms if m.get("event") == "message"]
    print(f"##### {env}: {len(ms)} messages")
    for m in ms:
        print(f"@@ {dt.datetime.fromtimestamp(m['time'], ET):%m-%d %H:%M:%S} | {m.get('title', '(no title — user command)')}")
        print(m.get("message", ""))
