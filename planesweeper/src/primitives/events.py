from enum import Enum
from primitives.position import Position


class EventType(Enum):
    NONE = 0
    EXIT = 1
    RIGHT_CLICK = 2
    LEFT_CLICK = 3
    NEW_GAME = 4
    NEW_SINGLE_GAME = 5
    NEW_CHALLENGE_GAME = 6
    CHANGE_LEVEL_1 = 11
    CHANGE_LEVEL_2 = 12
    CHANGE_LEVEL_3 = 13
    CHANGE_LEVEL_4 = 14
    CHANGE_LEVEL_5 = 15
    CHANGE_LEVEL_6 = 16
    ALPHANUMERIC_KEY = 40

class EventData:
    def __init__(self, event: EventType,
                 position: Position = None,
                 data = None):
        self.event = event
        self.position = position
        self.data = data
