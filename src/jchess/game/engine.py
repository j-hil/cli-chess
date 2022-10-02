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

from jchess.pieces import Piece, Role

if TYPE_CHECKING:
    from jchess.game.state import GameState


def evolve_state_(game: "GameState") -> None:
    """Implement `GameState.evolve_state`."""
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
            and game.targets_of(cursor_piece) != []
        ):
            game.attacking_piece = cursor_piece
        elif attacker is not None and game.cursor_coord in game.targets_of(attacker):
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
    game.turn += 1
    game.attacking_piece = None

    # piece is taken
    if defender is not None:
        game.pieces.remove(defender)
        game.taken_pieces[game.active_player()].append(defender.role)


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
