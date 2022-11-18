"""Contains representation of a chess piece."""

from dataclasses import dataclass
from enum import Enum

from jchess.geometry import Vector


class Player(Enum):
    """Role enum - contains associated data."""

    ONE = 1
    TWO = 2

    def __str__(self) -> str:
        return "ONE" if int(self) == 1 else "TWO"

    def __int__(self) -> int:
        return self.value

    def __invert__(self) -> "Player":
        return Player.ONE if self is Player.TWO else Player.TWO


class Role(Enum):
    """Role enum - contains associated data."""

    KING = ("King", "K", -1)
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
    """Internal representation of a chess piece."""

    role: Role
    player: Player
    # `moved` is only used for pawns, castles and kings.
    moved: bool = False

    def __repr__(self) -> str:
        m = "T" if self.moved else "F"
        return Piece.__name__ + f"({self.role.symbol}, p{self.player.value}, {m=!s})"


@dataclass(slots=True, frozen=True)
class LocPiece:
    """A 'Located Piece' - a piece with it's coordinate."""

    piece: Piece
    coord: Vector

    def __repr__(self) -> str:
        return f"[{self.piece} @ {self.coord}]"
