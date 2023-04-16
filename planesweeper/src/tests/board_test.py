import unittest
from primitives.position import Position
from primitives.size import Size
from entities.board_piece import BoardPiece, BoardPieceType
from entities.ui.board_grid_item import BoardGridItem
from entities.board import Gameboard, GameboardConfiguration, BoardState


class TestGameboard(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_level1_board_with_random_planes(self):
        level = 1
        board = Gameboard(level)
        board.create()

        planes = 0

        for piece in board._pieces:
            self.assertNotEqual(piece, None)
            if piece.get_type() == BoardPieceType.PLANE:
                planes += 1

        self.assertEqual(planes, GameboardConfiguration.LEVELS[level][1])

    def test_create_level2_board_with_random_planes(self):
        level = 2
        board = Gameboard(level)
        board.create()

        planes = 0

        for piece in board._pieces:
            self.assertNotEqual(piece, None)
            if piece.get_type() == BoardPieceType.PLANE:
                planes += 1

        self.assertEqual(planes, GameboardConfiguration.LEVELS[level][1])

    def test_create_level3_board_with_random_planes(self):
        level = 3
        board = Gameboard(level)
        board.create()

        planes = 0

        for piece in board._pieces:
            self.assertNotEqual(piece, None)
            if piece.get_type() == BoardPieceType.PLANE:
                planes += 1

        self.assertEqual(planes, GameboardConfiguration.LEVELS[level][1])

    def test_create_level4_board_with_random_planes(self):
        level = 4
        board = Gameboard(level)
        board.create()

        planes = 0

        for piece in board._pieces:
            self.assertNotEqual(piece, None)
            if piece.get_type() == BoardPieceType.PLANE:
                planes += 1

        self.assertEqual(planes, GameboardConfiguration.LEVELS[level][1])

    def test_create_level5_board_with_random_planes(self):
        level = 5
        board = Gameboard(level)
        board.create()

        planes = 0

        for piece in board._pieces:
            self.assertNotEqual(piece, None)
            if piece.get_type() == BoardPieceType.PLANE:
                planes += 1

        self.assertEqual(planes, GameboardConfiguration.LEVELS[level][1])

    def test_create_level6_board_with_random_planes(self):
        level = 6
        board = Gameboard(level)
        board.create()

        planes = 0

        for piece in board._pieces:
            self.assertNotEqual(piece, None)
            if piece.get_type() == BoardPieceType.PLANE:
                planes += 1

        self.assertEqual(planes, GameboardConfiguration.LEVELS[level][1])

    def test_incorrect_levels_not_accepted(self):
        with self.assertRaises(ValueError):
            Gameboard(min(GameboardConfiguration.LEVELS.keys())-1)
        with self.assertRaises(ValueError):
            Gameboard(max(GameboardConfiguration.LEVELS.keys())+1)

    def test_correct_reported_number_of_planes(self):
        for level in GameboardConfiguration.LEVELS.keys():
            planes = GameboardConfiguration.LEVELS[level][1]
            board = Gameboard(level)
            board.create()

            self.assertEqual(planes, board.get_total_planes())
    
    def test_correct_reported_level(self):
        for level in GameboardConfiguration.LEVELS.keys():
            board = Gameboard(level)
            board.create()

            self.assertEqual(level, board.get_level())

    def test_playthrough_win_is_possible(self):
        level = 6
        board = Gameboard(level)
        board.create()

        for index, piece in enumerate(board._pieces):
            pos = board._get_position_from_index(index)

            if piece.is_open():
                continue

            piece_type = piece.get_type()

            if piece_type == BoardPieceType.PLANE:
                board.mark_piece(pos)
            else:
                board.open_piece(pos)

        self.assertEqual(board.get_current_board_state(), BoardState.WON)

    def test_open_plane_piece_first_recreates_pieces(self):
        board = Gameboard(5)
        board.create()

        # as fairness algorithm ensures no first open can be plane
        # opening plane first should never result losing

        for index, piece in enumerate(board._pieces):
            pos = board._get_position_from_index(index)

            piece_type = piece.get_type()

            if piece_type == BoardPieceType.PLANE:
                board.open_piece(pos)
                break

        self.assertEqual(board.get_current_board_state(), BoardState.RUNNING)

    def test_open_plane_piece_cause_losing(self):
        board = Gameboard(6)
        board.create()

        # as fairness algorithm ensures no first open can be plane
        # we have to open one other number piece (to not propage open to others) 
        # first before opening plane to end game

        for index, piece in enumerate(board._pieces):
            pos = board._get_position_from_index(index)

            piece_type = piece.get_type()

            if piece_type == BoardPieceType.NUMBER:
                board.open_piece(pos)
                break

        for index, piece in enumerate(board._pieces):
            pos = board._get_position_from_index(index)

            piece_type = piece.get_type()

            if piece_type == BoardPieceType.PLANE:
                board.open_piece(pos)
                break

        self.assertEqual(board.get_current_board_state(), BoardState.LOST)

    def test_losing_does_not_allow_further_open_or_mark(self):
        board = Gameboard(6)
        board.create()

        opened_index = None
        plane_index = None

        # as fairness algorithm ensures no first open can be plane
        # we have to open one other number piece (to not propage open to others) 
        # first before opening plane to end game

        for index, piece in enumerate(board._pieces):
            pos = board._get_position_from_index(index)

            piece_type = piece.get_type()

            if piece_type == BoardPieceType.NUMBER:
                board.open_piece(pos)
                opened_index = index
                break

        for index, piece in enumerate(board._pieces):
            pos = board._get_position_from_index(index)

            piece_type = piece.get_type()

            if piece_type == BoardPieceType.PLANE:
                board.open_piece(pos)
                plane_index = index
                break

        for index, piece in enumerate(board._pieces):
            pos = board._get_position_from_index(index)

            if index == opened_index or index == plane_index:
                continue

            board.open_piece(pos)

            self.assertEqual(piece.is_open(), False)

    def test_marking_and_unmarking_works(self):
        board = Gameboard(3)
        board.create()

        for index, piece in enumerate(board._pieces):
            pos = board._get_position_from_index(index)

            piece_type = piece.get_type()

            if piece_type == BoardPieceType.PLANE:
                board.mark_piece(pos)

                self.assertEqual(board.get_current_board_state(), BoardState.RUNNING)
                self.assertEqual(piece.is_marked(), True)
                self.assertEqual(piece.is_open(), False)

                board.mark_piece(pos)

                self.assertEqual(board.get_current_board_state(), BoardState.RUNNING)
                self.assertEqual(piece.is_marked(), False)
                self.assertEqual(piece.is_open(), False)

                break

        self.assertEqual(board.get_current_board_state(), BoardState.RUNNING)

    def test_opening_marked_piece_is_prevented(self):
        board = Gameboard(3)
        board.create()

        for index, piece in enumerate(board._pieces):
            pos = board._get_position_from_index(index)

            piece_type = piece.get_type()

            if piece_type == BoardPieceType.PLANE:
                board.mark_piece(pos)
                board.open_piece(pos)

                self.assertEqual(board.get_current_board_state(), BoardState.RUNNING)
                self.assertEqual(piece.is_marked(), True)
                self.assertEqual(piece.is_open(), False)

                break

        self.assertEqual(board.get_current_board_state(), BoardState.RUNNING)

    def test_radar_marks_cannot_exceed_plane_count(self):
        board = Gameboard(5)
        board.create()

        for index, piece in enumerate(board._pieces):
            pos = board._get_position_from_index(index)
            board.mark_piece(pos)

        marked = 0

        for index, piece in enumerate(board._pieces):
            if piece._marked:
                marked += 1

        planes = board.get_total_planes()

        self.assertEqual(marked, planes)

    def test_board_repositioning_works(self):
        board = Gameboard(4)
        board.create()
        board.change_position(Position(5,5))

        self.assertEqual(board._offset.x, 5)
        self.assertEqual(board._offset.y, 5)

    def test_event_position_translation_returns_piece_position(self):
        board = Gameboard(4)
        board.create()
        board.change_position(Position(50,50))

        piece_dimensions = board._pieces[0].get_dimensions()

        # top-left corner piece
        event_position = Position(50 + piece_dimensions.width // 2, 
                                  50 + piece_dimensions.height // 2)
        
        piece_position = board.translate_event_position_to_piece_position(event_position)

        self.assertEqual(piece_position.x, 0)
        self.assertEqual(piece_position.y, 0)

        # bottom-right corner piece

        event_position = Position(50 + (board._configuration.size.width * piece_dimensions.width) - piece_dimensions.width // 2, 
                                  50 + (board._configuration.size.height * piece_dimensions.height) - piece_dimensions.height // 2)
        
        piece_position = board.translate_event_position_to_piece_position(event_position)

        self.assertEqual(piece_position.x, board._configuration.size.width - 1)
        self.assertEqual(piece_position.y, board._configuration.size.height - 1)

    def test_outside_event_position_translation_returns_none(self):
        board = Gameboard(4)
        board.create()
        board.change_position(Position(50,50))

        piece_dimensions = board._pieces[0].get_dimensions()

        # outside left boundary
        event_position = Position(45, 55)
        
        piece_position = board.translate_event_position_to_piece_position(event_position)

        self.assertEqual(piece_position, None)

        # outside top boundary
        event_position = Position(55, 45)
        
        piece_position = board.translate_event_position_to_piece_position(event_position)

        self.assertEqual(piece_position, None)

        # outside right boundary

        event_position = Position(50 + (board._configuration.size.width * piece_dimensions.width) + piece_dimensions.width // 2, 
                                  50 + (board._configuration.size.height * piece_dimensions.height) - piece_dimensions.height // 2)
        
        piece_position = board.translate_event_position_to_piece_position(event_position)

        self.assertEqual(piece_position, None)

        # outside bottom boundary

        event_position = Position(50 + (board._configuration.size.width * piece_dimensions.width) - piece_dimensions.width // 2, 
                                  50 + (board._configuration.size.height * piece_dimensions.height) + piece_dimensions.height // 2)
        
        piece_position = board.translate_event_position_to_piece_position(event_position)

        self.assertEqual(piece_position, None)

    def test_returns_necessary_rendering_items(self):
        board = Gameboard(1)
        board.create()
        
        rendering_items = board.get_rendering_items()

        pieces = 0
        grid_lines = 0

        for item in rendering_items:
            if isinstance(item, BoardPiece):
                pieces += 1
            if isinstance(item, BoardGridItem):
                grid_lines += 1

        # width x height pieces for board
        self.assertEqual(pieces, board._configuration.size.width * board._configuration.size.height)

        # width+1 + height+1 grid lines for board
        self.assertEqual(grid_lines, board._configuration.size.width + 1 + board._configuration.size.height + 1)

    def test_returns_correct_piece_dimensions(self):
        for level in GameboardConfiguration.LEVELS.keys():
            board = Gameboard(level)
            board.create()

            piece_size = board.get_piece_dimensions()

            in_pixels = board._get_piece_in_pixels()

            self.assertEqual(piece_size, Size(in_pixels, in_pixels))

    def test_pieces_are_creted_in_correct_size(self):
        for level in GameboardConfiguration.LEVELS.keys():
            board = Gameboard(level)
            board.create()

            in_pixels = board._get_piece_in_pixels()

            self.assertEqual(board._pieces[0]._size, in_pixels)
            
