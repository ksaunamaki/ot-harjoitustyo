from enum import Enum
import random
from primitives.interfaces import RenderedObject
from entities.board_piece import BoardPiece, BoardPieceType
from entities.board_grid_item import BoardGridItem


class BoardPieceSize(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2


class Gameboard:
    LEVELS = {
        1: [(5, 5), 3],
        2: [(9, 9), 19],
        3: [(15, 12), 44],
        4: [(30, 16), 139],
        5: [(55, 20), 333],
        6: [(58, 29), 599]
    }

    def __init__(self, level: int, draw_at: tuple[int, int] = (0, 0)):
        if level < 0 or level > 6:
            raise ValueError()

        self._level = level
        self._won = False
        self._lost = False
        self._xsize: int = Gameboard.LEVELS[level][0][0]
        self._ysize: int = Gameboard.LEVELS[level][0][1]
        self._xoffset: int = draw_at[0]
        self._yoffset: int = draw_at[1]
        self._planes: int = Gameboard.LEVELS[level][1]
        self._pieces: list[BoardPiece] = [None] * (self._xsize * self._ysize)
        self._grid_lines: list[BoardGridItem] = None

        self._piece_size = BoardPieceSize.MEDIUM

        if level <= 3:
            self._piece_size = BoardPieceSize.LARGE

        if level >= 5:
            self._piece_size = BoardPieceSize.SMALL

    def _get_index_from_position(self, position: tuple[int, int]) -> int:
        return position[1] * self._xsize + position[0]

    def _get_position_from_index(self, index) -> tuple[int, int]:
        y_pos = index // self._xsize
        x_pos = index - (y_pos * self._xsize)

        return (x_pos, y_pos)

    def _get_surrounding_planes(self, position: tuple[int, int]) -> int:
        x_pos = position[0]
        y_pos = position[1]
        planes = 0
        positions = []

        if y_pos > 0:
            # check row before
            if x_pos > 0:
                positions.append((x_pos-1, y_pos-1))
            positions.append((x_pos, y_pos-1))
            if x_pos < self._xsize-1:
                positions.append((x_pos+1, y_pos-1))

        if x_pos > 0:
            positions.append((x_pos-1, y_pos))
        if x_pos < self._xsize-1:
            positions.append((x_pos+1, y_pos))

        if y_pos < self._ysize-1:
            # check row after
            if x_pos > 0:
                positions.append((x_pos-1, y_pos+1))
            positions.append((x_pos, y_pos+1))
            if x_pos < self._xsize-1:
                positions.append((x_pos+1, y_pos+1))

        for position_to_check in positions:
            index = self._get_index_from_position(position_to_check)

            if self._pieces[index] is not None and \
                self._pieces[index].get_type() == BoardPieceType.PLANE:
                planes += 1

        return planes

    def _get_piece_in_pixels(self):
        if self._piece_size == BoardPieceSize.LARGE:
            return 25

        if self._piece_size == BoardPieceSize.MEDIUM:
            return 20

        return 15

    def _calculate_drawing_position(self, position: tuple[int, int]):
        pixels = self._get_piece_in_pixels()
        return (self._xoffset+position[0]*pixels, self._yoffset+position[1]*pixels)

    def change_position(self, draw_at: tuple[int, int]):
        self._xoffset: int = draw_at[0]
        self._yoffset: int = draw_at[1]

        for index, piece in enumerate(self._pieces):
            position = self._get_position_from_index(index)
            piece.change_position(
                self._calculate_drawing_position(position))

        self._grid_lines = None

    def translate_event_position_to_piece_position(self,
            event_position: tuple[int, int]) -> tuple[int, int]:
        event_x = event_position[0] - self._xoffset
        event_y = event_position[1] - self._yoffset

        if event_x < 0 or event_y < 0:
            return None  # out of bounds

        piece_pixels = self._get_piece_in_pixels()

        if event_x > piece_pixels*self._xsize or event_y > piece_pixels*self._ysize:
            return None  # out of bounds

        x_pos = event_x // piece_pixels
        y_pos = event_y // piece_pixels

        if x_pos >= self._xsize or y_pos >= self._ysize:
            return None  # out of bounds

        return (x_pos, y_pos)

    def create(self, randomize_planes: bool = True):
        # Initialize new game board
        plane_indexes = []
        self._pieces: list[BoardPiece] = [None] * (self._xsize * self._ysize)
        piece_in_pixels = self._get_piece_in_pixels()

        total_pieces = len(self._pieces)

        if randomize_planes:
            plane_indexes = random.sample(range(0, total_pieces), self._planes)

        for index in plane_indexes:
            position = self._get_position_from_index(index)
            self._pieces[index] = BoardPiece(
                piece_in_pixels, BoardPieceType.PLANE, None,
                self._calculate_drawing_position(position))

        # Initialize rest
        for i in range(0, total_pieces):
            if self._pieces[i] is not None:
                continue

            position = self._get_position_from_index(i)

            planes = self._get_surrounding_planes(position)

            if planes == 0:
                self._pieces[i] = BoardPiece(
                    piece_in_pixels, BoardPieceType.EMPTY, None,
                    self._calculate_drawing_position(position))
                continue

            self._pieces[i] = BoardPiece(
                piece_in_pixels, BoardPieceType.NUMBER, planes,
                self._calculate_drawing_position(position))

    def _recalculate_grid(self):
        self._grid_lines = []

        pixels = self._get_piece_in_pixels()

        width = pixels * self._xsize
        height = pixels * self._ysize

        color = (100, 100, 100)

        for y_pos in range(0, height+1, pixels):
            self._grid_lines.append(BoardGridItem(
                (self._xoffset, self._yoffset+y_pos),
                (self._xoffset+width, self._yoffset+y_pos),
                color))

        for x_pos in range(0, width+1, pixels):
            self._grid_lines.append(BoardGridItem(
                (self._xoffset+x_pos, self._yoffset),
                (self._xoffset+x_pos, self._yoffset+height),
                color))

    def get_level(self) -> int:
        return self._level

    def get_rendering_items(self) -> list[RenderedObject]:
        items: list(RenderedObject) = []

        if self._grid_lines is None:
            self._recalculate_grid()

        for line in self._grid_lines:
            items.append(line)

        for piece in self._pieces:
            items.append(piece)

        return items

    def get_total_planes(self) -> int:
        return self._planes

    def get_radar_contacts(self) -> int:
        marked = 0

        for piece in self._pieces:
            marked += 1 if piece.is_marked() else 0

        return marked

    def get_dimensions(self) -> tuple[int, int]:
        return (self._xsize * self._get_piece_in_pixels(),
                self._ysize * self._get_piece_in_pixels())

    def get_piece_dimensions(self) -> tuple[int, int]:
        pixels = self._get_piece_in_pixels()

        return (pixels, pixels)

    def _open_adjacent_pieces_above(self, x_pos:int, y_pos: int, position: tuple[int, int]):
        # check up
        self._open_adjacent_pieces((x_pos, y_pos-1), position)

        if x_pos > 0:
            # check left
            self._open_adjacent_pieces((x_pos-1, y_pos-1), position)

        if x_pos < self._xsize-1:
            # check right
            self._open_adjacent_pieces((x_pos+1, y_pos-1), position)

    def _open_adjacent_pieces_below(self, x_pos:int, y_pos: int, position: tuple[int, int]):
        # check down
        self._open_adjacent_pieces((x_pos, y_pos+1), position)

        if x_pos > 0:
            # check left
            self._open_adjacent_pieces((x_pos-1, y_pos+1), position)

        if x_pos < self._xsize-1:
            # check right
            self._open_adjacent_pieces((x_pos+1, y_pos+1), position)

    def _open_adjacent_pieces(self, position: tuple[int, int], previous: tuple[int, int] = None):
        x_pos = position[0]
        y_pos = position[1]

        piece = self._pieces[self._get_index_from_position(position)]

        if piece.is_open() or piece.is_marked():
            if previous is not None:
                return

        piece_type = piece.get_type()

        if piece_type in (BoardPieceType.EMPTY, BoardPieceType.NUMBER):
            piece.open()

        if piece_type != BoardPieceType.EMPTY:
            return

        if y_pos > 0:
            self._open_adjacent_pieces_above(x_pos, y_pos, position)

        if y_pos < self._ysize-1:
            self._open_adjacent_pieces_below(x_pos, y_pos, position)

        if x_pos > 0:
            # check left
            self._open_adjacent_pieces((x_pos-1, y_pos), position)

        if x_pos < self._xsize-1:
            # check right
            self._open_adjacent_pieces((x_pos+1, y_pos), position)

    def _is_first_open(self) -> bool:
        count = 0

        for piece in self._pieces:
            if piece.is_open():
                count += 1

            if count > 1:
                return False

        return count == 1

    def _check_for_win(self):
        for piece in self._pieces:
            if not piece.is_open() and not piece.is_marked():
                return

        self._won = True

    def _open_piece(self, piece: BoardPiece, position: tuple[int, int]):
        if piece.is_open() or piece.is_marked():
            return  # no-op

        result = piece.open()

        if not result:
            # Game over

            # ...but to make game fair, if this was very first first piece,
            # keep generating new pieces until we don't hit plane first
            is_first = self._is_first_open()

            if not is_first:
                self._lost = True
                return

            while not result:
                self.create()
                piece = self._pieces[self._get_index_from_position(position)]
                result = piece.open()

        # if empty piece, automatically open all adjacent empty and number pieces
        if piece.get_type() == BoardPieceType.EMPTY:
            self._open_adjacent_pieces(position)

        self._check_for_win()

    def open_piece(self, position: tuple[int, int]):
        if self._won or self._lost:
            return

        index = self._get_index_from_position(position)

        piece = self._pieces[index]

        self._open_piece(piece, position)

    def mark_piece(self, position: tuple[int, int]):
        if self._won or self._lost:
            return

        index = self._get_index_from_position(position)

        piece = self._pieces[index]

        if piece.is_open():
            return  # no-op

        if piece.is_marked():
            # unmark
            piece.unmark()
            return

        # check if radar contacts are full
        if self.get_radar_contacts() >= self._planes:
            return

        piece.mark()

        self._check_for_win()

    def is_finished(self) -> bool:
        if self._won:
            return True

        if self._lost:
            return False

        return None
