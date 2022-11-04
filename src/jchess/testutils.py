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

assert "".join(role.symbol for role in Role) == "KQHIJi ", "Update symbols in regex."
CELL_PATTERN = r"""
^
    (?:
        ([KQHIJi])([12])([-x])m([TF])   # Match [SYMBOL][PLAYER_NUM][FLAG]m[MOVED] ...
    )
    |
    --([-x])--                          # ... or --[FLAG]--
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
                    msg = f"{cell=} at {coord} doesn't match:\n{CELL_REGEX.pattern}"
                    raise RuntimeError(msg)
                sym, num, target_flag1, moved, target_flag2 = match.groups()

                # check the regex is working
                if __debug__:
                    *a, b = match.groups()
                    msg = f"Bad vals: {sym=}, {target_flag1=}, {num=}, {target_flag2=}"
                    assert (all(a) and not b) or (not any(a) and b), msg

                board[coord] = (
                    Piece(ROLE_LOOKUP[sym], PLAYER_LOOKUP[num], moved == "T")
                    if target_flag1
                    else None
                )

                if "x" in [target_flag1, target_flag2]:
                    targets.append(coord)

    board.update_targets()
    return board, targets


def board_to_ssv(board: Board, targets: Vectors) -> str:
    parts = []
    for y, x in product(range(8), range(8)):
        coord = V(x, y)
        flag = "x" if coord in targets else "-"
        if piece := board[coord]:
            sym = piece.role.symbol
            num = piece.player.value
            moved = "T" if piece.moved else "F"
            parts.append(f"{sym}{num}{flag}m{moved}")
        else:
            parts.append(f"--{flag}--")
        parts.append(" " if coord.x != 7 else "\n")
    return "".join(parts)
