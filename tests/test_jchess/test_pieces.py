from unittest import TestCase

from jchess.geometry import Vector
from jchess.pieces import Piece, Player, Role


class TestPiece(TestCase):
    """Test `jchess.pieces.Piece`."""

    def test_coord(self) -> None:
        bishop = Piece(Role.BISHOP, Player.TWO, (1, 2))
        self.assertEqual(bishop.coord, (1, 2))
        self.assertTrue(isinstance(bishop.coord, Vector))
        bishop.coord = (5, 4)
        self.assertEqual(bishop.coord, (5, 4))
        self.assertTrue(isinstance(bishop.coord, Vector))

    def test_has_moved(self) -> None:
        queen = Piece(Role.QUEEN, Player.ONE, (1, 2))
        queen.coord = (3, 4)

        self.assertEqual(queen.coord, Vector(3, 4))
        self.assertFalse(queen.unmoved())

    def test_eq(self) -> None:
        piece0 = Piece(Role.BISHOP, Player.ONE, (1, 2))
        pieces = [
            Piece(Role.BISHOP, Player.TWO, (1, 2)),
            Piece(Role.KNIGHT, Player.ONE, (1, 2)),
            Piece(Role.BISHOP, Player.ONE, (1, 3)),
        ]
        for piece in pieces:
            self.assertNotEqual(piece, piece0)
        self.assertEqual(piece0, Piece(Role.BISHOP, Player.ONE, (1, 2)))

    def test_repr(self) -> None:
        self.assertEqual(
            repr(Piece(Role.QUEEN, Player.ONE, (1, 2))), "Piece(Q, p1, V(1, 2))"
        )


class TestRole(TestCase):
    """Test `jchess.pieces.Role`."""

    # mostly tested through TestPieces

    def test_wroth(self):
        self.assertEqual(Role.QUEEN.worth, 9)
        self.assertEqual(Role.PAWN.worth, 1)
