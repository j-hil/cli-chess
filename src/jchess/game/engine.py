"""Implementation of `GameState.evolve_state`.

Controls reaction of `GameState` to player input.
"""

from copy import deepcopy
from enum import Enum, auto
import sys
from typing import TYPE_CHECKING
from msvcrt import getch

from jchess.squares import NULL_SQUARE, Player

if TYPE_CHECKING:
    from jchess.game.state import GameState


class Mode(Enum):
    ONE = "single player"
    TWO = "online multi-player"
    THREE = "local multi-player"


class Action(Enum):
    """Player actions recognized by the game."""

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

    new_cursor_coord = game.highlighted_coord + CARDINAL_DIRECTION.get(action, (0, 0))
    if new_cursor_coord.x in range(8) and new_cursor_coord.y in range(8):
        game.highlighted_coord = new_cursor_coord

    can_use_highlighted = (
        game.selected is None
        and game.highlighted.player is game.player
        and len(game.defending_coords(game.highlighted_coord)) > 0
    )

    if action is Action.SELECT and can_use_highlighted:
        game.selected_coord = deepcopy(game.highlighted_coord)
    elif action is Action.SELECT and game.is_defending(game.highlighted_coord, against=game.selected_coord):
        # TODO: somehow 2nd instance of Square(NULL, NULL) is created so != not `is not`
        if game.highlighted != NULL_SQUARE:
            game.taken_pieces[game.player].append(game.highlighted.role)

        # TODO: mypy issue
        # can't tell here that is_defending(game.highlighted_coord) => game.selected
        # possibly solve by overloading __getitem__
        game.highlighted = game.selected  # type: ignore
        game.selected = NULL_SQUARE
        if game.player is Player.ONE:
            game.player = Player.TWO
        else:
            game.player = Player.ONE
        game.selected_coord = None
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
