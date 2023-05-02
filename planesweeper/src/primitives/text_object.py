from primitives.position import Position
from primitives.color import Color


class TextObject:
    """Text content style and information.
    """
    def __init__(self, text: str, pos: Position,
                 size: int = 11, color: Color = Color(0,0,0)):
        """Initialize text information.

        Args:
            text (str): Text to show.
            pos (Position): Relative positioning of text on container element.
            size (int, optional): Font size for text. Defaults to 11.
            color (Color, optional): Color of text. Defaults to Color(0,0,0).
        """
        if text is None:
            text = ""

        self._text = text
        self._position: Position = pos
        self._size: int = size
        self._color: Color = color

    def get_text(self) -> str:
        """Gets textual content.

        Returns:
            str: Text content.
        """
        return self._text

    def get_position(self) -> Position:
        """Gets positioning of text on container element.

        Returns:
            Position: Top-left corner position of text.
        """
        return self._position

    def get_size(self) -> int:
        """Gets font size of the text.

        Returns:
            int: Font size.
        """
        return self._size

    def get_color(self) -> Color:
        """Gets color for text.

        Returns:
            Color: Color value.
        """
        return self._color

    def append_text(self, appended_text: str):
        """Adds characters to the text content held by this object.

        Args:
            appended_text (str): Text to append at the end of existing text content.
        """
        self._text += appended_text

    def truncate_text(self, by_characters: int):
        """Removes characters from the text content held by this object.

        Args:
            by_characters (int): Character count to remove from the end of existing text content.
        """
        if by_characters > len(self._text):
            by_characters = len(self._text)

        self._text = self._text[0:-by_characters]
