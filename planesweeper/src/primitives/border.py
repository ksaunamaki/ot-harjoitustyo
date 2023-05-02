from primitives.color import Color


class Border:
    """UI object's border style.

    Attributes:
        color: Color for border.
        thickness: Border's line thickness in pixels.
    """
    def __init__(self,
                 color: Color,
                 thickness = 1):
        """Initialize border style.

        Args:
            color (Color): Color for border.
            thickness (int, optional): Border's line thickness in pixels. Defaults to 1.
        """
        self.color = color
        self.thickness = thickness
