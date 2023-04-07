from entities.ui.text_box import TextBox
from primitives.interfaces import Renderer
from primitives.position import Position
from primitives.size import Size
from primitives.color import Color
from primitives.text_object import TextObject


class StatusItem(TextBox):

    def __init__(self,
                 text_to_show: str,
                 x_position: int, anchor_right = False,
                 renderer: Renderer = None):
        container_x = 0 if not anchor_right else -1

        # place "anchor" to top of status bar or  bottom of window if renderer is not available
        offset_to_statusbar = -1
        
        if renderer is not None:
            offset_to_statusbar = renderer.get_play_area_size().height

        # offset text by its height down from statusbar top and to x position
        text_object = TextObject(text_to_show, Position(x_position, 10), 14, Color(255,255,255))

        super().__init__(text_object)

        # move whole text area to correct position
        self.change_position(Position(container_x, offset_to_statusbar))
