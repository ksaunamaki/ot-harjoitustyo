class Position:
    """Represents (X,Y) coordinate point/position. 
        Specific meaning of Position() depends on its usage context (for example, specific piece's
        logical position on gameboard or specific pixel absolute position in game window)
    
    Attributes:
        x_pos (int): Position in X-axis.
        y_pos (int): Position in Y-axis.
    """
    def __init__(self, x_pos: int, y_pos: int):
        """Initialize coordinate position.

        Args:
            x_pos (int): Position in X-axis.
            y_pos (int): Position in Y-axis.
        """
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
