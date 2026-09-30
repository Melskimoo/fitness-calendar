from pathlib import Path
import requests
import re

url = "https://houseofpickle.podplay.app/community/events?location=tuggerah"

html = requests.get(url, timeout=30).text

Path("hop_debug.html").write_text(html, encoding="utf-8")

matches = re.findall(r"__NEXT_DATA__.*", html)

Path("hop_next_data.txt").write_text(
    "\n".join(matches),
    encoding="utf-8"
)

print("Debug generated")
