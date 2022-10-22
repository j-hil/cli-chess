"""Contains the class representing the internal state of the game."""
from enum import Enum
from typing import Any

from jchess.board import Board
from jchess.configs import DEFAULT_CONFIG, Config
from jchess.geometry import Vector
from jchess.pieces import Piece, Role
from jchess.terminal import Action

from . import _bdisplay as bdisplay
from . import _pdisplay as pdisplay


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

        # in board screen
        self.attacker: Piece | None = None
        self.cursor_b = Vector(4, 7)

        # in promotion menu
        self.cursor_p = 0
        self.promoting = False

        # printing updates
        self.config = config
        self.ctrlseq = bdisplay.init(self)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "cursor_b":
            value %= 8
        elif name == "cursor_p":
            value %= 4
        super().__setattr__(name, value)

    def evolve_state(self, action: Action) -> None:
        board = self.board
        self.ctrlseq = ""

        # while in promotion menu
        if self.promoting and self.attacker is not None:
            if action in CARDINAL_DIRECTION:
                old_cursor_p = self.cursor_p
                self.cursor_p += CARDINAL_DIRECTION[action][1]
                self.ctrlseq = pdisplay.update(self, old_cursor_p)
            elif action is Action.SELECT:
                self.attacker.role = pdisplay.OPTIONS[self.cursor_p]
                self.attacker, self.promoting = None, False
                self.ctrlseq = pdisplay.clear() + bdisplay.update(self)

        # while in board screen
        else:
            if action in CARDINAL_DIRECTION:
                self.cursor_b += CARDINAL_DIRECTION[action]

            elif action is Action.SELECT:
                attacker = self.attacker
                focus = board[self.cursor_b]

                if (
                    not attacker
                    and focus
                    and focus.player is board.player
                    and focus.targets
                ):
                    self.attacker = focus

                elif attacker and self.cursor_b in attacker.targets:
                    board.process_attack(attacker, self.cursor_b)
                    if attacker.role is Role.PAWN and attacker.coord.y in [0, 7]:
                        self.promoting = True
                        self.ctrlseq += pdisplay.init(self)
                    else:
                        self.attacker = None

            self.ctrlseq += bdisplay.update(self)


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
