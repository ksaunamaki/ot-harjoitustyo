import unittest
from entities.board_piece import BoardPiece,BoardPieceType
from entities.board import Gameboard

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
            if piece._type == BoardPieceType.Plane:
                planes += 1
        
        self.assertEqual(planes, Gameboard.LEVELS[level][1])

    def test_create_level2_board_with_random_planes(self):
        level = 2
        board = Gameboard(level)
        board.create()

        planes = 0

        for piece in board._pieces:
            self.assertNotEqual(piece, None)
            if piece._type == BoardPieceType.Plane:
                planes += 1
        
        self.assertEqual(planes, Gameboard.LEVELS[level][1])

    def test_create_level3_board_with_random_planes(self):
        level = 3
        board = Gameboard(level)
        board.create()

        planes = 0

        for piece in board._pieces:
            self.assertNotEqual(piece, None)
            if piece._type == BoardPieceType.Plane:
                planes += 1
        
        self.assertEqual(planes, Gameboard.LEVELS[level][1])

    def test_create_level4_board_with_random_planes(self):
        level = 4
        board = Gameboard(level)
        board.create()

        planes = 0

        for piece in board._pieces:
            self.assertNotEqual(piece, None)
            if piece._type == BoardPieceType.Plane:
                planes += 1
        
        self.assertEqual(planes, Gameboard.LEVELS[level][1])

    def test_create_level5_board_with_random_planes(self):
        level = 5
        board = Gameboard(level)
        board.create()

        planes = 0

        for piece in board._pieces:
            self.assertNotEqual(piece, None)
            if piece._type == BoardPieceType.Plane:
                planes += 1
        
        self.assertEqual(planes, Gameboard.LEVELS[level][1])

    def test_create_level6_board_with_random_planes(self):
        level = 6
        board = Gameboard(level)
        board.create()

        planes = 0

        for piece in board._pieces:
            self.assertNotEqual(piece, None)
            if piece._type == BoardPieceType.Plane:
                planes += 1
        
        self.assertEqual(planes, Gameboard.LEVELS[level][1])