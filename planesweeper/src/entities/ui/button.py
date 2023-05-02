from entities.ui.text_overlay import TextOverlay
from primitives.events import EventData
from primitives.interfaces import Renderer
from primitives.position import Position
from primitives.size import Size
from primitives.border import Border
from primitives.color import Color


class Button(TextOverlay):
    """Represents an UI button element.
    """
    def __init__(self,
                 text_to_show: str,
                 text_size: int,
                 text_offset: Position,
                 text_color: Color,
                 button_position: Position,
                 button_size: Size,
                 button_color: Color,
                 border: Border,
                 event_on_click: EventData,
                 renderer: Renderer):
        """Initialize button element.

        Args:
            text_to_show (str): Text to show in the button.
            text_size (int): Font size to use for button's text.
            text_offset (Position): Button text's relative offset inside the button.
            text_color (Color): Button text's color.
            button_position (Position): Button top-left corner position on container.
            button_size (Size): Size of the button.
            button_color (Color): Background color for the button.
            border (Border): Border style for button.
            event_on_click (EventData): Event information to return when button is clicked.
            renderer (Renderer): Hosting renderer (required to apply clipping correctly).
        """
        super().__init__(text_to_show,
                         text_size,
                         text_offset,
                         text_color,
                         button_position,
                         button_size,
                         button_color,
                         border,
                         renderer)
        
        self._use_hand_cursor = True
        self._event_on_click = event_on_click

    def get_click_event(self) -> EventData:
        """Gets button's event data on click. Called by event handler.

        Returns:
            EventData: Event data to return for click.
        """
        return self._event_on_click
