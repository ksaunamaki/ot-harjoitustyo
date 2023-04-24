from entities.ui.text_overlay import TextOverlay
from primitives.events import EventData
from primitives.interfaces import Renderer
from primitives.position import Position
from primitives.size import Size
from primitives.border import Border
from primitives.color import Color


class Button(TextOverlay):

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
        return self._event_on_click
