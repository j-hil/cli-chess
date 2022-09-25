"""Creates representation of a chess piece."""
from dataclasses import dataclass
from enum import Enum, auto


class Role(Enum):
    """Each type chess piece and a `Null` for empty squares."""

    KING = auto()
    QUEEN = auto()
    ROOK = auto()
    BISHOP = auto()
    KNIGHT = auto()
    PAWN = auto()
    NULL = auto()


class Player(Enum):
    """Which player (if any) that a square or turn belongs to."""

    ONE = "ONE"
    TWO = "TWO"
    NULL = "NULL"


@dataclass
class Square:
    """Representation any square on the board."""

    role: Role
    player: Player


NULL_SQUARE = Square(Role.NULL, Player.NULL)

# if every white pawn where to turn into a queen, and then black captured all enemy
# pieces, black would be left with a score of
#   9 * 8 + 2 * 5 + 2 * 3 + 2 * 3 + 1 * 9 = 103
# so we set Role.KING = 104 so that a score > 103 is an unambiguous win condition.
PIECE_VALUE = {
    Role.KING: 104,
    Role.QUEEN: 9,
    Role.ROOK: 5,
    Role.BISHOP: 3,
    Role.KNIGHT: 3,
    Role.PAWN: 1,
}
