"""Various constants used throughout the project."""
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
