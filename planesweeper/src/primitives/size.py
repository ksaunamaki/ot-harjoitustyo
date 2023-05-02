class Size:
    """Represents (width,height) size. 
        Specific meaning of Size() depends on its usage context (for example, text's logical
        size as length x 1 characters or pixel size area of object in game window).

    Attributes:
        width (int): Width.
        height (int): Height.
    """
    def __init__(self, width: int, height: int):
        """Initialize size.

        Args:
            width (int): Width.
            height (int): Height.
        """
        self.width: int = width
        self.height: int = height

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, Size):
            return NotImplemented

        return self.width == other.width and self.height == other.height

    def __hash__(self):
        return hash((self.width, self.height))

    def __str__(self):
        return f"Width = {self.width}, Height = {self.height}"
