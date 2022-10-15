"""Contains the class representing the internal state of the game."""
import sys
from enum import Enum

from jchess.board import Board
from jchess.pieces import Piece
from jchess.configs import DEFAULT_CONFIG, Config
from jchess.geometry import Vector
from jchess.terminal import Action, get_user_action


class Mode(Enum):
    ONE = "single player"
    TWO = "online multi-player"
    THREE = "local multi-player"


class GameState:
    """Interface layer between the player and chess game."""

    def __init__(self, config: Config = DEFAULT_CONFIG):
        """Initialise a `GameState`.

        :param config: Controls settings such as color, symbols etc. Several pre-made
            configs available in jchess.config. Defaults to VSC_CONFIG
        """
        self.board = Board()

        self.attacking_piece: Piece | None = None
        self.cursor_coord = Vector(4, 7)

        self.config = config
        self.mode = Mode.ONE

    def evolve_state(self) -> None:

        board = self.board
        action = get_user_action()

        if action in CARDINAL_DIRECTION:

            # account for fact that user's view is rotated from the internal view
            if self.mode is Mode.TWO:
                action = ROTATE.get(action, action)

            new_cursor_coord = self.cursor_coord + CARDINAL_DIRECTION[action]
            if board.has(new_cursor_coord):
                self.cursor_coord = new_cursor_coord

        elif action is Action.SELECT:
            attacker = self.attacking_piece
            cursor_piece = board[self.cursor_coord]
            if (
                attacker is None
                and cursor_piece is not None
                and cursor_piece.player is board.active_player
                and cursor_piece.targets != []
            ):
                self.attacking_piece = cursor_piece
            elif attacker is not None and self.cursor_coord in attacker.targets:
                board.process_attack(attacker, self.cursor_coord)
                self.attacking_piece = None

        elif action is Action.QUIT:
            sys.exit()


CARDINAL_DIRECTION = {
    Action.UP: (0, -1),
    Action.DOWN: (0, +1),
    Action.LEFT: (-1, 0),
    Action.RIGHT: (+1, 0),
}

ROTATE = {
    Action.UP: Action.LEFT,
    Action.DOWN: Action.RIGHT,
    Action.RIGHT: Action.UP,
    Action.LEFT: Action.DOWN,
}
