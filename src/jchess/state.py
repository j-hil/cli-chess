"""Contains the class representing the internal state of the game."""
import sys
from enum import Enum, auto
from typing import Any

from jchess.action import Action, get_action_lhs, get_action_rhs
from jchess.board import Board
from jchess.geometry import V, Vector
from jchess.pieces import Player, Role, Square


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

        self.attacker: Square | None = None

        self.scursor = 0
        self.bcursor = V(4, 7)
        self.pcursor = 0

        self.status_prev = Status.UNINITIALIZED
        self.status = Status.START_MENU

        self.mode: Mode | None = None

    def get_action(self) -> Action:
        player = self.board.active_player
        return get_action_rhs() if player == Player.ONE else get_action_lhs()

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "bcursor":
            value %= 8
        elif name == "pcursor":
            value %= len(PROMOTION_OPTIONS)
        elif name == "scursor":
            value %= len(Mode)
        super().__setattr__(name, value)

    def evolve_state(self) -> None:
        action = self.get_action()
        board = self.board
        status = self.status_prev = self.status
        attacker = self.attacker

        if action is Action.QUIT:
            sys.exit()

        # while in mode selection menu
        if status is Status.START_MENU:
            self.scursor += CARDINAL_DIRECTION.get(action, V(0, 0)).y
            if action is Action.SELECT:
                self.mode = list(Mode)[self.scursor]
                self.status = Status.BOARD_FOCUS

        # while in promotion menu
        elif status is Status.PROMOTING:
            assert attacker, "Can only promote if an attacker is selected"
            self.pcursor += CARDINAL_DIRECTION.get(action, V(0, 0)).y
            if action is Action.SELECT:
                board.process_move(
                    attacker.coord,
                    self.bcursor,
                    promote_to=PROMOTION_OPTIONS[self.pcursor],
                )
                self.attacker = None
                self.status = Status.BOARD_FOCUS

        # while in board screen
        else:  # (status is Status.BOARD_FOCUS)
            self.bcursor += CARDINAL_DIRECTION.get(action, V(0, 0))
            if action is Action.SELECT:
                cursor = self.bcursor
                focus = board[cursor]
                if (
                    not attacker
                    and focus
                    and focus.player is board.active_player
                    and board.targets[cursor]
                ):
                    self.attacker = Square(focus, cursor)

                elif attacker and cursor in board.targets[attacker.coord]:
                    if (
                        attacker.piece.role is Role.PAWN
                        and attacker.coord.y in [1, 6]
                        and attacker.piece.moved
                    ):
                        self.status = Status.PROMOTING
                    else:
                        board.process_move(attacker.coord, self.bcursor)
                        self.attacker = None


CARDINAL_DIRECTION: dict[Action, Vector] = {
    Action.UP: V(0, -1),
    Action.DOWN: V(0, +1),
    Action.LEFT: V(-1, 0),
    Action.RIGHT: V(+1, 0),
}

ROTATE = {
    Action.UP: Action.LEFT,
    Action.DOWN: Action.RIGHT,
    Action.RIGHT: Action.UP,
    Action.LEFT: Action.DOWN,
}

PROMOTION_OPTIONS = (Role.QUEEN, Role.KNIGHT, Role.ROOK, Role.BISHOP)
