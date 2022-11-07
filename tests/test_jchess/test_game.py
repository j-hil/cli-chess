from jchess.game import Game
from jchess.geometry import V
from jchess.pieces import Piece, Player, Role
from jchess.testutils import patch_inputs


@patch_inputs("↓ ↲ ↑ ↲ ↑ ↑ ↲ ← ← ↑ ↑ ↑ ↲ ↓ ↲")
def test_step_and_jump(game: Game) -> None:
    """Checks standard 2 space and 1 space move."""
    assert game.board[V(2, 2)] == Piece(Role.PAWN, Player.TWO, moved=True)
    assert game.board[V(4, 4)] == Piece(Role.PAWN, Player.ONE, moved=True)


@patch_inputs("↓ ↲ ↑ ↲ ↑ ↑ ↲ ↑ ↑ ↑ ← ↲ ↓ ↓ ↲ ↓ → ↲ ← ↑ ↲ ↑ ↑ → ↲ ↓ ↓ ↲ ← ↲ ↑ → ↲ ")
def test_take_and_passant(game: Game) -> None:
    """Checks standard 'take' and 'en passant'."""
    assert game.board[V(4, 2)] == Piece(Role.PAWN, Player.ONE, moved=True)
    taken = game.board.taken_pieces[Player.ONE]
    assert taken == [Role.PAWN, Role.PAWN]


inputs = """
    ← ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↲ ↑ ↲ ↑ ↑ ↲ ↑ ↑ ↑ → ↲ ↓ ↓ ↲ ↓ ← ↲ ↑ → ↲ ↑ ↑ → ↲ ↓ ↲ ↓ ←
    ↲ ↑ → ↲ ↑ → ↑ ← ↲ ↓ ↓ ← ↲ ↓ → ↑ ↲ ↑ → ↲ ↑ ↲ ← ↲ ↓ → ↲ ↑ ← ↲ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
    ↓ ↓ ↲ ← ← ↲ ↓ → ↲ ↑ → ↲ ↓ ↓ ↓ ↓ ↓ ↲
"""


@patch_inputs(inputs)
def test_promotion(game: Game) -> None:
    """Checks promotion mechanic."""
    assert game.board[V(6, 5)] == Piece(Role.ROOK, Player.ONE, moved=True)


@patch_inputs("↲ ↑ ↲ ↑ ↑ ↲ ← ↓ ↓ ↲ ↲ ↑ ↑ ↑ ↑ ↑ ↑ ← ↲ ↲ ↓ ↓")
def test_selection_ignored(game: Game) -> None:
    pass
