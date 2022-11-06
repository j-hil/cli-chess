"""Contains representation of a chess piece."""

from dataclasses import dataclass
from enum import Enum

from jchess.geometry import Vector


class Player(Enum):
    ONE = 1
    TWO = 2


class Role(Enum):
    KING = ("King", "K", 104)
    QUEEN = ("Queen", "Q", 9)
    ROOK = ("Rook", "H", 5)
    BISHOP = ("Bishop", "I", 3)
    KNIGHT = ("Knight", "J", 3)
    PAWN = ("Pawn", "i", 1)
    BLANK = ("Blank", " ", 0)

    @property
    def symbol(self) -> str:
        return self.value[1]

    @property
    def worth(self) -> int:
        return self.value[2]

    def __str__(self) -> str:
        return self.value[0]

    def __repr__(self) -> str:
        return f"Role[{self.symbol}]"


@dataclass(slots=True, frozen=True)
class Piece:

    role: Role
    player: Player
    moved: bool = False

    def __repr__(self) -> str:
        m = "T" if self.moved else "F"
        return Piece.__name__ + f"({self.role.symbol}, p{self.player.value}, {m=!s})"


@dataclass(slots=True, frozen=True)
class LocPiece:
    """A 'Located Piece'; a piece with it's coordinate."""

    piece: Piece
    coord: Vector

    def __repr__(self) -> str:
        return f"[{self.piece} @ {self.coord}]"
