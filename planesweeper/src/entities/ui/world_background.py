from entities.board import Gameboard
from primitives.interfaces import Renderer, RenderedObject
from primitives.position import Position
from primitives.size import Size
from services.asset_service import AssetService


class WorldBackground(RenderedObject):
    """Represents an UI background object for the game window.
    """
    WIDTH = 900
    HEIGHT = 450

    def __init__(self, renderer: Renderer = None):
        super().__init__(Position(0,0), -1000, renderer)

    def position_board_on_world(self, board: Gameboard):
        """Calculates relative positioning for the game board on the world background, based
            on the board's logical size and positioning it initally over Europe and at larger sizes
            to fit the game window reasonably.
            Positioning is intended to prepare for the usage of real plane position data via API,
            which statistically will mostly be over inhabited world areas.

        Args:
            board (Gameboard): Gameboard for which to calculate new positioning.
        """
        dimensions = board.get_dimensions()

        # position on Europe, initially
        x_pos = max(0, 472 - dimensions.width // 2)
        y_pos = max(0, 165 - dimensions.height // 2)

        if dimensions.width >= WorldBackground.WIDTH // 2:
            x_pos = WorldBackground.WIDTH // 2 - dimensions.width // 2

        if dimensions.height >= WorldBackground.HEIGHT // 1.5:
            y_pos = WorldBackground.HEIGHT // 2 - dimensions.height // 2

        board.change_position(Position(x_pos, y_pos))

    def get_asset(self):
        return AssetService.get_asset("world.png")
