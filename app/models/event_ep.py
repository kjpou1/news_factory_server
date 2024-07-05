from dataclasses import dataclass

@dataclass
class EventEP:
    name: str
    description: str
    end_point: str
    file: str
