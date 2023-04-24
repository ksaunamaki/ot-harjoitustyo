from primitives.color import Color


class Border:
    def __init__(self,
                 color: Color,
                 thickness = 1):
        self.color = color
        self.thickness = thickness
