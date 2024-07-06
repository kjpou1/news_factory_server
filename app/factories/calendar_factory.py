from app.core.icalendar import ICalendar
from app.implementations.ical_impl import ICalImpl
from app.implementations.icalendar_impl import ICalendarImpl


class CalendarFactory:
    @staticmethod
    def create_calendar(implementation: str = "default") -> ICalendar:
        if implementation == "icalendar":
            return ICalendarImpl()
        return ICalImpl()
