from icalendar import Calendar, Event, Timezone, TimezoneStandard, TimezoneDaylight
from datetime import datetime, timedelta
from app.core.icalendar import ICalendar
from dateutil import parser
import pytz
import logging

logger = logging.getLogger(__name__)

class ICalendarImpl(ICalendar):
    def __init__(self):
        """
        Initialize the ICalendarImpl class.
        
        This constructor initializes the iCalendar object and adds timezone information.
        """
        self.calendar = Calendar()
        self._add_timezone()

    def _add_timezone(self):
        """
        Adds timezone information to the iCalendar object.

        This method sets up a timezone component in the iCalendar object, including
        standard and daylight sub-components. The timezone is set to UTC by default,
        but this can be customized as needed. The standard and daylight components
        define the timezone offset and name for both standard time and daylight
        saving time.

        The timezone information ensures that all events added to the calendar are
        properly time-zone aware and can be correctly interpreted by calendar clients
        in different time zones.
        """
        timezone = Timezone()
        timezone.add('TZID', 'UTC')  # Define the timezone ID as UTC

        # Define the standard time sub-component
        standard = TimezoneStandard()
        standard.add('DTSTART', datetime(1970, 10, 25, 2, 0, 0, tzinfo=pytz.UTC))
        standard.add('TZOFFSETFROM', timedelta(hours=-4))
        standard.add('TZOFFSETTO', timedelta(hours=-5))
        standard.add('TZNAME', 'EST')

        # Define the daylight saving time sub-component
        daylight = TimezoneDaylight()
        daylight.add('DTSTART', datetime(1970, 4, 26, 2, 0, 0, tzinfo=pytz.UTC))
        daylight.add('TZOFFSETFROM', timedelta(hours=-5))
        daylight.add('TZOFFSETTO', timedelta(hours=-4))
        daylight.add('TZNAME', 'EDT')

        # Add the standard and daylight components to the timezone
        timezone.add_component(standard)
        timezone.add_component(daylight)

        # Add the timezone to the calendar
        self.calendar.add_component(timezone)

    def add_event(self, event):
        """
        Add a single event to the iCalendar from JSON data.
        
        Parameters:
        calendar (Calendar): The iCalendar object to add events to
        event (dict): A dictionary containing event details
        
        This method parses the event details from the provided JSON data and adds it to the
        iCalendar object. It supports both all-day events and time-specific events.
        """
        try:
            ical_event = Event()
            ical_event.add('summary', event.get('trimmedPrefixedName'))  # Add the event summary

            dtstart = parser.parse(event.get('timestamp_local')).astimezone(pytz.UTC)  # Parse and convert start time to UTC
            if event.get('timeLabel') == 'All Day':
                dtstart = dtstart.date()  # Convert to date for all-day events
                dtend = dtstart + timedelta(days=1)  # Set end date to the next day
                ical_event.add('dtstart', dtstart)
                ical_event.add('dtend', dtend)
            else:
                dtend = dtstart + timedelta(hours=1)  # Set end time to one hour after start time
                ical_event.add('dtstart', dtstart)
                ical_event.add('dtend', dtend)

            # Add other event details
            ical_event.add('description', f"Country: {event.get('country')}, Impact: {event.get('impactTitle')}, Forecast: {event.get('forecast')}, Previous: {event.get('previous')}")
            ical_event.add('location', event.get('country'))

            # Add the event to the calendar
            self.calendar.add_component(ical_event)
        except Exception as e:
            logger.exception("Failed to create iCal event for JSON event: %s", event, e)

    def to_string(self):
        """
        Convert the iCalendar object to a string.

        Returns:
        str: The iCalendar data as a string
        """
        return self.calendar.to_ical().decode('utf-8')
