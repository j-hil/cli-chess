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

    def unmoved(self) -> bool:
        return self._initial_coord == self._coord

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Piece):
            return NotImplemented
        return (
            self.role == other.role
            and self.player == other.player
            and self.coord == other.coord
        )

    def __repr__(self) -> str:
        return f"Piece({self.role.symbol}, p{self.player.value}, {self._coord})"


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
    def symbol(self) -> str:
        return self.value[1]

    @property
    def worth(self) -> int:
        return self.value[2]

    def __str__(self) -> str:
        return self.value[0]
