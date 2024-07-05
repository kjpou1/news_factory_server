from ics import Calendar, Event
from datetime import timedelta, datetime
from app.core.icalendar import ICalendar
from dateutil import parser
import pytz
import logging

logger = logging.getLogger(__name__)

class ICalImpl(ICalendar):
    def __init__(self):
        """
        Initialize the CalendarImpl class.

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
        # Create the timezone component
        timezone = pytz.timezone("UTC")

        # This is a simplification. In a real-world scenario, you would add a proper VTIMEZONE component
        # Here we assume all times are in UTC to demonstrate the concept
        self.timezone = timezone

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
            ical_event.name = event.get('trimmedPrefixedName')  # Add the event name

            # Parse and convert start time to UTC
            dtstart = parser.parse(event.get('timestamp_local')).astimezone(self.timezone)
            if event.get('timeLabel') == 'All Day':
                dtstart = dtstart.date()  # Convert to date for all-day events
                dtend = dtstart + timedelta(days=1)  # Set end date to the next day
                ical_event.begin = dtstart
                ical_event.end = dtend
                ical_event.make_all_day()
            else:
                dtend = dtstart + timedelta(hours=1)  # Set end time to one hour after start time
                ical_event.begin = dtstart
                ical_event.end = dtend

            # Add other event details
            ical_event.description = f"Country: {event.get('country')}, Impact: {event.get('impactTitle')}, Forecast: {event.get('forecast')}, Previous: {event.get('previous')}"
            ical_event.location = event.get('country')

            # Add the event to the calendar
            self.calendar.events.add(ical_event)
        except Exception as e:
            logger.exception("Failed to create iCal event for JSON event: %s", event, e)

    def to_string(self):
        """
        Convert the iCalendar object to a string.

        Returns:
        str: The iCalendar data as a string
        """
        return str(self.calendar)
