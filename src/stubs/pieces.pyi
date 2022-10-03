from enum import Enum
from jchess.geometry import Vector, VectorLike

class Piece:

    role: Role
    player: Player

    def __init__(self, role: Role, player: Player, coord: VectorLike) -> None: ...

    @property
    def coord(self) -> Vector: ...

    @coord.setter
    def coord(self, value: VectorLike) -> None: ...

    def has_not_moved(self) -> bool: ...

class Player(Enum):
    ONE: str
    TWO: str

class Role(Enum):
    KING: tuple[str, int]
    QUEEN: tuple[str, int]
    ROOK: tuple[str, int]
    BISHOP: tuple[str, int]
    KNIGHT: tuple[str, int]
    PAWN: tuple[str, int]

    @property
    def worth(self) -> int: ...
