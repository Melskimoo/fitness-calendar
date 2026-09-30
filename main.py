from datetime import datetime, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

HOP_EVENTS_URL = (
    "https://houseofpickle.podplay.app/community/events"
    "?location=tuggerah"
)

INCLUDE_KEYWORDS = [
    "open play",
    "social",
    "coach",
    "coaching",
    "skills",
    "clinic",
    "development",
    "drill",
    "40+",
]

EXCLUDE_KEYWORDS = [
    "tournament",
    "league",
    "competition",
    "court hire",
    "private booking",
]


def is_wanted_event(text):
    text = text.lower()

    if any(word in text for word in EXCLUDE_KEYWORDS):
        return False

    if any(word in text for word in INCLUDE_KEYWORDS):
        return True

    return False


def create_calendar():
    cal = Calendar()
    cal.add("prodid", "-//House Of Pickle Tuggerah//")
    cal.add("version", "2.0")
    return cal


def add_placeholder_event(cal, title):
    event = Event()

    now = datetime.utcnow()
    later = now + timedelta(hours=2)

    event.add("summary", title)
    event.add("dtstart", now)
    event.add("dtend", later)

    cal.add_component(event)


def scrape_house_of_pickle():
    cal = create_calendar()

    try:
        response = requests.get(HOP_EVENTS_URL, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        page_text = soup.get_text(" ", strip=True)

        found_match = False

        for keyword in INCLUDE_KEYWORDS:
            if keyword.lower() in page_text.lower():
                found_match = True
                break

        if found_match:
            add_placeholder_event(
                cal,
                "🏓 HOP Feed Active - Matching events discovered",
            )
        else:
            add_placeholder_event(
                cal,
                "🏓 HOP Feed Active - No matching events found",
            )

    except Exception as ex:
        add_placeholder_event(
            cal,
            f"🏓 HOP Feed Error: {str(ex)[:80]}"
        )

    Path("hop.ics").write_bytes(cal.to_ical())


def create_empty_placeholder(name, filename):
    cal = Calendar()
    cal.add("prodid", f"-//{name}//")
    cal.add("version", "2.0")

    event = Event()
    now = datetime.utcnow()

    event.add("summary", f"{name} feed coming soon")
    event.add("dtstart", now)
    event.add("dtend", now + timedelta(hours=1))

    cal.add_component(event)

    Path(filename).write_bytes(cal.to_ical())


scrape_house_of_pickle()

create_empty_placeholder(
    "PCYC Bateau Bay",
    "pcyc.ics"
)

create_empty_placeholder(
    "Mingara One",
    "mingara.ics"
)

print("Calendars generated")
