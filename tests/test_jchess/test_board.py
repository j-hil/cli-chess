from unittest import TestCase

from jchess.board import Board
from jchess.geometry import Vector
from jchess.pieces import Piece, Player, Role


class TestBoard(TestCase):
    """Test `jchess.board.Board`."""

    def setUp(self):
        self.board = Board()

    def test_has(self):
        self.assertTrue(Board.has((0, 7)))
        self.assertFalse(Board.has((-1, -1)))

        self.assertTrue(Board.has(Vector(1, 4)))
        self.assertFalse(Board.has(Vector(8, 1)))

    def test_init(self):
        self.assertEqual(len(self.board.pieces), 32)

    def test_getsetdel_item(self):

        self.assertEqual(self.board[0, 6], Piece(Role.PAWN, Player.ONE, (0, 6)))
        self.assertIsNone(self.board[0, 5])

        del self.board[0, 6]
        self.assertIsNone(self.board[0, 6])

        rook = Piece(Role.ROOK, Player.TWO, (1, 1))
        self.board[0, 6] = rook
        self.assertEqual(rook.coord, (0, 6))
        self.assertEqual(self.board[0, 6], rook)
