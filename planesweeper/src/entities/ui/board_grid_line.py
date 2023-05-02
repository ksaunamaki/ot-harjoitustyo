from primitives.interfaces import RenderedObject
from primitives.position import Position
from primitives.color import Color


class BoardGridLine(RenderedObject):
    """Represents a single grid line under the gameboard.
    """
    def __init__(self, start_pos: Position, end_pos: Position,
                  color: Color):
        """Initialize line.

        Args:
            start_pos (Position): Point to draw line from.
            end_pos (Position): Point to draw line to.
            color (Color): Line color.
        """
        super().__init__(start_pos, -1)
        self._line_end = end_pos
        self._color = color

    def get_line(self) -> tuple[Position, Position, Color]:
        return (self._position, self._line_end, self._color)
