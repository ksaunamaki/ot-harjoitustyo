from primitives.asset import Asset
from primitives.events import EventData, EventType
from primitives.position import Position
from primitives.size import Size
from primitives.border import Border
from primitives.color import Color
from primitives.text_object import TextObject


class Renderer:
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

    def calculate_child_position(self,
                                 pos: Position,
                                 container_size: Size = None) -> Position:
        actual_positioning = Position(pos.x, pos.y)

        container_width = container_size.width\
            if container_size is not None\
            else Renderer.WINDOW_WIDTH

        container_height = container_size.height\
            if container_size is not None\
            else Renderer.WINDOW_HEIGHT

        if pos.x < 0:
            # calculate from end of container
            actual_positioning.x = container_width + pos.x

        if pos.y < 0:
            # calculate from bottom of container
            actual_positioning.y = container_height + pos.y

        return actual_positioning

class RenderedObject:
    def __init__(self,
                 initial_position: Position = Position(0,0),
                 z_order: int = 0,
                 renderer: Renderer = None):
        self._position = Position(initial_position.x, initial_position.y)
        self._text: TextObject = None
        self._background_size: Size = None
        self._background_color: Color = None
        self._border: Border = None
        self._z_order: int = z_order
        self._use_hand_cursor = False
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

    def get_border(self) -> Border:
        return self._border

    def change_position(self, new_position: Position):
        self._position = Position(new_position.x, new_position.y)

    def get_text(self) -> TextObject:
        return self._text

    def get_line(self) -> tuple[Position, Position, tuple[int, int, int]]:
        return None

    def show_hand_cursor(self) -> bool:
        return self._use_hand_cursor

class EventsCore:
    def get(self) -> EventData:
        return EventData(EventType.NONE, None, None)

class LanguageResource:
    _resources = {}

    def get_text(self,
                 text_id,
                 format_params: list = None) -> str:
        if text_id in self._resources:
            if format_params is None:
                return self._resources[text_id]

            return self._resources[text_id].format(*format_params)

        return f"{text_id}"
