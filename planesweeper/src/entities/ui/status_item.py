from entities.ui.text_box import TextBox
from primitives.interfaces import Renderer
from primitives.position import Position
from primitives.color import Color
from primitives.text_object import TextObject


class StatusItem(TextBox):
    """Represents an UI status bar text item.
    """
    def __init__(self,
                 text_to_show: str,
                 x_position: int, anchor_right = False,
                 renderer: Renderer = None):
        """Initialize status bar item.

        Args:
            text_to_show (str): Text to show on status bar ite,-
            x_position (int): Relative X coordinate position on status bar line.
            anchor_right (bool, optional): Anchors text to the right side of status bar instead
                of default left. Defaults to False.
            renderer (Renderer, optional): Renderer implementation to use to calculate
                Y position for status bar area on program window. Defaults to None.
        """
        container_x = 0 if not anchor_right else -1

        # place "anchor" to top of status bar or bottom of window if renderer is not available
        offset_to_statusbar = -1
        
        if renderer is not None:
            offset_to_statusbar = renderer.get_play_area_size().height

        # offset text by its height down from statusbar top and to x position
        text_object = TextObject(text_to_show, Position(x_position, 10), 14, Color(255,255,255))

        super().__init__(text_object)

        # move whole text area to correct position
        self.change_position(Position(container_x, offset_to_statusbar))
