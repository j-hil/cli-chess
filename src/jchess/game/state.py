"""Contains the class representing the internal state of the game.

Draws upon the other modules in jchess/game to complete the class.
"""

from jchess.configs import Config
from jchess.geometry import Vector, VectorLike
from jchess.pieces import Piece, Player, Role
from jchess.game.logic import targets_of_
from jchess.game.engine import Action, Mode, evolve_state_
from jchess.game.visuals import generate_main_display

K, Q, R, B, N, P = list(Role)
BACK_ROW = [R, N, B, Q, K, B, N, R]


class GameState:
    """Represents the state of the game, and controls the game logic."""

    @staticmethod
    def has(coord: VectorLike) -> bool:
        return coord[0] in range(8) and coord[1] in range(8)

    def __init__(self, config: Config):
        """Initialise a `GameState`.

        :param config: Controls settings such as color, symbols etc. Several pre-made
            configs available in jchess.config. Defaults to VSC_CONFIG
        """
        self.pieces = [
            *[Piece(role, Player.TWO, (x, 0)) for x, role in enumerate(BACK_ROW)],
            *[Piece(Role.PAWN, Player.TWO, (x, 1)) for x in range(8)],
            *[Piece(Role.PAWN, Player.ONE, (x, 6)) for x in range(8)],
            *[Piece(role, Player.ONE, (x, 7)) for x, role in enumerate(BACK_ROW)],
        ]

        self.passant_vulnerable_piece: Piece | None = None
        self.turn = 0
        self.taken_pieces: dict[Player, list[Role]] = {Player.ONE: [], Player.TWO: []}

        self.attacking_piece: Piece | None = None
        self.cursor_coord = Vector(4, 7)

        self.config = config
        self.mode = Mode.ONE

    def score(self, player: Player) -> int:
        return sum(role.worth for role in self.taken_pieces[player])

    def active_player(self) -> Player:
        return list(Player)[self.turn % 2]

    def targets_of(self, piece: Piece) -> list[Vector]:
        return targets_of_(self, piece)

    def evolve_state(self, action: Action | None = None) -> None:
        evolve_state_(self, action)

    def __str__(self) -> str:
        return str(generate_main_display(self))

    def __getitem__(self, key: VectorLike) -> Piece | None:
        for piece in self.pieces:
            if piece._coord == key:
                return piece
        return None

    def __setitem__(self, key: VectorLike, value: Piece) -> None:
        value.coord = key
        self.pieces.append(value)
