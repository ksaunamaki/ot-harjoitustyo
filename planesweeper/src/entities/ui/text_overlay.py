from entities.ui.text_box import TextBox
from primitives.interfaces import Renderer
from primitives.position import Position
from primitives.size import Size
from primitives.border import Border
from primitives.color import Color
from primitives.text_object import TextObject


class TextOverlayScrollData:
    def __init__(self):
        self.scroll: bool = False
        self.scroll_offset: float = 0
        self.scroll_wait_counter: int = 0
        self.original_text: str = None

class TextOverlay(TextBox):

    _SCROLL_SPACING = 10

    def _get_clipping_size(self,
                           text: TextObject, 
                           length: int, available_size: Size, text_offset_x: int,
                           renderer: Renderer):
        text_to_show = text.get_text()[0:length]

        if renderer is None:
            return Size(len(text_to_show), 1)

        if available_size is None:
            return Size(len(text_to_show), 1)

        if len(text_to_show) == 0:
            return Size(0, 1)

        text_to_measure = TextObject(text_to_show, text.get_position(),
                                     text.get_size(), text.get_color())

        measured_size = renderer.measure_text_dimensions(text_to_measure)
        if measured_size is None:
            return Size(len(text_to_show), 1)

        if (text_offset_x + measured_size.width) > available_size.width:
            return self._get_clipping_size(text, length-1, available_size,
                                           text_offset_x, renderer)

        return Size(len(text_to_measure.get_text()), 1)

    def __init__(self,
                 text_to_show: str,
                 text_size: int,
                 text_offset: Position,
                 text_color: Color,
                 overlay_position: Position,
                 overlay_size: Size,
                 overlay_color: Color,
                 border: Border,
                 renderer: Renderer):
        
        text = TextObject(text_to_show, text_offset, text_size, text_color)
        super().__init__(text)

        self._z_order = 1
        self._position = overlay_position
        self._background_size = overlay_size
        self._background_color = overlay_color
        self._border = border

        self._clip =  self._get_clipping_size(text, len(text_to_show),
                                              overlay_size, text_offset.x, renderer)
        
        self._scroll_data = TextOverlayScrollData()
        self._scroll_data.scroll = self._clip.width < len(text_to_show)

        self._scroll_data.scroll_offset: float = 0
        self._scroll_data.scroll_wait_counter: int = 0

        self._scroll_data.original_text = text_to_show if not self._scroll_data.scroll\
            else text_to_show + " " * self._SCROLL_SPACING
        
        self._fps = renderer.get_fps()

        self._blink_end: bool = False
        self._blink_state: bool = False
        self._blink_wait_counter: int = 0
    
    def _wait_scroll_start(self) -> bool:
        self._scroll_data.scroll_wait_counter = (self._scroll_data.scroll_wait_counter + 1)\
            % (self._fps // 10)
        
        return self._scroll_data.scroll_wait_counter != 0

    def _handle_scroll(self):
        rounded_offset = int(self._scroll_data.scroll_offset) %\
                len(self._scroll_data.original_text)

        if rounded_offset == 0:
            if self._wait_scroll_start():
                return
        
        self._scroll_data.scroll_offset = self._scroll_data.scroll_offset + .1
        remaining = min(self._clip.width,
                        len(self._scroll_data.original_text)-rounded_offset)
        text_to_show = self._scroll_data.original_text[rounded_offset:rounded_offset+remaining]

        if remaining < self._clip.width:
            from_beginning = self._clip.width - remaining + 3
            text_to_show += f"{self._scroll_data.original_text[0:from_beginning]}"

        self._text._text = text_to_show

    def _wait_blink_state(self) -> bool:
        self._blink_wait_counter = (self._blink_wait_counter + 1)\
            % (self._fps // 10)
        
        return self._blink_wait_counter == 0

    def _handle_blinking(self):
        if self._wait_blink_state():
            self._blink_state = not self._blink_state

            if self._blink_state:
                self._text._text += " _"
            else:
                if self._text._text[-1] == "_":
                    self._text._text = self._text._text[0:-2]

    def tick(self):
        if self._scroll_data.scroll:
            self._handle_scroll()

        if self._blink_end:
            self._handle_blinking()

    def enable_blink_on_end(self):
        self._blink_end = True

    def disable_blink_on_end(self):
        self._blink_end = False

    def append_text(self, text: str):
        if not self._blink_end or not self._blink_state:
            self._text.append_text(text)
            return

        if self._text._text[-1] == "_":
            self._text._text = self._text._text[0:-2]

        self._text.append_text(text)
        self._text._text += " _"

    def truncate_text(self, by_characters: int):
        if not self._blink_end or not self._blink_state:
            self._text.truncate_text(by_characters)
            return

        if self._text._text[-1] == "_":
            self._text._text = self._text._text[0:-2]

        self._text.truncate_text(by_characters)
        self._text._text += " _"
