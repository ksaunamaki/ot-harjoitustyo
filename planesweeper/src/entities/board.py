from enum import Enum
from collections import deque
import random
from primitives.interfaces import RenderedObject
from primitives.position import Position
from primitives.size import Size
from entities.board_piece import BoardPiece, BoardPieceType
from entities.ui.board_grid_item import BoardGridItem


class BoardPieceSize(Enum):
    SMALL = 0
    MEDIUM = 1
    LARGE = 2

class VisitedStackItem:
    def __init__(self, position: Position, neighbours: list[Position],
                 item_processed: bool = False,
                 is_empty: bool = False):
        self.position: Position = position
        self.neighbours: list[Position] = neighbours
        self.index: int = 0
        self.item_processed: bool = item_processed
        self.is_empty: bool = is_empty

class Gameboard:
    LEVELS = {
        1: [(5, 5), 3],
        2: [(9, 9), 19],
        3: [(15, 12), 44],
        4: [(30, 16), 139],
        5: [(55, 20), 333],
        6: [(58, 29), 599]
    }

    def __init__(self, level: int):
        if level < 1 or level > 6:
            raise ValueError()

        self._level = level
        self._won = False
        self._lost = False
        self._xsize: int = Gameboard.LEVELS[level][0][0]
        self._ysize: int = Gameboard.LEVELS[level][0][1]
        self._offset: Position = Position(0,0)
        self._planes: int = Gameboard.LEVELS[level][1]
        self._pieces: list[BoardPiece] = [None] * (self._xsize * self._ysize)
        self._grid_lines: list[BoardGridItem] = None
        self._max_recursion_depth = self._xsize + self._ysize

        self._piece_size = BoardPieceSize.MEDIUM

        if level <= 3:
            self._piece_size = BoardPieceSize.LARGE

        if level >= 5:
            self._piece_size = BoardPieceSize.SMALL

    def _get_index_from_position(self, position: Position) -> int:
        return position.y * self._xsize + position.x

    def _get_position_from_index(self, index) -> Position:
        y_pos = index // self._xsize
        x_pos = index - (y_pos * self._xsize)

        return Position(x_pos, y_pos)

    def _get_neighbouring_positions(self, position: Position,
                                    exclude: set[Position] = None) -> list[Position]:
        positions = []

        for x_pos,y_pos in [(position.x, position.y-1),
                            (position.x+1, position.y-1),
                            (position.x+1, position.y),
                            (position.x+1, position.y+1),
                            (position.x, position.y+1),
                            (position.x-1, position.y+1),
                            (position.x-1, position.y),
                            (position.x-1, position.y-1)
                            ]:
            if x_pos < 0 or x_pos > self._xsize-1 or \
                y_pos < 0 or y_pos > self._ysize-1:
                continue

            new_pos = Position(x_pos, y_pos)

            if exclude is not None and new_pos in exclude:
                continue

            positions.append(new_pos)

        return positions

    def _get_surrounding_planes(self, position: Position) -> int:
        planes = 0

        for position_to_check in self._get_neighbouring_positions(position):
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

    def _calculate_drawing_position(self, position: Position):
        pixels = self._get_piece_in_pixels()
        return Position(self._offset.x + position.x * pixels,
                self._offset.y + position.y * pixels)

    def change_position(self, draw_at: Position):
        self._offset = draw_at

        for index, piece in enumerate(self._pieces):
            position = self._get_position_from_index(index)
            piece.change_position(
                self._calculate_drawing_position(position))

        self._grid_lines = None

    def translate_event_position_to_piece_position(self,
            event_position: Position) -> Position:
        event_x = event_position.x - self._offset.x
        event_y = event_position.y - self._offset.y

        if event_x < 0 or event_y < 0:
            return None  # out of bounds

        piece_pixels = self._get_piece_in_pixels()

        if event_x > piece_pixels * self._xsize or event_y > piece_pixels * self._ysize:
            return None  # out of bounds

        x_pos = event_x // piece_pixels
        y_pos = event_y // piece_pixels

        if x_pos >= self._xsize or y_pos >= self._ysize:
            return None  # out of bounds

        return Position(x_pos, y_pos)

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
                Position(self._offset.x, self._offset.y + y_pos),
                Position(self._offset.x + width, self._offset.y + y_pos),
                color))

        for x_pos in range(0, width+1, pixels):
            self._grid_lines.append(BoardGridItem(
                Position(self._offset.x + x_pos, self._offset.y),
                Position(self._offset.x + x_pos, self._offset.y + height),
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

    def get_dimensions(self) -> Size:
        return Size(self._xsize * self._get_piece_in_pixels(),
                self._ysize * self._get_piece_in_pixels())

    def get_piece_dimensions(self) -> Size:
        pixels = self._get_piece_in_pixels()

        return Size(pixels, pixels)

    def _open_adjacent_piece(self, item: VisitedStackItem):
        item.item_processed = True

        index = self._get_index_from_position(item.position)

        piece = self._pieces[index]

        if not piece.is_open() and not piece.is_marked():
            piece_type = piece.get_type()

            if piece_type in (BoardPieceType.EMPTY, BoardPieceType.NUMBER):
                piece.open()

            if piece_type == BoardPieceType.EMPTY:
                item.is_empty = True

    def _open_adjacent_pieces(self, position: Position):
        visited = set()
        item = VisitedStackItem(position, self._get_neighbouring_positions(position),
                                item_processed = True, is_empty = True)
        visit_stack = deque()
        visit_stack.append(item)

        while len(visit_stack) > 0:
            item = visit_stack.pop()

            visited.add(item.position)

            if not item.item_processed:
                self._open_adjacent_piece(item)

            item.index += 1

            if item.index <= len(item.neighbours):
                visit_stack.append(item)

                if not item.is_empty:
                    continue

                next_position = item.neighbours[item.index-1]
                item = VisitedStackItem(next_position,
                                        self._get_neighbouring_positions(next_position, visited))
                visit_stack.append(item)

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

    def _open_piece(self, piece: BoardPiece, position: Position):
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

    def open_piece(self, position: Position):
        if self._won or self._lost:
            return

        index = self._get_index_from_position(position)

        piece = self._pieces[index]

        self._open_piece(piece, position)

    def mark_piece(self, position: Position):
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

    def game_end_result(self) -> bool:
        if self._won:
            return True

        if self._lost:
            return False

        return None
