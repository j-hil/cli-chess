from unittest import TestCase

from jchess.geometry import V
from jchess.pieces import Piece, Player, Role
from jchess.state import GameState
from jchess.testutils import patch_inputs


class TestPawnLogic(TestCase):
    @patch_inputs("↲ ↑ ↲ ↑ ↑ ↲ ← ← ↑ ↑ ↑ ↲ ↓ ↲")
    def test_1(self, game: GameState) -> None:
        """Checks standard 2 space and 1 space move."""
        self.assertEqual(game.board[V(2, 2)], Piece(Role.PAWN, Player.TWO, V(2, 2)))
        self.assertEqual(game.board[V(4, 4)], Piece(Role.PAWN, Player.ONE, V(4, 4)))

    @patch_inputs("↲ ↑ ↲ ↑ ↑ ↲ ↑ ↑ ↑ ← ↲ ↓ ↓ ↲ ↓ → ↲ ← ↑ ↲ ↑ ↑ → ↲ ↓ ↓ ↲ ← ↲ ↑ → ↲ ")
    def test_2(self, game: GameState) -> None:
        """Checks standard 'take' and 'en passant'."""
        self.assertEqual(game.board[V(4, 2)], Piece(Role.PAWN, Player.ONE, V(4, 2)))
        taken = game.board.taken_pieces[Player.ONE]
        self.assertEqual(taken, [Role.PAWN, Role.PAWN])

    @patch_inputs(
        """
            ↲ ↑ ↲ ↑ ↑ ↲ ↑ ↑ ↑ → ↲ ↓ ↓ ↲ ↓ ← ↲ ↑ → ↲ ↑ ↑ → ↲ ↓ ↲ ↓ ← ↲ ↑ → ↲ ↑ ← ← →
            → ↑ ↲ ↓ ↓ ← ↲ → ↲ ↑ → ↲ ↑ ↲ ← ↲ ↓ → ↲ ↑ ↲ ↓ ↓ ↲
        """
    )
    def test_3(self, game: GameState) -> None:
        """Checks promotion mechanic."""
        self.assertEqual(game.board[V(7, 7)], Piece(Role.ROOK, Player.ONE, V(7, 7)))
        taken = game.board.taken_pieces[Player.ONE]
        self.assertEqual(taken, [Role.PAWN, Role.PAWN, Role.PAWN])
