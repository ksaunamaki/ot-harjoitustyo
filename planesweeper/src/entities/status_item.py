from primitives.interfaces import RenderedObject
from entities.world_background import WorldBackground

class StatusItem(RenderedObject):

    def __init__(self, x_position: int):
        super().__init__((x_position, -5))

    def set_text(self, text: str):
        self._text = text
