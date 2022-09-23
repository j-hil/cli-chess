from dataclasses import dataclass
from enum import Enum, auto


class Role(Enum):
    KING = auto()
    QUEEN = auto()
    ROOK = auto()
    BISHOP = auto()
    KNIGHT = auto()
    PAWN = auto()
    NULL = auto()


class Player(Enum):
    ONE = auto()
    TWO = auto()
    NULL = auto()


@dataclass
class Piece:
    role: Role
    player: Player
