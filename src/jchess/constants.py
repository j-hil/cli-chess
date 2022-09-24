"""Various constants used throughout the project.

Purely exists for aesthetic purposes; each constant is only used within one file.
"""

from itertools import product
from jchess.squares import Square, Player, Role, NULL_SQUARE

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
    [Square(role, Player.ONE) for role in _BACK_ROW],
    [Square(Role.PAWN, Player.ONE) for _ in range(8)],
    *[[NULL_SQUARE for _ in range(8)] for _ in range(4)],
    [Square(Role.PAWN, Player.TWO) for _ in range(8)],
    [Square(role, Player.TWO) for role in _BACK_ROW],
]
STANDARD_CHESS_BOARD: list[list[Square]] = list(map(list, zip(*_TRANSPOSED_BOARD)))

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

# 19 x 39
BOARD_TEMPLATE = (
    "     a   b   c   d   e   f   g   h     \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 0 |   |   |   |   |   |   |   |   | 0 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 1 |   |   |   |   |   |   |   |   | 1 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 2 |   |   |   |   |   |   |   |   | 2 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 3 |   |   |   |   |   |   |   |   | 3 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 4 |   |   |   |   |   |   |   |   | 4 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 5 |   |   |   |   |   |   |   |   | 5 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 6 |   |   |   |   |   |   |   |   | 6 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 7 |   |   |   |   |   |   |   |   | 7 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    "     a   b   c   d   e   f   g   h     "
)

# 6 x 16
PLAYER_INFO_TEMPLATE = (
    "PLAYER {0: <3}      \n"
    "                \n"
    "SCORE={1: <2}        \n"
    "                \n"
    "                \n"
    "                "
)

PIECE_VALUE = {
    Role.QUEEN: 9,
    Role.ROOK: 5,
    Role.BISHOP: 3,
    Role.KNIGHT: 3,
    Role.PAWN: 1,
}
