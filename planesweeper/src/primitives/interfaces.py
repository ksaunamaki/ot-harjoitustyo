from primitives.asset import Asset
from primitives.event_data import EventData
from primitives.event_type import EventType
from primitives.position import Position
from primitives.size import Size
from primitives.color import Color
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

    def get_fps(self) -> int:
        return 0

    def get_window_size(self) -> Size:
        return Size(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    def get_play_area_size(self) -> Size:
        return Size(self.WINDOW_WIDTH, self.PLAYAREA_HEIGHT)

    def get_status_area_size(self) -> Size:
        return Size(self.WINDOW_WIDTH, self.STATUS_BAR_HEIGHT)

    def measure_text_dimensions(self, text_object: TextObject) -> Size:
        if text_object is None:
            return None

        return None


class RenderedObject:
    def __init__(self,
                 initial_position: Position = Position(0,0),
                 z_order: int = 0,
                 renderer: Renderer = None):
        self._position = Position(initial_position.x, initial_position.y)
        self._text: TextObject = None
        self._background_size: Size = None
        self._background_color: Color = None
        self._z_order: int = z_order
        self._renderer = renderer

    def get_z_order(self) -> int:
        return self._z_order

    def get_asset(self) -> Asset:
        return None

    def get_position(self) -> Position:
        return self._position

    def get_background_size(self) -> Size:
        return self._background_size

    def get_background_color(self) -> Color:
        return self._background_color

    def change_position(self, new_position: Position):
        self._position = Position(new_position.x, new_position.y)

    def get_text(self) -> TextObject:
        return self._text

    def get_line(self) -> tuple[Position, Position, tuple[int, int, int]]:
        return None

class EventsCore:
    def get(self) -> EventData:
        return EventData(EventType.NONE, None, None)
