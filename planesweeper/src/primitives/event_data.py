from primitives.event_type import EventType
from primitives.position import Position


class EventData:
    def __init__(self, event: EventType,
                 position: Position = None,
                 data = None):
        self.event = event
        self.position = position
        self.data = data
