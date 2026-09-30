from pathlib import Path
import requests
from icalendar import Calendar

URL = "https://houseofpickle.podplay.app/community/events?location=tuggerah"

response = requests.get(URL, timeout=30)

Path("hop_debug.html").write_text(
    response.text,
    encoding="utf-8"
)

cal = Calendar()
cal.add("prodid", "-//House Of Pickle Debug//")
cal.add("version", "2.0")

Path("hop.ics").write_bytes(cal.to_ical())

print("Debug page saved")
