from unittest import TestCase

from jchess.geometry import V
from jchess.pieces import Piece, Player, Role
from jchess.state import GameState
from jchess.testutils import patch_inputs


class TestPawnLogic(TestCase):
    @patch_inputs("↲ ↑ ↲ ↑ ↑ ↲ ← ← ↑ ↑ ↑ ↲ ↓ ↲")
    def test_step_and_jump(self, game: GameState) -> None:
        """Checks standard 2 space and 1 space move."""
        self.assertEqual(game.board[V(2, 2)], Piece(Role.PAWN, Player.TWO, moved=True))
        self.assertEqual(game.board[V(4, 4)], Piece(Role.PAWN, Player.ONE, moved=True))

    @patch_inputs("↲ ↑ ↲ ↑ ↑ ↲ ↑ ↑ ↑ ← ↲ ↓ ↓ ↲ ↓ → ↲ ← ↑ ↲ ↑ ↑ → ↲ ↓ ↓ ↲ ← ↲ ↑ → ↲ ")
    def test_take_and_passant(self, game: GameState) -> None:
        """Checks standard 'take' and 'en passant'."""
        self.assertEqual(game.board[V(4, 2)], Piece(Role.PAWN, Player.ONE, moved=True))
        taken = game.board.taken_pieces[Player.ONE]
        self.assertEqual(taken, [Role.PAWN, Role.PAWN])

    inputs = """
        ↲ ↑ ↲ ↑ ↑ ↲ ↑ ↑ ↑ → ↲ ↓ ↓ ↲ ↓ ← ↲ ↑ → ↲ ↑ ↑ → ↲ ↓ ↲ ↓ ← ↲ ↑ → ↲ ↑ ← ← →
        → ↑ ↲ ↓ ↓ ← ↲ → ↲ ↑ → ↲ ↑ ↲ ← ↲ ↓ → ↲ ↑ ↲ ↓ ↓ ↲
    """

    @patch_inputs(inputs)
    def test_promotion(self, game: GameState) -> None:
        """Checks promotion mechanic."""
        self.assertEqual(game.board[V(7, 7)], Piece(Role.ROOK, Player.ONE, moved=False))
        taken = game.board.taken_pieces[Player.ONE]
        self.assertEqual(taken, [Role.PAWN, Role.PAWN, Role.PAWN])
