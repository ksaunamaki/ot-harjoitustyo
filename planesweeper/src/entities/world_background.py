import os
from entities.board import Gameboard
from primitives.interfaces import RenderedObject
from services.AssetService import AssetService

class WorldBackground(RenderedObject):
    WIDTH = 900
    HEIGHT = 450

    def __init__(self):
        super().__init__((0,0))

    def position_board_on_world(self, board: Gameboard):
        dimensions = board.get_dimensions()

        # position on Europe, initially
        x = max(0, 472 - dimensions[0] // 2)
        y = max(0, 165 - dimensions[1] // 2)

        if dimensions[0] >= WorldBackground.WIDTH // 2:
            x = WorldBackground.WIDTH // 2 - dimensions[0] // 2

        if dimensions[1] >= WorldBackground.HEIGHT // 1.5:
            y = WorldBackground.HEIGHT // 2 - dimensions[1] // 2

        board.change_position((x, y))

    def get_asset(self):
        return AssetService.get_asset("world.png")
    
    def get_dimensions(self) -> tuple[int,int]:
        return (WorldBackground.WIDTH, WorldBackground.HEIGHT)