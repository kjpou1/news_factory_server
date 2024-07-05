from ics import Calendar, Event
import logging
from datetime import timedelta
from dateutil import parser

logger = logging.getLogger(__name__)

class ICalUtil:
    @staticmethod
    def add_event_from_json(calendar, event):
        """
        Add a single event to the iCalendar from JSON data.
        
        Parameters:
        calendar (Calendar): The iCalendar object to add events to
        event (dict): A dictionary containing event details
        """
        try:
            ical_event = Event()
            ical_event.name = event.get('trimmedPrefixedName')
            ical_event.classification = event.get('impactTitle')
            ical_event.description = f"Country: {event.get('country')}, Impact: {event.get('impactTitle')}, Forecast: {event.get('forecast')}, Previous: {event.get('previous')}"
            ical_event.location = event.get('country')
            if event.get('timeLabel') == 'All Day':
                ## Not sure why I need to do this but am pretty sure it has to do with timezone crap 
                ical_event.end = parser.parse(event.get('timestamp_local')) + timedelta(days=1, hours=1)  # Assuming a default duration of 1 hour                
                ical_event.begin = parser.parse(event.get('timestamp_local')) + timedelta(days=1)
                ical_event.make_all_day()
            else:
                ical_event.begin = parser.parse(event.get('timestamp_local'))
                ical_event.end = parser.parse(event.get('timestamp_local')) + timedelta(hours=1)  # Assuming a default duration of 1 hour

            calendar.events.add(ical_event)
        except Exception as e:
            logger.exception("Failed to create iCal event for JSON event: %s", event, e)

    @staticmethod
    def create_ical_from_json(json_data):
        """
        Convert JSON data to an iCalendar format.
        
        Parameters:
        json_data (list): List of event dictionaries
        
        Returns:
        Calendar: An iCalendar object populated with events from the JSON data
        """
        calendar = Calendar()
        for event in json_data:
            ICalUtil.add_event_from_json(calendar, event)
        return calendar

    @staticmethod
    def save_ical_to_file(calendar, file_path):
        """
        Save an iCalendar object to a file.
        
        Parameters:
        calendar (Calendar): The iCalendar object to save
        file_path (str): The file path to save the calendar to
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(calendar)
