from unittest import TestCase
from unittest.mock import patch

from jchess.pieces import Piece, Player, Role
from jchess.state import GameState
from tests.utils import patch_inputs


class TestPawnLogic(TestCase):
    @patch_inputs("↲ ↑ ↲ ↑ ↑ ↲ ← ← ↑ ↑ ↑ ↲ ↓ ↲")
    def test_1(self, game: GameState):
        """Checks standard 2 space and 1 space move."""
        self.assertEqual(game.board[2, 2], Piece(Role.PAWN, Player.TWO, (2, 2)))
        self.assertEqual(game.board[4, 4], Piece(Role.PAWN, Player.ONE, (4, 4)))

    @patch_inputs("↲ ↑ ↲ ↑ ↑ ↲ ↑ ↑ ↑ ← ↲ ↓ ↓ ↲ ↓ → ↲ ← ↑ ↲ ↑ ↑ → ↲ ↓ ↓ ↲ ← ↲ ↑ → ↲ ")
    def test_2(self, game: GameState):
        """Checks standard 'take' and 'en passant'."""
        self.assertEqual(game.board[4, 2], Piece(Role.PAWN, Player.ONE, (4, 2)))
        taken = game.board.taken_pieces[Player.ONE]
        self.assertEqual(taken, [Role.PAWN, Role.PAWN])

    @patch_inputs(
        "↲ ↑ ↲ ↑ ↑ ↲ ↑ ↑ ↑ → ↲ ↓ ↓ ↲ ↓ ← ↲ ↑ → ↲ ↑ ↑ → ↲ ↓ ↲ ↓ ← ↲ ↑ → ↲ ↑ ← ← → "
        "→ ↑ ↲ ↓ ↓ ← ↲ → ↲ ↑ → ↲ ↑ ↲ ← ↲ ↓ → ↲ ↑ ↲ ↓ ↓ ↲"
    )
    def test_3(self, game: GameState):
        """Checks promotion mechanic."""
        self.assertEqual(game.board[7, 7], Piece(Role.ROOK, Player.ONE, (7, 7)))
        taken = game.board.taken_pieces[Player.ONE]
        self.assertEqual(taken, [Role.PAWN, Role.PAWN, Role.PAWN])
