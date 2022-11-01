import csv
import functools
import re
from itertools import product
from pathlib import Path
from typing import Any, Callable
from unittest import TestCase
from unittest.mock import Mock, patch

from jchess.action import Action
from jchess.board import Board
from jchess.geometry import V, Vectors
from jchess.pieces import Piece, Player, Role
from jchess.state import GameState

# TODO: move to pytest

ACTION_LOOKUP = {action.value: action for action in Action}
ROLE_LOOKUP = {role.symbol: role for role in Role}
PLAYER_LOOKUP = {str(player.value): player for player in Player}

SYMBOLS = "".join(role.symbol for role in Role)
CELL_PATTERN = rf"""
^
    (?:
        ([{SYMBOLS}])([-x])([12])  # Match [SYMBOL][FLAG][PLAYER_NUMBER] ...
    )
    |
    -([-x])-                       # ... or [-][FLAG][-]
$
"""
CELL_REGEX = re.compile(CELL_PATTERN, re.X)


# not worth getting more specific
Func = Callable[..., Any]


def patch_inputs(cmdstr: str) -> Func:
    actions = [ACTION_LOOKUP[c] for c in cmdstr.split()]

    def decorator(func: Func) -> Func:
        @functools.wraps(func)
        @patch("jchess.state.GameState.get_action")
        def wrapper(self: TestCase, mock_get_action: Mock) -> Any:
            mock_get_action.side_effect = actions
            game = GameState()
            for _ in actions:
                game.evolve_state()
            return func(self, game)

        return wrapper

    return decorator


def board_from_ssv(path: Path) -> tuple[Board, Vectors]:
    """Construct a `Board` from a ".ssv" file."""

    # initializes with pieces in default position, but these are all overridden
    board = Board()
    targets = []

    with open(path, encoding="utf-8") as csvfh:
        for y, row in enumerate(csv.reader(csvfh, delimiter=" ")):
            for x, cell in enumerate(row):
                coord = V(x, y)

                match = CELL_REGEX.match(cell)
                if not match:
                    raise RuntimeError(f"{cell=} at {coord} :\n{CELL_REGEX.pattern}")
                sym, flag1, num, flag2 = match.groups()

                if not sym and not flag1 and not num and flag2:
                    board[coord] = None
                elif sym and flag1 and num and not flag2:
                    board[coord] = Piece(ROLE_LOOKUP[sym], PLAYER_LOOKUP[num], coord)
                else:
                    assert False, f"Bad vals: {sym=}, {flag1=}, {num=}, {flag2=}"

                if "x" in [flag1, flag2]:
                    targets.append(coord)

    board.update_targets()
    return board, targets


def board_to_ssv(board: Board, targets: Vectors) -> str:
    parts = []
    for y, x in product(range(8), range(8)):
        key = V(x, y)
        flag = "x" if key in targets else "-"
        if piece := board[key]:
            parts.append(f"{piece.role.symbol}{flag}{piece.player.value}")
        else:
            parts.append(f"-{flag}-")
        parts.append(" " if x != 7 else "\n")
    return "".join(parts)
