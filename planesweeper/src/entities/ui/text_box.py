from primitives.interfaces import RenderedObject
from primitives.text_object import TextObject


class TextBox(RenderedObject):

    def __init__(self, text: TextObject):
        super().__init__()
        self._text = text
