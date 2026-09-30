from pathlib import Path
from datetime import datetime
import requests

from icalendar import Calendar, Event

EVENTS_URL = (
    "https://houseofpickle.podplay.app/apis/v2/events"
    "?excludeUnlisted=true"
    "&tag=Featured"
    "&ipp=100"
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
    "intermediate"
]

EXCLUDE_KEYWORDS = [
    "tournament",
    "league",
    "competition",
    "court hire",
    "private booking"
]


def should_include(name, description):
    text = f"{name} {description}".lower()

    if any(word in text for word in EXCLUDE_KEYWORDS):
        return False

    return any(word in text for word in INCLUDE_KEYWORDS)


def create_calendar():
    cal = Calendar()
    cal.add("prodid", "-//House Of Pickle Tuggerah//")
    cal.add("version", "2.0")
    return cal


response = requests.get(EVENTS_URL, timeout=30)
response.raise_for_status()

data = response.json()

cal = create_calendar()

count = 0

for item in data.get("items", []):

    name = item.get("name", "")
    description = item.get("description", "")

    if not should_include(name, description):
        continue

    pods = item.get("pods", {}).get("items", [])

    tuggerah = False

    for pod in pods:
        slug = pod.get("slug", "")

        if slug == "tuggerah-pickleball-courts":
            tuggerah = True
            break

    if not tuggerah:
        continue

    start_time = item.get("startTime")
    end_time = item.get("endTime")

    if not start_time or not end_time:
        continue

    event = Event()

    event.add("summary", f"🏓 HOP: {name}")

    event.add(
        "dtstart",
        datetime.fromisoformat(
            start_time.replace("Z", "+00:00")
        ),
    )

    event.add(
        "dtend",
        datetime.fromisoformat(
            end_time.replace("Z", "+00:00")
        ),
    )

    event.add(
        "description",
        description[:5000]
    )

    cal.add_component(event)

    count += 1

Path("hop.ics").write_bytes(cal.to_ical())

print(f"Created {count} House of Pickle events")
