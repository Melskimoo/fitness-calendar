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

days = [
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday"
]

all_html = []

for day in days:

    try:

        page.click(
            f'button[data-day="{day}"'
        )

        page.wait_for_timeout(2000)

        all_html.append(page.content())

        print(f"Captured {day}")

    except Exception as ex:

        print(f"Failed {day}: {ex}")

html = "\n".join(all_html)
 
browser.close()
 
Path("mingara_playwright.html").write_text(
html,
encoding="utf-8"
)

from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")

matches = []

for row in soup.select(".timetable-row"):

    row_text = row.get_text(" ", strip=True)

    if any(
        x.lower() in row_text.lower()
        for x in [
            "Body Pump",
            "Body Pump HEAVY",
            "Body Step",
            "Barbell",
            "Dance"
        ]
    ):
        matches.append(row_text)

Path("mingara_playwright.html").write_text(
    html,
    encoding="utf-8"
)

soup = BeautifulSoup(html, "html.parser")

from icalendar import Calendar, Event
from datetime import datetime, timedelta

mingara_cal = Calendar()
mingara_cal.add("prodid", "-//Mingara Fitness//")
mingara_cal.add("version", "2.0")

TARGET_CLASSES = [
    "Body Pump",
    "Body Pump HEAVY",
    "Body Step",
    "Barbell",
    "Dance"
]

# Temporary date while we prove the calendar works
event_date = datetime(2026, 10, 2)

events_found = 0

for row in soup.select(".timetable-row"):

    title = row.select_one(".class-title")

    if not title:
        continue

    title_text = title.get_text(strip=True)

    if not any(
        target.lower() in title_text.lower()
        for target in TARGET_CLASSES
    ):
        continue

    time_div = row.select_one(".class-time")
    duration_div = row.select_one(".class-duration")

    if not time_div or not duration_div:
        continue

    start_time = time_div.get_text(strip=True)

    try:
        start_time = start_time.replace("Finished", "")
        hours, minutes = map(int, start_time.split(":"))
    except:
        continue

    duration_text = duration_div.get_text(strip=True)

    try:
        duration_minutes = int(duration_text.split()[0])
    except:
        duration_minutes = 60

    start = event_date.replace(
        hour=hours,
        minute=minutes
    )

    end = start + timedelta(minutes=duration_minutes)

    event = Event()

    event.add(
        "summary",
        f"💪 Mingara: {title_text}"
    )

    event.add("dtstart", start)
    event.add("dtend", end)

    mingara_cal.add_component(event)

    events_found += 1

Path("mingara.ics").write_bytes(
    mingara_cal.to_ical()
)

print(f"Created {events_found} Mingara events")
