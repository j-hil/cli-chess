from typing import Type
from jchess.configs import Config
from jchess.game.engine import Action, Mode
from jchess.geometry import Vector, VectorLike
from jchess.pieces import Piece, Player, Role

K: Type[Role]
Q: Type[Role]
R: Type[Role]
B: Type[Role]
N: Type[Role]
P: Type[Role]
BACK_ROW: list[Type[Role]]

class GameState:
    @staticmethod
    def has(coord: VectorLike) -> bool: ...
    pieces: list[Piece]
    passant_vulnerable_piece: Piece | None
    turn: int
    taken_pieces: dict[Player, list[Role]]
    attacking_piece: Piece | None
    cursor_coord: Vector
    config: Config
    mode: Mode
    def __init__(self, config: Config) -> None: ...
    def score(self, player: Player) -> int: ...
    def active_player(self) -> Player: ...
    def targets_of(self, piece: Piece) -> list[Vector]: ...
    def evolve_state(self, action: Action | None = ...) -> None: ...
    def __getitem__(self, key: VectorLike) -> Piece | None: ...
    def __setitem__(self, key: VectorLike, value: Piece) -> None: ...
