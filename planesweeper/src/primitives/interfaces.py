from enum import Enum
from primitives.asset import Asset

class RenderedObject:
    def __init__(self, initial_position: tuple[int,int]):
        self._x = initial_position[0]
        self._y = initial_position[1]
        self._text: str = None

    def get_asset(self) -> Asset:
        return None
    
    def get_position(self) -> tuple[int,int]:
        return (self._x, self._y)
    
    def change_position(self, new_position: tuple[int, int]):
        self._x = new_position[0]
        self._y = new_position[1]

    def get_text(self) -> str:
        return self._text
    
    def get_line(self) -> tuple[tuple[int,int],tuple[int,int],tuple[int,int,int]]:
        return None

class Renderer:
    WINDOW_TITLE = "Planesweeper"
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 485

    def __init__(self, fps: int = 60):
        self._fps = fps

    def compose(self, objects):
        pass

    def tick(self):
        pass

    def set_game_state(self):
        pass

    def set_won_state(self):
        pass

    def set_lost_state(self):
        pass

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

class EventsCore:
    def get(self) -> tuple[EventType, tuple[int,int]]:
        return (EventType.NONE, None)
