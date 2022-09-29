"""Implementation of `GameState.evolve_state`.

Controls reaction to and collection player input. Recognized actions are
* quitting - exit the entire game
* select - pick the highlighted square to move to/from
* up, down, left, right - move the cursor around the board
"""

from enum import Enum, auto
import sys
from typing import TYPE_CHECKING
from msvcrt import getch
from jchess.geometry import Vector

from jchess.squares import Square, Role, Player

if TYPE_CHECKING:
    from jchess.game.state import GameState

# Sentinel: A square on the board, but with no piece on it
EMPTY_SQUARE = Square(Role.NULL, Player.NULL)

# Sentinel: A square not on the board
UNSELECTED_SQUARE = Square(Role.NULL, Player.NULL)
UNSELECTED_COORD = Vector(-999, -999)  # in theory any |x|, |y| >= 8 will do


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


def evolve_state_(game: "GameState") -> None:
    """Implement `GameState.evolve_state`."""
    action = _get_action_from_user()
    _process_action(game, action)


def _get_action_from_user() -> Action:

    # 2nd char necessary: directions are as '\x00{c}' or '\xe0{c}' for some capital `c`
    user_input = getch().upper()
    if user_input in [b"\x00", b"\xe0"]:
        user_input += getch().upper()

    for action in Action:
        if user_input in ACTION_INPUTS.get(action, []):
            return action
    return Action.IGNORE


def _process_action(game: "GameState", action: Action) -> None:

    if game.mode is Mode.TWO:
        # account for fact that user's view is rotated from the internal view
        action = ROTATE.get(action, action)

    new_cursor_coord = game.cursor_coord + CARDINAL_DIRECTION.get(action, (0, 0))
    if game.has(new_cursor_coord):
        game.cursor_coord = new_cursor_coord

    if (
        action is Action.SELECT
        and game.selected_coord is UNSELECTED_COORD
        and game.cursor.player is game.active_player()
        and game.defending_coords(game.cursor_coord)
    ):
        game.selected_coord = game.cursor_coord
    elif (
        action is Action.SELECT
        and game.selected_coord is not UNSELECTED_COORD
        and game.cursor_coord in game.defending_coords(game.selected_coord)
    ):
        # piece is taken - add it to taken pieces list
        if game.cursor is not EMPTY_SQUARE:
            game.taken_pieces[game.active_player()].append(game.cursor.role)

        # remove any previous vulnerabilities to en passant
        if game.en_passant_victim_coord is not UNSELECTED_COORD and game.active_player() is game[game.en_passant_victim_coord].player:
            game.en_passant_victim_coord = UNSELECTED_COORD

        # add a vulnerability to en passant (if appropriate)
        if game.selected.role is Role.PAWN and (game.selected_coord - game.cursor_coord) in [Vector(0, 2), Vector(0, -2)]:
            game.en_passant_victim_coord = (game.cursor_coord)

        # en passant move chosen, so delete piece to the left/ right or whatever
        delta = game.cursor_coord - game.selected_coord
        if game.selected.role is Role.PAWN and delta in [Vector(1, 1), Vector(1, -1), Vector(-1, 1), Vector(-1, -1)] and game.cursor is EMPTY_SQUARE:
            game[game.selected_coord + (delta.x, 0)] = EMPTY_SQUARE
            game.taken_pieces[game.active_player()].append(Role.PAWN)

        # execute move
        game.cursor = game.selected
        game.selected = EMPTY_SQUARE
        game.turn += 1
        game.selected_coord = UNSELECTED_COORD

    elif action is Action.QUIT:
        sys.exit()


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
