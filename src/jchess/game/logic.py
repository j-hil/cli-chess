"""Implements rules/logic associate with each piece.

We use 2 different general methods:
* Queen, Bishop, Rook: check along each line of movement; terminate when a blocker met
* King, Knight: check each viable translation vector
And then pawns and castling require specialized logic.
"""

from copy import deepcopy
from itertools import product
from typing import TYPE_CHECKING

from jchess.geometry import Vector
from jchess.pieces import Piece, Role
from jchess.game.engine import CARDINAL_DIRECTION, Action, process_attack

if TYPE_CHECKING:
    from jchess.board import Board


def update_targets_(game: "Board"):
    for attacker in game.pieces:
        targets: list[Vector] = []

        # the pawn has unique behavior warranting it's own function
        if attacker.role is Role.PAWN:
            targets.extend(pawn_targets(game, attacker))

        # the queen, bishop & rook always move along lines
        for line in LINES.get(attacker.role, []):
            for delta in line:
                defender_coord = attacker.coord + delta
                if game.has(defender_coord):
                    defender = game[defender_coord]
                    if defender is None:
                        targets.append(defender_coord)
                        continue
                    if defender.player is not attacker.player:
                        targets.append(defender_coord)
                    break

        # the king and knight always have fixed potential translations
        for delta in DELTAS.get(attacker.role, []):
            defender_coord = attacker.coord + delta
            if game.has(defender_coord):
                defender = game[defender_coord]
                if defender is None or defender.player != attacker.player:
                    targets.append(defender_coord)

        # extra logic for castling
        if attacker.role is Role.KING and attacker.has_not_moved():
            targets.extend(castling_targets(game, attacker))

        # extra logic for check
        if game.protect_king:
            bad_targets = risky_targets(game, attacker, targets)
            targets = [t for t in targets if t not in bad_targets]

        attacker.targets = targets


def risky_targets(
    board: "Board", attacker: Piece, current_targets: list[Vector]
) -> list[Vector]:

    result = []

    for defender_coord in current_targets:
        board_copy = deepcopy(board)
        attacker_copy = deepcopy(attacker)

        # initiate the attack
        board_copy.protect_king = False
        board_copy.update_targets()
        process_attack(board_copy, attacker_copy, defender_coord)

        for piece in board_copy.pieces:
            if piece.player is not attacker_copy.player:
                for coord in piece.targets:
                    target = board_copy[coord]
                    if target is not None and target.role is Role.KING:
                        result.append(defender_coord)
    return result


def castling_targets(board: "Board", attacker: Piece) -> list[Vector]:
    result = []

    y_king = attacker.coord.y

    # extra logic for king-side castling
    rook = board[(7, y_king)]
    if (
        # unmoved rook
        (rook is not None and rook.role is Role.ROOK and rook.has_not_moved())
        # empty path
        and all(board[(x, y_king)] is None for x in [5, 6])
        # safe path
        and all(
            (x, y_king) not in p.targets
            for p, x in product(board.pieces, [4, 5, 6])
            if p.player is not attacker.player
        )
    ):
        result.append(attacker.coord + (2, 0))

    # extra logic for queen-side castling
    rook = board[(0, y_king)]
    if (
        # unmoved rook
        (rook is not None and rook.role is Role.ROOK and rook.has_not_moved())
        # empty path
        and all(board[(x, y_king)] is None for x in [1, 2, 3])
        # safe path
        and all(
            (x, y_king) not in p.targets
            for p, x in product(board.pieces, [1, 2, 3, 4])
            if p.player is not attacker.player
        )
    ):
        result.append(attacker.coord - (2, 0))
    return result


def pawn_targets(board: "Board", attacker: Piece) -> list[Vector]:
    result = []

    # map 1 to -1 and 2 to +1; i.e up or down depending on player.
    direction = 2 * attacker.player.value - 3

    defender_coord = attacker.coord + (0, direction)
    if board.has(defender_coord) and board[defender_coord] is None:
        result.append(defender_coord)

    for dx in [1, -1]:
        defender_coord = attacker.coord + (dx, direction)
        defender = board[defender_coord]
        en_passant_vulnerable_piece = board[attacker.coord + (dx, 0)]
        if (
            # standard pawn capture
            board.has(defender_coord)
            and defender is not None
            and defender.player is not attacker.player
            # en passant capture
            or en_passant_vulnerable_piece is not None
            and en_passant_vulnerable_piece == board.passant_vulnerable_piece
        ):
            result.append(defender_coord)

    defender_coord = attacker.coord + (0, 2 * direction)
    if (
        attacker.has_not_moved()
        and board[defender_coord - (0, direction)] is None
        and board[defender_coord] is None
    ):
        result.append(defender_coord)

    return result


DELTAS = {
    Role.KING: list(product([-1, 0, +1], [-1, 0, +1])),
    Role.KNIGHT: list(product((-1, 1), (-2, 2))) + list(product((-2, 2), (-1, 1))),
}


L1 = [[(s * d, t * d) for d in range(1, 8)] for s, t in CARDINAL_DIRECTION.values()]
L2 = [[(s * d, t * d) for d in range(1, 8)] for s, t in product([1, -1], repeat=2)]
LINES = {
    Role.QUEEN: L1 + L2,
    Role.ROOK: L1,
    Role.BISHOP: L2,
}
