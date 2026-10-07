from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

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

    page.goto(
        URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_timeout(5000)

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

# MINGARA

MINGARA_URL = "https://onebymingara.com.au/timetables/"

mingara_cal = Calendar()

mingara_cal.add(
    "X-WR-TIMEZONE",
    "Australia/Sydney"
)

mingara_cal.add(
    "prodid",
    "-//Mingara Fitness//"
)

mingara_cal.add(
    "version",
    "2.0"
)

TARGET_CLASSES = [
    "Body Pump",
    "Body Pump HEAVY",
    "Body Step",
    "Barbell",
    "Dance"
]

DAY_DATES = {
    "Thursday": (8, 10),
    "Friday": (9, 10),
    "Saturday": (10, 10),
    "Sunday": (11, 10),
    "Monday": (12, 10),
    "Tuesday": (13, 10),
    "Wednesday": (14, 10),
}

mingara_events = 0

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(
        MINGARA_URL,
        wait_until="domcontentloaded",
        timeout=60000
    )

    for day_name, (day_num, month_num) in DAY_DATES.items():

        try:

            page.click(
                f'button[data-day="{day_name}"]'
            )

            page.wait_for_timeout(2000)

            html = page.content()

            soup = BeautifulSoup(
                html,
                "html.parser"
            )

            event_date = datetime(
                2026,
                month_num,
                day_num
            )

            for row in soup.select(".timetable-row"):

                title = row.select_one(".class-title")

                if not title:
                    continue

                title_text = title.get_text(
                    strip=True
                )

                if not any(
                    target.lower() in title_text.lower()
                    for target in TARGET_CLASSES
                ):
                    continue

                time_div = row.select_one(
                    ".class-time"
                )

                duration_div = row.select_one(
                    ".class-duration"
                )

                if not time_div or not duration_div:
                    continue

                start_time = time_div.get_text(
                    strip=True
                ).replace(
                    "Finished",
                    ""
                )

                try:
                    hours, minutes = map(
                        int,
                        start_time.split(":")
                    )
                except:
                    continue

                try:
                    duration_minutes = int(
                        duration_div.get_text(
                            strip=True
                        ).split()[0]
                    )
                except:
                    duration_minutes = 60

start = event_date.replace(
    hour=hours,
    minute=minutes,
    tzinfo=ZoneInfo("Australia/Sydney")
)

                end = start + timedelta(
                    minutes=duration_minutes
                )

                event = Event()

                event.add(
                    "summary",
                    f"💪 Mingara: {title_text}"
                )

                event.add(
                    "dtstart",
                    start
                )

                event.add(
                    "dtend",
                    end
                )

                mingara_cal.add_component(
                    event
                )

                mingara_events += 1

            print(
                f"Captured {day_name}"
            )

        except Exception as ex:

            print(
                f"Failed {day_name}: {ex}"
            )

    browser.close()

Path("mingara.ics").write_bytes(
    mingara_cal.to_ical()
)

print(
    f"Created {mingara_events} Mingara events"
)
