from primitives.interfaces import RenderedObject
from primitives.text_object import TextObject


class TextBox(RenderedObject):
    """Represents a generic UI text element which holds text content.
    """
    def __init__(self, text: TextObject):
        """Initialize text information.

        Args:
            text (TextObject): Text information object.
        """
        super().__init__()
        self._text = text
