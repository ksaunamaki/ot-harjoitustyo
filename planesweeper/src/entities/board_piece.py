from enum import Enum
from primitives.asset import Asset
from primitives.position import Position
from primitives.size import Size
from primitives.interfaces import RenderedObject
from services.asset_service import AssetService


class BoardPieceType(Enum):
    EMPTY = 0
    PLANE = 1
    NUMBER = 2

class BoardPiece(RenderedObject):
    cached_assets = {}

    def __init__(self, piece_size: int, piece_type: BoardPieceType, data,
                 initial_position: Position):
        super().__init__(initial_position)

        self._type = piece_type
        self._size = piece_size
        self._open = False
        self._marked = False

        if self._type == BoardPieceType.NUMBER:
            self._number = data

    def get_asset(self) -> Asset:
        pixel_size = self._size
        asset = None

        if self._marked:
            asset = f"radar-{pixel_size}.png"
        elif not self._open:
            asset = f"unopened-{pixel_size}.png"
        elif self._type == BoardPieceType.PLANE:
            asset = f"plane-{pixel_size}.png"
        elif self._type == BoardPieceType.NUMBER:
            asset = f"number_{self._number}-{pixel_size}.png"

        if asset is not None:
            if asset in BoardPiece.cached_assets:
                return BoardPiece.cached_assets[asset]

            resolved = AssetService.get_asset(asset)

            BoardPiece.cached_assets[asset] = resolved

            return resolved

        return None

    def get_dimensions(self) -> Size:
        return Size(self._size, self._size)

    def is_marked(self):
        return self._marked

    def is_open(self):
        return self._open

    def get_type(self) -> BoardPieceType:
        return self._type

    def open(self):
        if self._open or self._marked:
            return True

        self._open = True

        if self._type == BoardPieceType.PLANE:
            return False

        return True

    def mark(self):
        if self._open or self._marked:
            return

        self._marked = True

    def unmark(self):
        if self._open or not self._marked:
            return

        self._marked = False
