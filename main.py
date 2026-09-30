from pathlib import Path
import requests

build_id = "HWjzM42HVwk30WjQWQeCv"

url = (
    f"https://houseofpickle.podplay.app/_next/data/"
    f"{build_id}/community/events.json?location=tuggerah"
)

response = requests.get(url, timeout=30)

Path("hop_json_debug.txt").write_text(
    response.text,
    encoding="utf-8"
)

print("Downloaded:", response.status_code)
