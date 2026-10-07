from pathlib import Path
from datetime import datetime, timedelta

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

URL = "https://houseofpickle.podplay.app/community/events?location=tuggerah"

INCLUDE_WORDS = [
    "open play",
    "social",
    "coach",
    "coaching",
    "skills",
    "clinic",
    "drill",
    "40+",
    "intermediate"
]

cal = Calendar()
cal.add("prodid", "-//House Of Pickle Tuggerah//")
cal.add("version", "2.0")

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(URL, wait_until="networkidle")

    html = page.content()

    browser.close()

Path("hop_playwright.html").write_text(
    html,
    encoding="utf-8"
)

soup = BeautifulSoup(html, "html.parser")

events_found = 0

for heading in soup.find_all("h3"):

    title = heading.get_text(strip=True)

    if not any(
        word in title.lower()
        for word in INCLUDE_WORDS
    ):
        continue

    time_tag = heading.find_next("time")

    if not time_tag:
        continue

    timestamp = time_tag.get("datetime")

    if not timestamp:
        continue

    try:
        start = datetime.fromtimestamp(
            int(timestamp) / 1000
        )
    except:
        continue

    end = start + timedelta(hours=2)

    event = Event()

    event.add(
        "summary",
        f"🏓 HOP: {title}"
    )

    event.add(
        "dtstart",
        start
    )

    event.add(
        "dtend",
        end
    )

    cal.add_component(event)

    events_found += 1

Path("hop.ics").write_bytes(cal.to_ical())

print(f"Created {events_found} events")

Path("hop.ics").write_bytes(cal.to_ical())

print(f"Created {events_found} events")

# MINGARA TEST

MINGARA_URL = "https://onebymingara.com.au/timetables/"

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(
        MINGARA_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(5000)

    html = page.content()

    browser.close()

Path("mingara_playwright.html").write_text(
    html,
    encoding="utf-8"
)

print("Mingara page captured")
