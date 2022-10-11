"""Implementation of `GameState.evolve_state`.

Controls reaction to and collection player input. Recognized actions are
* quitting - exit the entire game
* select - pick the highlighted square to move to/from
* up, down, left, right - move the cursor around the board
"""

from enum import Enum, auto
import sys
from typing import TYPE_CHECKING, Union
from msvcrt import getch

if TYPE_CHECKING:
    from jchess.game.state import GameState


def evolve_state_(game: "GameState", action: Union["Action", None] = None) -> None:
    """Implement `GameState.evolve_state`."""
    if action is None:
        action = _get_action_from_user()
    _process_action(game, action)


def _get_action_from_user() -> "Action":

    # 2nd char necessary: directions are as '\x00{c}' or '\xe0{c}' for some capital `c`
    user_input = getch().upper()
    if user_input in [b"\x00", b"\xe0"]:
        user_input += getch().upper()

    for action in Action:
        if user_input in ACTION_INPUTS.get(action, []):
            return action
    return Action.IGNORE


def _process_action(game: "GameState", action: "Action") -> None:
    board = game.board

    if action in CARDINAL_DIRECTION:
        if game.mode is Mode.TWO:
            # account for fact that user's view is rotated from the internal view
            action = ROTATE.get(action, action)

        new_cursor_coord = game.cursor_coord + CARDINAL_DIRECTION[action]
        if board.has(new_cursor_coord):
            game.cursor_coord = new_cursor_coord

    elif action is Action.SELECT:
        attacker = game.attacking_piece
        cursor_piece = board[game.cursor_coord]
        if (
            attacker is None
            and cursor_piece is not None
            and cursor_piece.player is board.active_player
            and cursor_piece.targets != []
        ):
            game.attacking_piece = cursor_piece
        elif attacker is not None and game.cursor_coord in attacker.targets:
            board.process_attack(attacker, game.cursor_coord)
            game.attacking_piece = None

    elif action is Action.QUIT:
        sys.exit()


class Mode(Enum):
    ONE = "single player"
    TWO = "online multi-player"
    THREE = "local multi-player"


class Action(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    SELECT = auto()
    QUIT = auto()
    IGNORE = auto()


CARDINAL_DIRECTION = {
    Action.UP: (0, -1),
    Action.DOWN: (0, +1),
    Action.LEFT: (-1, 0),
    Action.RIGHT: (+1, 0),
}

ACTION_INPUTS = {
    Action.QUIT: [b"\x1b", b"Q"],
    Action.SELECT: [b" ", b"\r"],
    Action.UP: [b"W", b"\x00H", b"\xe0H"],
    Action.DOWN: [b"S", b"\x00P", b"\xe0P"],
    Action.LEFT: [b"A", b"\x00K", b"\xe0K"],
    Action.RIGHT: [b"D", b"\x00M", b"\xe0M"],
}

ROTATE = {
    Action.UP: Action.LEFT,
    Action.DOWN: Action.RIGHT,
    Action.RIGHT: Action.UP,
    Action.LEFT: Action.DOWN,
}
