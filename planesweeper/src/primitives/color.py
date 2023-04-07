class Color:
    def __init__(self, rgb_r: int, rgb_g: int, rgb_b: int, alpha: float = 1):
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
