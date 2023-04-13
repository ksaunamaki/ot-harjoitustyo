from primitives.interfaces import RenderedObject
from primitives.position import Position


class BoardGridItem(RenderedObject):

    def __init__(self, start_pos: Position, end_pos: Position,
                  color: tuple[int, int, int]):
        super().__init__(start_pos, -1)
        self._line_end = end_pos
        self._color = color

    def get_line(self) -> tuple[Position, Position, tuple[int, int, int]]:
        return (self._position, self._line_end, self._color)
