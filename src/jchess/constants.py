"""Various constants used throughout the project."""

from jchess.squares import Square, Player, Role, NULL_SQUARE
from jchess.display import DisplaySize

MAIN_DISPLAY_SIZE = DisplaySize(25, 88)

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
    "SCORE={1:0>3}       \n"
    "                \n"
    "                \n"
    "                "
)

#
