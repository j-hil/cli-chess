"""Various constants used throughout the project.

Purely exists for aesthetic purposes; each constant is only used within `state.py`.
"""

from itertools import product
from jchess.pieces import Piece, Player, Role

_BACK_ROW = [
    Role.ROOK,
    Role.KNIGHT,
    Role.BISHOP,
    Role.QUEEN,
    Role.KING,
    Role.BISHOP,
    Role.KNIGHT,
    Role.ROOK,
]

_TRANSPOSED_BOARD = [
    [Piece(role, Player.ONE) for role in _BACK_ROW],
    [Piece(Role.PAWN, Player.ONE) for _ in range(8)],
    *[[Piece(Role.NULL, Player.NULL) for _ in range(8)] for _ in range(4)],
    [Piece(Role.PAWN, Player.TWO) for _ in range(8)],
    [Piece(role, Player.TWO) for role in _BACK_ROW],
]
STANDARD_CHESS_BOARD: list[list[Piece]] = list(map(list, zip(*_TRANSPOSED_BOARD)))

DELTAS: dict[Role, list[tuple[int, int]]] = {
    # pylint: disable=unnecessary-comprehension  # mypy can't tell types if `list` used
    Role.KING: [(x, y) for x, y in product([-1, 0, +1], repeat=2)],
    Role.KNIGHT: (
        [(s * 2, t * 1) for s, t in product([1, -1], repeat=2)]
        + [(s * 1, t * 2) for s, t in product([1, -1], repeat=2)]
    ),
}

_ROOK_LINES = [
    [(s * d, t * d) for d in range(1, 8)] for s, t in [(0, 1), (1, 0), (-1, 0), (0, -1)]
]

_BISHOP_LINES = [
    [(s * d, t * d) for d in range(1, 8)] for s, t in product([1, -1], repeat=2)
]

LINES = {
    Role.QUEEN: _ROOK_LINES + _BISHOP_LINES,
    Role.ROOK: _ROOK_LINES,
    Role.BISHOP: _BISHOP_LINES,
}

INPUT_DELTAS: dict[str, tuple[int, int]] = {
    "\x00H": (0, -1),
    "\x00P": (0, +1),
    "\x00K": (-1, 0),
    "\x00M": (+1, 0),
}
