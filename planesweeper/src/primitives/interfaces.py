from primitives.asset import Asset
from primitives.events import EventData, EventType
from primitives.position import Position
from primitives.size import Size
from primitives.border import Border
from primitives.color import Color
from primitives.text_object import TextObject


class Renderer:
    """Base interface class for all renderer implementations.
    """
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 485

    # assume 450 height play area and statusbar under it
    PLAYAREA_HEIGHT = 450
    STATUS_BAR_HEIGHT = 485-PLAYAREA_HEIGHT

    def __init__(self, fps: int = 60):
        """Initialize renderer

        Args:
            fps: Framerate to use to update the UI, defaults to 60.
        """
        self._fps = fps

    def compose(self, objects):
        """Runs composition of all drawn objects into UI window. Method in this
            base class does not implement any logic dy design and actual implementation
            is left to derived class using UI-library specific logic.

        Args:
            objects: A list of objects derived from RenderedObject base class that
                should be drawn.
        """

    def tick(self):
        """Synchronizes the UI to the target FPS. Method in this
            base class does not implement any logic dy design and actual implementation
            is left to derived class using UI-library specific logic.
        """

    def set_game_state(self):
        """Signals the renderer to update UI to reflect ongoing game state visually, if any.
            Method in this base class does not implement any logic dy design and actual
            implementation is left to derived class using UI-library specific logic.
        """

    def set_won_state(self):
        """Signals the renderer to update UI to reflect won game state visually, if any.
            Method in this base class does not implement any logic dy design and actual
            implementation is left to derived class using UI-library specific logic.
        """

    def set_lost_state(self):
        """Signals the renderer to update UI to reflect lost game state visually, if any.
            Method in this base class does not implement any logic dy design and actual
            implementation is left to derived class using UI-library specific logic.
        """

    def get_fps(self) -> int:
        """Gets currently set framerate.

        Returns:
            int: Current frames per second value.
        """
        return self._fps

    def get_window_size(self) -> Size:
        """Gets size of the UI window.

        Returns:
            Size: UI window size.
        """
        return Size(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    def get_play_area_size(self) -> Size:
        """Gets size of active playarea (window size - status area)

        Returns:
            Size: Play area size.
        """
        return Size(self.WINDOW_WIDTH, self.PLAYAREA_HEIGHT)

    def get_status_area_size(self) -> Size:
        """Gets size of status area (window size - play area)

        Returns:
            Size: Status area size.
        """
        return Size(self.WINDOW_WIDTH, self.STATUS_BAR_HEIGHT)

    def measure_text_dimensions(self, text_object: TextObject) -> Size:
        """Measures actual rendered dimensions of a text object. Method in this
            base class does not implement any logic dy design and actual implementation
            is left to derived class using UI-library specific logic.

        Args:
            text_object (TextObject): Text object to measure dimensions of.

        Returns:
            Size: Size of rendered text or None.
        """
        if text_object is None:
            return None

        return None

    def calculate_child_position(self,
                                 pos: Position,
                                 container_size: Size = None) -> Position:
        """Calculates actual X and Y position of child element on rendered surface
         based on its relative position. Usage of negative X and Y are supported
         to base calculate from the rightmost or bottom border of the window, respectively.
         Negative coordinates act as offset from the border, i.e. -5 is 5 pixels from border.

        Args:
            pos (Position): Child element's position to calculate from.
            container_size (Size, optional): Container against which to to calculate. 
                Defaults to None which means to calculate from UI window.

        Returns:
            Position: Calculated position.
        """
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
    """Base interface class for all UI drawn object classes to derive from.
    """
    def __init__(self,
                 initial_position: Position = Position(0,0),
                 z_order: int = 0,
                 renderer: Renderer = None):
        """Initialize UI object. Derived classes may implement type-specific initialization
            instead.

        Args:
            initial_position (Position, optional): Object's positioning on container element.
                Defaults to Position(0,0).
            z_order (int, optional): Object's z-order. 
                Defaults to 0.
            renderer (Renderer, optional): Renderer implementation that will render this UI object.
                Defaults to None.
        """
        self._position = Position(initial_position.x, initial_position.y)
        self._text: TextObject = None
        self._background_size: Size = None
        self._background_color: Color = None
        self._border: Border = None
        self._z_order: int = z_order
        self._use_hand_cursor = False
        self._renderer = renderer

    def get_z_order(self) -> int:
        """Get's UI object's z-order position in draw stack.

        Returns:
            int: z-order position.
        """
        return self._z_order

    def get_asset(self) -> Asset:
        """Gets image asset's path information if derived class is image.
            Method in this base class does not implement any logic dy design.

        Returns:
            Asset: Asset path information or None if object is not image.
        """
        return None

    def get_position(self) -> Position:
        """Gets UI object's draw position (top-left corner).

        Returns:
            Position: Object's draw position.
        """
        return self._position

    def get_background_size(self) -> Size:
        """Gets UI object's background size if derived class implements background drawing.

        Returns:
            Size: Size of the background to draw  or None.
        """
        return self._background_size

    def get_background_color(self) -> Color:
        """Gets UI object's background color if derived class implements background drawing.

        Returns:
            Color: Color to use for drawn background or None.
        """
        return self._background_color

    def get_border(self) -> Border:
        """Gets UI object's border information if derived class implements border drawing.

        Returns:
            Border: Border style to draw or None.
        """
        return self._border

    def change_position(self, new_position: Position):
        """Changes UI object's relative positioning.

        Args:
            new_position (Position): New position to set for object.
        """
        self._position = Position(new_position.x, new_position.y)

    def get_text(self) -> TextObject:
        """Gets UI object's text information if derived class implements text.

        Returns:
            TextObject: Text object to draw or None.
        """
        return self._text

    def get_line(self) -> tuple[Position, Position, Color]:
        """Gets UI object's line information if derived class implements line.

        Returns:
            tuple[Position, Position, Color]: Line start and end positions and color or None.
        """
        return None

    def show_hand_cursor(self) -> bool:
        """Hovering over UI object will show hard mouse pointer instead of normal arrow.

        Returns:
            bool: True to show hand, otherwise False.
        """
        return self._use_hand_cursor

class EventsCore:
    """Base interface class for all event handling implementations.
    """
    def get(self) -> EventData:
        """Gets mouse/keyboard events of interest to game engine.
            Method in this base class does not implement any logic dy design and
            actual implementation is left to derived class using UI-library specific logic
            for handling events.

        Returns:
            EventData: Received event information.
        """
        return EventData(EventType.NONE, None, None)

class LanguageResource:
    """Base interface class for all language translation classes.
    """
    _resources = {}

    def get_text(self,
                 text_id: str,
                 format_params: list = None) -> str:
        """Gets language -specific text string identified by text id.

        Args:
            text_id (str): Text identifier for which to fetch text string.
            format_params (list, optional): 
                Formatting parameters to apply against retrieved string.
                Each {0},{1} etc. in text string is substituted with corresponding
                value in list. Defaults to None.

        Returns:
            str: _description_
        """
        if text_id in self._resources:
            if format_params is None:
                return self._resources[text_id]

            return self._resources[text_id].format(*format_params)

        return f"{text_id}"
