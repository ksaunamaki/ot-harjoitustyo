from enum import Enum
from collections import deque
import random
import time
from primitives.interfaces import RenderedObject
from primitives.position import Position
from primitives.size import Size
from primitives.color import Color
from entities.board_piece import BoardPiece, BoardPieceType
from entities.ui.board_grid_line import BoardGridLine


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

class BoardState:
    RUNNING = 0
    WON = 1
    LOST = 2

class GameboardConfiguration:
    """Internal gameboard configuration object for keeping track of game's properties.
    """
    LEVELS = {
        1: [(5, 5), 3],
        2: [(9, 9), 19],
        3: [(15, 12), 44],
        4: [(30, 16), 139],
        5: [(55, 20), 333],
        6: [(58, 29), 599]
    }

    def __init__(self, level: int):
        self._level: int = level
        self._size: Size = Size(GameboardConfiguration.LEVELS[level][0][0],
                          GameboardConfiguration.LEVELS[level][0][1])
        self._planes: int = GameboardConfiguration.LEVELS[level][1]

    @staticmethod
    def get_max_level() -> int:
        return max(GameboardConfiguration.LEVELS.keys())

    @property
    def level(self) -> int:
        return self._level

    @property
    def size(self) -> Size:
        return self._size

    @property
    def planes(self) -> int:
        return self._planes

class Gameboard:
    """Main gameboard object implementing logic for single level of gameplay.
    """
    def __init__(self, level: int):
        if level < 1 or level > 6:
            raise ValueError()

        self._configuration = GameboardConfiguration(level)
        self._state = BoardState.RUNNING
        self._start_time: float = None
        self._stop_time: float = None
        self._offset: Position = Position(0,0)
        self._pieces: list[BoardPiece] = [None] *\
            (self._configuration.size.width * self._configuration.size.height)
        self._grid_lines: list[BoardGridLine] = None

        self._piece_size = BoardPieceSize.MEDIUM

        if level <= 3:
            self._piece_size = BoardPieceSize.LARGE

        if level >= 5:
            self._piece_size = BoardPieceSize.SMALL

    def _get_index_from_position(self, position: Position) -> int:
        return position.y * self._configuration.size.width + position.x

    def _get_position_from_index(self, index) -> Position:
        y_pos = index // self._configuration.size.width
        x_pos = index - (y_pos * self._configuration.size.width)

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
            if x_pos < 0 or x_pos > self._configuration.size.width-1 or \
                y_pos < 0 or y_pos > self._configuration.size.height-1:
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
        """Changes this board's relative position on the container UI element.

        Args:
            draw_at (Position): New top-left position from which to draw board and its elements
        """
        self._offset = draw_at

        for index, piece in enumerate(self._pieces):
            position = self._get_position_from_index(index)
            piece.change_position(
                self._calculate_drawing_position(position))

        self._grid_lines = None

    def translate_event_position_to_piece_position(self,
            event_position: Position) -> Position:
        """Converts event's (e.g. mouse click) pixel position into game board
            piece's X,Y coordinate.

        Args:
            event_position (Position): Pixel position of the event

        Returns:
            Position: X,Y coordinate representing game piece on board or None if
                event position is outside the board's pieces
        """
        event_x = event_position.x - self._offset.x
        event_y = event_position.y - self._offset.y

        if event_x < 0 or event_y < 0:
            return None  # out of bounds

        piece_pixels = self._get_piece_in_pixels()

        if event_x > piece_pixels * self._configuration.size.width or\
            event_y > piece_pixels * self._configuration.size.height:
            return None  # out of bounds

        x_pos = event_x // piece_pixels
        y_pos = event_y // piece_pixels

        if x_pos >= self._configuration.size.width or y_pos >= self._configuration.size.height:
            return None  # out of bounds

        return Position(x_pos, y_pos)

    def create(self):
        """Creates or re-creates new game board content according to initialization data 
            passed in constructor.

            This method MUST be called before board can be played.
        """

        # Create plane pieces
        plane_indexes = []
        self._pieces: list[BoardPiece] = [None] *\
            (self._configuration.size.width * self._configuration.size.height)
        piece_in_pixels = self._get_piece_in_pixels()

        total_pieces = len(self._pieces)

        plane_indexes = random.sample(range(0, total_pieces), self._configuration.planes)

        for index in plane_indexes:
            position = self._get_position_from_index(index)
            self._pieces[index] = BoardPiece(
                piece_in_pixels, BoardPieceType.PLANE, None,
                self._calculate_drawing_position(position))

        # Create other pieces
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

        width = pixels * self._configuration.size.width
        height = pixels * self._configuration.size.height

        color = Color(200, 200, 200)

        for y_pos in range(0, height+1, pixels):
            self._grid_lines.append(BoardGridLine(
                Position(self._offset.x, self._offset.y + y_pos),
                Position(self._offset.x + width, self._offset.y + y_pos),
                color))

        for x_pos in range(0, width+1, pixels):
            self._grid_lines.append(BoardGridLine(
                Position(self._offset.x + x_pos, self._offset.y),
                Position(self._offset.x + x_pos, self._offset.y + height),
                color))

    def get_level(self) -> int:
        """Get current play level

        Returns:
            int: Current level
        """
        return self._configuration.level

    def get_rendering_items(self) -> list[RenderedObject]:
        """Gets all UI items consisting of the game board's current state
            (pieces and underlying grid).

        Returns:
            list[RenderedObject]: UI items
        """
        items: list(RenderedObject) = []

        if self._grid_lines is None:
            self._recalculate_grid()

        for line in self._grid_lines:
            items.append(line)

        for piece in self._pieces:
            items.append(piece)

        return items

    def get_total_planes(self) -> int:
        """Get total number of planes in the current game.

        Returns:
            int: Number of planes
        """
        return self._configuration.planes

    def get_radar_contacts(self) -> int:
        """Get total number currently marked pieces a.k.a. radar contacts.

        Returns:
            int: Number of radar contacts
        """
        marked = 0

        for piece in self._pieces:
            marked += 1 if piece.is_marked() else 0

        return marked

    def get_pieces_on_board(self) -> int:
        """Get total number of pieces on the gameboard (X x Y).

        Returns:
            int: Number of pieces on board.
        """
        return self._configuration.size.height *\
                self._configuration.size.width

    def get_dimensions(self) -> Size:
        """Get gameboard's current size.

        Returns:
            Size: Current size in pixels
        """
        return Size(self._configuration.size.width * self._get_piece_in_pixels(),
                self._configuration.size.height * self._get_piece_in_pixels())

    def get_piece_dimensions(self) -> Size:
        """Get gameboard's pieces current size.

        Returns:
            Size: Individual piece's size in pixels
        """
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

        self._state = BoardState.WON
        self._stop_clock()

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
                self._state = BoardState.LOST
                self._stop_clock()
                return

            while not result:
                self.create()
                piece = self._pieces[self._get_index_from_position(position)]
                result = piece.open()

        # if empty piece, automatically open all adjacent empty and number pieces
        if piece.get_type() == BoardPieceType.EMPTY:
            self._open_adjacent_pieces(position)

        self._check_for_win()

    def _start_clock(self):
        if self._start_time is None:
            self._start_time = time.time()

    def _stop_clock(self):
        if self._stop_time is None:
            self._stop_time = time.time()

    def open_piece(self, position: Position):
        """Perform open operation on piece at specific coordinates.

        Args:
            position (Position): Coordinates of the piece.
                Please note that this is relative coordinate of the piece, not 
                pixel coordinates i.e. 0,0 refers to piece at the top-left corner 
                of the board and 9,9 refers to bottom-right piece, assuming 9x9 board.
        """
        if self._state in (BoardState.WON, BoardState.LOST):
            return

        self._start_clock()

        index = self._get_index_from_position(position)

        piece = self._pieces[index]

        self._open_piece(piece, position)

    def mark_piece(self, position: Position):
        """Perform mark operation on piece at specific coordinates.

        Args:
            position (Position): Coordinates of the piece.
                Please note that this is relative coordinate of the piece, not 
                pixel coordinates i.e. 0,0 refers to piece at the top-left corner 
                of the board and 9,9 refers to bottom-right piece, assuming 9x9 board.
        """
        if self._state in (BoardState.WON, BoardState.LOST):
            return

        self._start_clock()

        index = self._get_index_from_position(position)

        piece = self._pieces[index]

        if piece.is_open():
            return  # no-op

        if piece.is_marked():
            # unmark
            piece.unmark()
            return

        # check if radar contacts are full
        if self.get_radar_contacts() >= self._configuration.planes:
            return

        piece.mark()

        self._check_for_win()

    def get_current_board_state(self) -> BoardState:
        """Get current play state of the gameboard.

        Returns:
            BoardState: State of the play (game running, game is won, game is lost)
        """
        return self._state

    def get_elapsed_play_time(self) -> float:
        """Get currently elapsed play time since start of first move (open or mark).

        Returns:
            float: Play time in seconds.
        """
        if self._start_time is None:
            return 0.0

        if self._stop_time is None:
            return time.time() - self._start_time

        return self._stop_time-self._start_time
