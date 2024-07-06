from abc import ABC, abstractmethod


class ICalendar(ABC):
    @abstractmethod
    def add_event(self, event):
        pass

    @abstractmethod
    def to_string(self):
        pass
