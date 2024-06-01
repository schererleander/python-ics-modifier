from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta

# load .ics file
file_path = './calendar.ics'
with open(file_path, 'r') as file:
    ics_content = file.read()

cal = Calendar.from_ical(ics_content)

new_cal = Calendar()

for component in cal.walk():
    if component.name == "VEVENT":
        event = Event()
        for key, value in component.items():
            event.add(key, value)

        # add reminder
        alarm = Alarm()
        alarm.add("ACTION", "DISPLAY")
        alarm.add("DESCRIPTION", "Erinnerung: Mülltonne rausstellen")

        # reminder on previous date on 17:00
        event_start = event.get('DTSTART').dt
        if isinstance(event_start, datetime):
            reminder_time = event_start - timedelta(days=1, hours=event_start.hour-17, minutes=event_start.minute)
        else:
            event_start = datetime.combine(event_start, datetime.min.time())
            reminder_time = event_start - timedelta(days=1, hours=event_start.hour-17, minutes=event_start.minute)

        alarm.add("TRIGGER", reminder_time)

        event.add_component(alarm)
        new_cal.add_component(event)

# save modified calendar
new_file_path = './modified_calendar.ics'
with open(new_file_path, 'wb') as new_file:
    new_file.write(new_cal.to_ical())

