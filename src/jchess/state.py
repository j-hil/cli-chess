"""Contains the class representing the internal state of the game."""
import sys
from enum import Enum, auto
from typing import Any

from jchess.action import Action, get_action_lhs, get_action_rhs
from jchess.board import Board
from jchess.geometry import Vector
from jchess.pieces import Piece, Player, Role


class Status(Enum):
    UNINITIALIZED = auto()
    START_MENU = auto()
    PROMOTING = auto()
    BOARD_FOCUS = auto()


class Mode(Enum):
    LMP = "Local Multi-Player"
    SPM = "Simple Single-Player"  # TODO: implement
    # RMP = "Remote Multi-Player"
    # VAI = "Versus AI"


class GameState:
    """Interface layer between the player and chess game."""

    def __init__(self) -> None:
        """Initialise a `GameState`.

        :param config: Controls settings such as color, symbols etc. Several pre-made
            configs available in jchess.config. Defaults to VSC_CONFIG
        """
        self.board = Board()

        # in board screen
        self.attacker: Piece | None = None

        self.scursor = 0
        self.bcursor = Vector(4, 7)
        self.pcursor = 0

        self.status_prev = Status.UNINITIALIZED
        self.status = Status.START_MENU

        self.mode = None

    def get_action(self) -> Action:
        player = self.board.active_player
        return get_action_rhs() if player == Player.ONE else get_action_lhs()

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "bcursor":
            value %= 8
        elif name == "pcursor":
            value %= 4
        elif name == "scursor":
            value %= len(Mode)
        super().__setattr__(name, value)

    def evolve_state(self) -> None:
        # pylint: disable=too-many-branches  # TODO: fix!

        board = self.board
        self.status_prev = self.status

        action = self.get_action()

        if action is Action.QUIT:
            sys.exit()

        # while in mode selection menu
        if self.status == Status.START_MENU:
            if action in CARDINAL_DIRECTION:
                self.scursor += CARDINAL_DIRECTION[action][1]
            if action is Action.SELECT:
                self.mode = list(Mode)[self.scursor]
                self.status_prev = self.status
                self.status = Status.BOARD_FOCUS

        # while in promotion menu (`and self.attacker` helps type checker)
        elif self.status is Status.PROMOTING and self.attacker:
            if action in CARDINAL_DIRECTION:
                self.pcursor += CARDINAL_DIRECTION[action][1]
            elif action is Action.SELECT:
                self.attacker.role = PROMOTION_OPTIONS[self.pcursor]
                board.process_attack(self.attacker, self.bcursor)
                self.attacker = None
                self.status = Status.BOARD_FOCUS

        # while in board screen
        elif self.status is Status.BOARD_FOCUS:
            if action in CARDINAL_DIRECTION:
                self.bcursor += CARDINAL_DIRECTION[action]

            elif action is Action.SELECT:
                attacker = self.attacker
                focus = board[self.bcursor]

                if (
                    not attacker
                    and focus
                    and focus.player is board.active_player
                    and focus.targets
                ):
                    self.attacker = focus

                elif attacker and self.bcursor in attacker.targets:
                    if (
                        attacker.role is Role.PAWN
                        and attacker.coord.y in [1, 6]
                        and not attacker.unmoved()
                    ):
                        self.status = Status.PROMOTING
                    else:
                        board.process_attack(attacker, self.bcursor)
                        self.attacker = None


CARDINAL_DIRECTION: dict[Action, tuple[int, int]] = {
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

PROMOTION_OPTIONS = (Role.QUEEN, Role.KNIGHT, Role.ROOK, Role.BISHOP)
