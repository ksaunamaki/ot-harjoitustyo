class Position:
    def __init__(self, x_pos: int, y_pos: int):
        self.x: int = x_pos
        self.y: int = y_pos

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, Position):
            return NotImplemented

        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"X = {self.x}, Y = {self.y}"
