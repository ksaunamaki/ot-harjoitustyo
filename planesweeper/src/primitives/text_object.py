from primitives.position import Position
from primitives.color import Color


class TextObject:
    def __init__(self, text: str, pos: Position,
                 size: int = 11, color: Color = Color(0,0,0)):
        self._text = text
        self._position: Position = pos
        self._size: int = size
        self._color: Color = color

    def get_text(self) -> str:
        return self._text

    def get_position(self) -> Position:
        return self._position

    def get_size(self) -> int:
        return self._size

    def get_color(self) -> Color:
        return self._color
