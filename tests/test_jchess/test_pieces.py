from unittest import TestCase

from jchess.geometry import V
from jchess.pieces import Piece, Player, Role


class TestPiece(TestCase):
    """Test `jchess.pieces.Piece`."""

    def test_has_moved(self) -> None:
        queen = Piece(Role.QUEEN, Player.ONE, V(1, 2))
        queen.coord = V(3, 4)

        self.assertEqual(queen.coord, V(3, 4))
        self.assertFalse(queen.unmoved())

    def test_eq(self) -> None:
        piece0 = Piece(Role.BISHOP, Player.ONE, V(1, 2))
        pieces = [
            Piece(Role.BISHOP, Player.TWO, V(1, 2)),
            Piece(Role.KNIGHT, Player.ONE, V(1, 2)),
            Piece(Role.BISHOP, Player.ONE, V(1, 3)),
        ]
        for piece in pieces:
            self.assertNotEqual(piece, piece0)
        self.assertEqual(piece0, Piece(Role.BISHOP, Player.ONE, V(1, 2)))


class TestRole(TestCase):
    """Test `jchess.pieces.Role`."""

    # mostly tested through TestPieces

    def test_wroth(self):
        self.assertEqual(Role.QUEEN.worth, 9)
        self.assertEqual(Role.PAWN.worth, 1)
