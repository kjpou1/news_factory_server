import logging
from app.config.config import Config
from app.services.data_service import DataService
from app.factories.calendar_factory import CalendarFactory

class ICalService:
    @staticmethod
    def generate_ical(data, implementation: str = 'default'):
        config = Config()

        if data:
            impact_classes = config.impact_classes
            currencies = config.currencies
            filtered_data = DataService.filter_data(data, impact_classes, currencies)

            calendar = CalendarFactory.create_calendar(implementation)
            for event in filtered_data:
                calendar.add_event(event)

            return calendar
        else:
            logging.error("No data available for the requested calendar")
            return None
