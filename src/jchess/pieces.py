"""Contains representation of a chess piece."""

from dataclasses import dataclass, field
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

    @property
    def name(self) -> str:
        return self.value[0]

    @property
    def symbol(self) -> str:
        return self.value[1]

    @property
    def worth(self) -> int:
        return self.value[2]

    def __repr__(self) -> str:
        return f"Role[{self.symbol}]"



@dataclass
class Piece:

    role: Role
    player: Player

    # coord and targets are managed by the containing Board class
    coord: Vector
    targets: list[Vector] = field(default_factory=list, init=False, compare=False)

    def __post_init__(self) -> None:
        self._initial_coord = self.coord

    def unmoved(self) -> bool:
        return self._initial_coord == self.coord

    def __repr__(self) -> str:
        return f"Piece({self.role.symbol}, p{self.player.value}, {self.coord})"
