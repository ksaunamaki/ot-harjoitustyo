from entities.board import Gameboard
from primitives.interfaces import Renderer, RenderedObject
from primitives.position import Position
from primitives.size import Size
from primitives.text_object import TextObject
from services.asset_service import AssetService


class WorldBackground(RenderedObject):
    WIDTH = 900
    HEIGHT = 450

    def __init__(self, renderer: Renderer = None):
        super().__init__(Position(0,0), renderer)

        if renderer is not None:
            text = "New game: Alt+N, new game with level: Alt+[1-6]"
            self._text = TextObject(text, Position(5, renderer.get_play_area_size().height-20))

    def position_board_on_world(self, board: Gameboard):
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

    def get_dimensions(self) -> Size:
        return Size(WorldBackground.WIDTH, WorldBackground.HEIGHT)
