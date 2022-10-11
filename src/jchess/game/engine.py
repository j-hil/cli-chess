"""Implementation of `GameState.evolve_state`.

Controls reaction to and collection player input. Recognized actions are
* quitting - exit the entire game
* select - pick the highlighted square to move to/from
* up, down, left, right - move the cursor around the board
"""

from enum import Enum, auto
import sys
from typing import TYPE_CHECKING, Union

from jchess.terminal import get_char

if TYPE_CHECKING:
    from jchess.game.state import GameState


def evolve_state_(game: "GameState", action: Union["Action", None] = None) -> None:
    """Implement `GameState.evolve_state`."""
    if action is None:
        action = _get_action_from_user()
    _process_action(game, action)


def _get_action_from_user() -> "Action":

    user_input = get_char().upper()

    # for windows terminal and vscode inputs
    if user_input in ["\x00", "\xe0"]:
        user_input += get_char().upper()

    # for linux vscode inputs
    if user_input == "\x1b":
        user_input += get_char().upper()
        user_input += get_char().upper()

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
    Action.QUIT: ["\x1b", "Q"],
    Action.SELECT: [" ", "\r"],
    Action.UP: ["W", "\x00H", "\xe0H", "\x1b[A"],
    Action.DOWN: ["S", "\x00P", "\xe0P", "\x1b[B"],
    Action.LEFT: ["A", "\x00K", "\xe0K", "\x1b[D"],
    Action.RIGHT: ["D", "\x00M", "\xe0M", "\x1b[C"],
}

ROTATE = {
    Action.UP: Action.LEFT,
    Action.DOWN: Action.RIGHT,
    Action.RIGHT: Action.UP,
    Action.LEFT: Action.DOWN,
}
