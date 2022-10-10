"""Contains the class representing the internal state of the game.

Draws upon the other modules in jchess/game to complete the class.
"""

from jchess.board import Board
from jchess.configs import VSC_CONFIG, Config
from jchess.geometry import Vector
from jchess.pieces import Piece
from jchess.game.engine import Action, Mode, evolve_state_
from jchess.game.visuals import generate_main_display


class GameState:
    """Represents the state of the game, and controls the game logic."""

    def __init__(self, config: Config = VSC_CONFIG, board: Board | None = None):
        """Initialise a `GameState`.

        :param config: Controls settings such as color, symbols etc. Several pre-made
            configs available in jchess.config. Defaults to VSC_CONFIG
        """
        if board is None:
            self.board = Board()

        self.attacking_piece: Piece | None = None
        self.cursor_coord = Vector(4, 7)

        self.config = config
        self.mode = Mode.ONE

    def evolve_state(self, action: Action | None = None) -> None:
        evolve_state_(self, action)

    def __str__(self) -> str:
        return str(generate_main_display(self))
