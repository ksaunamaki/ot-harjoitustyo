from primitives.position import Position
from primitives.color import Color


class TextObject:
    def __init__(self, text: str, pos: Position,
                 size: int = 11, color: Color = Color(0,0,0)):
        if text is None:
            text = ""

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

    def append_text(self, appended_text: str):
        self._text += appended_text

    def truncate_text(self, by_characters: int):
        self._text = self._text[0:-by_characters]
