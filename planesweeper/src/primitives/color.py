class Color:
    """Represents color (R,G,B,alpha) data.

    Attributes:
        rgb_r (int): Red -component's value (0-255)
        rgb_g (int): Green -component's value (0-255)
        rgb_b (int): Blue -component's value (0-255)
        alpha (float, optional): Alpha (transparency) value (0-1), 
            where 0 is fully transparent and 1 is fully opaque.
    """
    def __init__(self, rgb_r: int, rgb_g: int, rgb_b: int, alpha: float = 1):
        """Initialize color data.

        Args:
            rgb_r (int): Red -component's value (0-255)
            rgb_g (int): Green -component's value (0-255)
            rgb_b (int): Blue -component's value (0-255)
            alpha (float, optional): Alpha (transparency) value (0-1), where 0 is fully 
                transparent and 1 is fully opaque. Defaults to 1.
        """
        self.rgb_r: int = rgb_r
        self.rgb_g: int = rgb_g
        self.rgb_b: int = rgb_b
        self.alpha: float = alpha

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, Color):
            return NotImplemented

        return self.rgb_r == other.rgb_r and\
            self.rgb_g == other.rgb_g and\
            self.rgb_b == other.rgb_b and\
            self.alpha == other.alpha

    def __hash__(self):
        return hash((self.rgb_r, self.rgb_g, self.rgb_b, self.alpha))
