from icalendar import Calendar
from pathlib import Path

def create_calendar(name):
    cal = Calendar()
    cal.add("prodid", f"-//{name}//")
    cal.add("version", "2.0")
    return cal

def save_calendar(cal, filename):
    Path(filename).write_bytes(cal.to_ical())

hop = create_calendar("House of Pickle")
pcyc = create_calendar("PCYC")
mingara = create_calendar("Mingara")

save_calendar(hop, "hop.ics")
save_calendar(pcyc, "pcyc.ics")
save_calendar(mingara, "mingara.ics")

print("Calendars generated")
