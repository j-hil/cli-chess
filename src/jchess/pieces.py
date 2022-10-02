from enum import Enum
from jchess.geometry import Vector, VectorLike


class Piece:
    def __init__(self, role: "Role", player: "Player", coord: VectorLike):
        self.role = role
        self.player = player
        self._coord = self._initial_coord = Vector(*coord)

    @property
    def coord(self) -> Vector:
        return self._coord

    @coord.setter
    def coord(self, value: VectorLike):
        self._coord = Vector(*value)

    def has_not_moved(self) -> bool:
        return self._initial_coord == self._coord

    def __repr__(self) -> str:
        return f"Piece({self.role}, {self.player}, {self._coord})"


class Player(Enum):
    ONE = "ONE"
    TWO = "TWO"


class Role(Enum):
    KING = ("KING", 104)
    QUEEN = ("QUEEN", 9)
    ROOK = ("ROOK", 5)
    BISHOP = ("BISHOP", 3)
    KNIGHT = ("KNIGHT", 3)
    PAWN = ("PAWN", 1)

    @property
    def worth(self) -> int:
        return self.value[1]
