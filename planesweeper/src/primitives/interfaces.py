from enum import Enum
from primitives.asset import Asset
from primitives.position import Position
from primitives.size import Size
from primitives.text_object import TextObject


class Renderer:
    WINDOW_TITLE = "Planesweeper"
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 485

    # assume 450 height play area and statusbar under it
    PLAYAREA_HEIGHT = 450
    STATUS_BAR_HEIGHT = 485-PLAYAREA_HEIGHT

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

    def get_window_size(self) -> Size:
        return Size(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    def get_play_area_size(self) -> Size:
        return Size(self.WINDOW_WIDTH, self.PLAYAREA_HEIGHT)

    def get_status_area_size(self) -> Size:
        return Size(self.WINDOW_WIDTH, self.STATUS_BAR_HEIGHT)



class RenderedObject:
    def __init__(self, initial_position: Position = Position(0,0), renderer: Renderer = None):
        self._position = Position(initial_position.x, initial_position.y)
        self._text: TextObject = None
        self._renderer = renderer

    def get_asset(self) -> Asset:
        return None

    def get_position(self) -> Position:
        return Position(self._position.x, self._position.y)

    def change_position(self, new_position: Position):
        self._position = Position(new_position.x, new_position.y)

    def get_text(self) -> TextObject:
        return self._text

    def get_line(self) -> tuple[Position, Position, tuple[int, int, int]]:
        return None


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
    def get(self) -> tuple[EventType, Position]:
        return (EventType.NONE, None)
