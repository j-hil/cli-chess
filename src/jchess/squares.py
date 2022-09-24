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

    ONE = auto()
    TWO = auto()
    NULL = auto()


@dataclass
class Square:
    """Representation any square on the board."""

    role: Role
    player: Player
