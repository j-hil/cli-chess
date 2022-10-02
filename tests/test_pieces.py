from unittest import TestCase
from jchess.geometry import Vector

from jchess.pieces import Piece, Player, Role


class TestPiece(TestCase):
    """Test `jchess.pieces.Piece`."""

    def test_has_moved(self) -> None:
        queen = Piece(Role.QUEEN, Player.ONE, Vector(1, 2))
        queen.coord = (3, 4)

        self.assertEqual(queen.coord, Vector(3, 4))
        self.assertFalse(queen.has_not_moved())
