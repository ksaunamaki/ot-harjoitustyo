from primitives.interfaces import RenderedObject
from primitives.position import Position


class StatusItem(RenderedObject):

    def __init__(self, x_position: int):
        super().__init__(Position(x_position, -5))

    def set_text(self, text: str):
        self._text = text