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
from jchess.geometry import Vector

from jchess.pieces import Piece, Role

if TYPE_CHECKING:
    from jchess.game.state import GameState
    from jchess.board import Board


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
            and cursor_piece.player is board.active_player()
            and cursor_piece.targets != []
        ):
            game.attacking_piece = cursor_piece
        elif attacker is not None and game.cursor_coord in attacker.targets:
            process_attack(game.board, attacker, game.cursor_coord)
            game.attacking_piece = None

    elif action is Action.QUIT:
        sys.exit()


def process_attack(board: "Board", attacker: Piece, defender_coord: Vector) -> None:

    defender = board[defender_coord]
    delta = defender_coord - attacker.coord

    # remove any previous vulnerability to en passant
    if (
        board.passant_vulnerable_piece is not None
        and board.passant_vulnerable_piece.player is board.active_player()
    ):
        board.passant_vulnerable_piece = None

    # add any new vulnerability to en passant
    if attacker.role is Role.PAWN and delta in [(0, 2), (0, -2)]:
        board.passant_vulnerable_piece = attacker

    # en passant move chosen, so delete piece to the left/right
    if (
        attacker.role is Role.PAWN
        and delta in [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        and defender is None
        # not really required: pleases type checker
        and board.passant_vulnerable_piece is not None
    ):
        board.pieces.remove(board.passant_vulnerable_piece)
        board.taken_pieces[board.active_player()].append(Role.PAWN)

    # castling
    if attacker.role is Role.KING:
        y_king = attacker.coord.y

        # king-side castle
        if delta.x == 2:
            castle = board[7, y_king]
            if castle is None:
                raise RuntimeError("King-side castling shouldn't have been available.")
            castle.coord = (5, y_king)

        # queen-side caste
        if delta.x == -2:
            castle = board[0, y_king]
            if castle is None:
                raise RuntimeError("Queen-side castling shouldn't have been available.")
            castle.coord = (3, y_king)

    # execute move
    attacker.coord = defender_coord
    if defender is not None:
        board.pieces.remove(defender)
        board.taken_pieces[board.active_player()].append(defender.role)
    board.turn += 1
    board.update_targets()


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
