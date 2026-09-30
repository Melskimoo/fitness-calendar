from pathlib import Path
import requests

url = "https://houseofpickle.podplay.app/community/events?location=tuggerah"

response = requests.get(url, timeout=30)

html = response.text

Path("hop_debug.html").write_text(
    html,
    encoding="utf-8"
)

interesting = []

for line in html.splitlines():
    lower = line.lower()

    if (
        "event" in lower
        or "api" in lower
        or "graphql" in lower
        or "podplay" in lower
        or "tuggerah" in lower
    ):
        interesting.append(line)

Path("hop_clues.txt").write_text(
    "\n".join(interesting),
    encoding="utf-8"
)

print("Debug files created")
