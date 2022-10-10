"""Implementation of `GameState.evolve_state`.

Controls reaction to and collection player input. Recognized actions are
* quitting - exit the entire game
* select - pick the highlighted square to move to/from
* up, down, left, right - move the cursor around the board
"""

from enum import Enum, auto
import sys
from typing import TYPE_CHECKING, Union

from jchess.pieces import Piece, Role
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

    if action in CARDINAL_DIRECTION:
        if game.mode is Mode.TWO:
            # account for fact that user's view is rotated from the internal view
            action = ROTATE.get(action, action)

        new_cursor_coord = game.cursor_coord + CARDINAL_DIRECTION[action]
        if game.has(new_cursor_coord):
            game.cursor_coord = new_cursor_coord

    elif action is Action.SELECT:
        attacker = game.attacking_piece
        cursor_piece = game[game.cursor_coord]
        if (
            attacker is None
            and cursor_piece is not None
            and cursor_piece.player is game.active_player()
            and cursor_piece.targets != []
        ):
            game.attacking_piece = cursor_piece
        elif attacker is not None and game.cursor_coord in attacker.targets:
            _process_attack(game, attacker)

    elif action is Action.QUIT:
        sys.exit()


def _process_attack(game: "GameState", attacker: Piece) -> None:
    defender = game[game.cursor_coord]
    delta = game.cursor_coord - attacker.coord

    # remove any previous vulnerability to en passant
    if (
        game.passant_vulnerable_piece is not None
        and game.passant_vulnerable_piece.player is game.active_player()
    ):
        game.passant_vulnerable_piece = None

    # add any new vulnerability to en passant
    if attacker.role is Role.PAWN and delta in [(0, 2), (0, -2)]:
        game.passant_vulnerable_piece = attacker

    # en passant move chosen, so delete piece to the left/right
    if (
        attacker.role is Role.PAWN
        and delta in [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        and defender is None
        # not really required: pleases type checker
        and game.passant_vulnerable_piece is not None
    ):
        game.pieces.remove(game.passant_vulnerable_piece)
        game.taken_pieces[game.active_player()].append(Role.PAWN)

    # castling
    if attacker.role is Role.KING:
        y_king = attacker.coord.y

        # king-side castle
        if delta.x == 2:
            castle = game[7, y_king]
            if castle is None:
                raise RuntimeError("King-side castling shouldn't have been available.")
            castle.coord = (5, y_king)

        # queen-side caste
        if delta.x == -2:
            castle = game[0, y_king]
            if castle is None:
                raise RuntimeError("Queen-side castling shouldn't have been available.")
            castle.coord = (3, y_king)

    # execute move
    attacker.coord = game.cursor_coord
    game.attacking_piece = None
    if defender is not None:
        game.pieces.remove(defender)
        game.taken_pieces[game.active_player()].append(defender.role)
    game.turn += 1

    game.update_targets()


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
