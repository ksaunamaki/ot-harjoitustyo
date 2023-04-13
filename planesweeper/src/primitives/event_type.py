from enum import Enum


class EventType(Enum):
    NONE = 0
    EXIT = 1
    RIGHT_CLICK = 2
    LEFT_CLICK = 3
    NEW_GAME = 4
    CHANGE_LEVEL_1 = 11
    CHANGE_LEVEL_2 = 12
    CHANGE_LEVEL_3 = 13
    CHANGE_LEVEL_4 = 14
    CHANGE_LEVEL_5 = 15
    CHANGE_LEVEL_6 = 16
    ALPHANUMERIC_KEY = 40
