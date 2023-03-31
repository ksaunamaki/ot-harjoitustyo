from primitives.interfaces import RenderedObject

class BoardGridItem(RenderedObject):

    def __init__(self, start_pos: tuple[int,int], end_pos: tuple[int,int], color: tuple[int,int,int]):
        super().__init__(start_pos)
        self._line_end = end_pos
        self._color = color

    def get_line(self) -> tuple[tuple[int,int],tuple[int,int],tuple[int,int,int]]:
        return ((self._x, self._y), self._line_end, self._color)
