"""Contains representation of a chess piece."""

from enum import Enum
from jchess.geometry import Vector, VectorLike


class Piece:
    def __init__(self, role: "Role", player: "Player", coord: VectorLike):
        self.role = role
        self.player = player
        self._coord = self._initial_coord = Vector(*coord)
        self.targets: list[Vector] = []

    @property
    def coord(self) -> Vector:
        return self._coord

    @coord.setter
    def coord(self, value: VectorLike) -> None:
        self._coord = Vector(*value)

    def has_not_moved(self) -> bool:
        return self._initial_coord == self._coord

    def __repr__(self) -> str:
        return f"Piece({self.role.value[0]}, P{self.player.value}, {self._coord})"


class Player(Enum):
    ONE = 1
    TWO = 2


class Role(Enum):
    KING = ("K", 104)
    QUEEN = ("Q", 9)
    ROOK = ("R", 5)
    BISHOP = ("B", 3)
    KNIGHT = ("N", 3)
    PAWN = ("P", 1)

    @property
    def worth(self) -> int:
        return self.value[1]
