"""Interface layer between the player and chess game.

`Mode` is set by the user early in `Game`'s lifecycle and doesn't change. `Status` is
internally controlled by `Game`. Both aid `Game`'s logic flow.
"""
import random
import sys
from collections.abc import Iterator
from enum import Enum, auto
from time import sleep
from typing import Any

from jchess.action import Action, get_action_lhs, get_action_rhs
from jchess.board import Board
from jchess.geometry import V, Vector
from jchess.pieces import LocPiece, Player, Role

SELECT, UP, DOWN, RIGHT, LEFT, IGNORE, QUIT = list(Action)
AXIS_LOOKUP = {UP: V(0, -1), DOWN: V(0, +1), LEFT: V(-1, 0), RIGHT: V(+1, 0)}
ROTATE = {UP: LEFT, DOWN: RIGHT, RIGHT: UP, LEFT: DOWN}
PROMOTION_OPTIONS = (Role.QUEEN, Role.KNIGHT, Role.ROOK, Role.BISHOP)
MAX_PLY_COUNT = 100


class Mode(Enum):
    """Determines game-play type - user set."""

    VDB = "Versus Dumb Bot"
    LTP = "Local Two-Player"
    TDB = "Two Dumb Bots"
    # RMP = "Remote Multi-Player"
    # VAI = "Versus AI"


class Status(Enum):
    """Helper enum for tracking `Game`'s internal state."""

    UNINITIALIZED = auto()
    START_MENU = auto()
    PROMOTING = auto()
    BOARD_FOCUS = auto()
    GAME_OVER = auto()


class Game:
    """Interface layer between the player and chess game."""

    def __init__(self) -> None:
        """Initialise a `GameState`."""
        self.board = Board()

        self.attacker: LocPiece | None = None

        # Cursors for different `State` (START_MENU, BOARD_FOCUS & PROMOTING resp.)
        self.scursor = 0
        self.bcursor = V(4, 7)
        self.pcursor = 0

        self.status_prev = Status.UNINITIALIZED
        self.status = Status.START_MENU

        self.mode: Mode | None = None
        self.bot_action = self.__action_generator()

    def __setattr__(self, name: str, value: Any) -> None:
        # ensures user can 'cycle' through options
        if name == "bcursor":
            value %= 8
        elif name == "pcursor":
            value %= len(PROMOTION_OPTIONS)
        elif name == "scursor":
            value %= len(Mode)
        super().__setattr__(name, value)

    def evolve_state(self) -> None:
        """Get next action and update the game accordingly."""

        if self.status is Status.GAME_OVER:
            input()
            sys.exit()

        action = self.get_action()
        board = self.board
        status = self.status_prev = self.status
        attacker = self.attacker

        if action is QUIT and self.mode is not None:
            self.status = Status.GAME_OVER

        elif status is Status.START_MENU:
            self.scursor += AXIS_LOOKUP.get(action, V(0, 0)).y
            if action is SELECT:
                self.mode = list(Mode)[self.scursor]
                self.status = Status.BOARD_FOCUS

        elif status is Status.PROMOTING:
            assert attacker, "Can only promote if an attacker is selected"
            self.pcursor += AXIS_LOOKUP.get(action, V(0, 0)).y
            if action is Action.SELECT:
                board.process_move(
                    attacker.coord,
                    self.bcursor,
                    promote_to=PROMOTION_OPTIONS[self.pcursor],
                )
                self.attacker = None
                self.status = Status.BOARD_FOCUS

        elif status is Status.BOARD_FOCUS:
            self.bcursor += AXIS_LOOKUP.get(action, V(0, 0))
            if action is SELECT:
                cursor = self.bcursor
                if not attacker and board.can_move_from(cursor):
                    self.attacker = LocPiece(board[cursor], cursor)  # type: ignore

                elif attacker and cursor in board.targets_of[attacker.coord]:
                    if (
                        attacker.piece.role is Role.PAWN
                        and attacker.coord.y in [1, 6]
                        and attacker.piece.moved
                    ):
                        self.status = Status.PROMOTING
                    else:
                        board.process_move(attacker.coord, self.bcursor)
                        self.attacker = None

        if board.ply >= MAX_PLY_COUNT or not board.can_move():
            self.status = Status.GAME_OVER

    def get_action(self) -> Action:
        """Get next action from user or bot."""

        player = self.board.active_player
        if self.mode is Mode.TDB:
            return next(self.bot_action)
        if self.mode is Mode.VDB:
            return get_action_rhs() if player is Player.ONE else next(self.bot_action)
        # else mode is LTP
        return get_action_rhs() if player is Player.ONE else get_action_lhs()

    def __action_generator(self) -> Iterator[Action]:
        """Generate a sequence of `Action`s forming a valid (but random) chess move."""
        board = self.board
        while True:

            attacker_coord = random.choice([v for v in board if board.can_move_from(v)])
            yield from self.__path_to(attacker_coord)

            assert self.attacker, "Attacker should have been set by previous moves."
            target = random.choice(list(board.targets_of[self.attacker.coord]))
            yield from self.__path_to(target)

            if self.status is Status.PROMOTING:
                for _ in range(random.randint(0, 3)):
                    yield Action.DOWN
                yield Action.SELECT

    def __path_to(self, destination: Vector) -> Iterator[Action]:
        """Generate sequence of `Action`s to move `bcursor` to `destination`."""
        dx, dy = destination - self.bcursor
        secs = 0.2
        for _ in range(abs(dy)):
            sleep(secs)
            yield Action.UP if dy < 0 else Action.DOWN
        for _ in range(abs(dx)):
            sleep(secs)
            yield Action.RIGHT if dx > 0 else Action.LEFT
        sleep(secs)
        yield Action.SELECT
