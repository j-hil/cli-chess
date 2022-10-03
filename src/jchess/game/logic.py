"""Implements rules/logic associate with each piece.

We use 2 different general methods:
* Queen, Bishop, Rook: check along each line of movement; terminate when a blocker met
* King, Knight: check each viable translation vector
And then pawns and castling require specialized logic.
"""

from copy import deepcopy
from itertools import product
from typing import TYPE_CHECKING

from jchess.game.engine import CARDINAL_DIRECTION, Action
from jchess.geometry import Vector
from jchess.pieces import Piece, Role, Player

if TYPE_CHECKING:
    from jchess.game.state import GameState


def targets_of_(game: "GameState", attacker: Piece) -> list[Vector]:

    if attacker not in game.pieces:
        raise RuntimeError(f"{attacker} not in play.")

    result: list[Vector] = []

    # the pawn has unique behavior warranting it's own function
    if attacker.role is Role.PAWN:
        _targeted_by_pawn(game, attacker, result)

    # the queen, bishop & rook always move along lines
    for line in LINES.get(attacker.role, []):
        for delta in line:
            defender_coord = attacker.coord + delta
            if game.has(defender_coord):
                defender = game[defender_coord]
                if defender is None:
                    result.append(defender_coord)
                    continue
                if defender.player is not game.active_player():
                    result.append(defender_coord)
                break

    # the king and knight always have fixed potential translations
    for delta in DELTAS.get(attacker.role, []):
        defender_coord = attacker.coord + delta
        if game.has(defender_coord):
            defender = game[defender_coord]
            if defender is None or defender.player != game.active_player():
                result.append(defender_coord)

    # extra logic for castling
    if attacker.role is Role.KING and attacker.has_not_moved():
        _castling_logic(game, attacker, result)

    # TODO: revise just like all of this branch... its so slow! may require large rework
    if not hasattr(game, "flag"):
        _handle_check(game, attacker, result)

    return result


def _handle_check(game: "GameState", attacker: Piece, result: list[Vector]):
    for defender_coord in result.copy():
        game_copy = deepcopy(game)
        game_copy.flag = "monkey_patch"  # type: ignore

        # initiate the attack
        game_copy.attacking_piece = game_copy[attacker.coord]
        game_copy.cursor_coord = defender_coord
        game_copy.evolve_state(Action.SELECT)

        for piece in game_copy.pieces:
            if piece.player is not attacker.player:
                for coord in targets_of_(game_copy, piece):
                    defender = game_copy[coord]
                    if defender is not None and defender.role is Role.KING:
                        result.remove(defender_coord)


def _castling_logic(game: "GameState", attacker: Piece, result: list[Vector]):
    y_king = attacker.coord.y

    # extra logic for king-side castling
    rook = game[(7, y_king)]
    if (
        # unmoved rook
        (rook is not None and rook.role is Role.ROOK and rook.has_not_moved())
        # empty path
        and all(game[(x, y_king)] is None for x in [5, 6])
        # safe path
        and all(
            (x, y_king) not in game.targets_of(p)
            for p, x in product(game.pieces, [4, 5, 6])
            if p.player is not attacker.player
        )
    ):
        result.append(attacker.coord + (2, 0))

    # extra logic for queen-side castling
    rook = game[(0, y_king)]
    if (
        # unmoved rook
        (rook is not None and rook.role is Role.ROOK and rook.has_not_moved())
        # empty path
        and all(game[(x, y_king)] is None for x in [1, 2, 3])
        # safe path
        and all(
            (x, y_king) not in game.targets_of(p)
            for p, x in product(game.pieces, [1, 2, 3, 4])
            if p.player is not attacker.player
        )
    ):
        result.append(attacker.coord - (2, 0))


def _targeted_by_pawn(game: "GameState", attacker: Piece, result: list[Vector]):
    """Implement `GameState.defending_coords` for pawns."""

    if attacker.player is Player.TWO:
        direction = 1
    else:  # player is ONE
        direction = -1

    defender_coord = attacker.coord + (0, direction)
    if game.has(defender_coord) and game[defender_coord] is None:
        result.append(defender_coord)

    for dx in [1, -1]:
        defender_coord = attacker.coord + (dx, direction)
        defender = game[defender_coord]
        en_passant_vulnerable_piece = game[attacker.coord + (dx, 0)]
        if (
            # standard pawn capture
            game.has(defender_coord)
            and defender is not None
            and defender.player is not game.active_player()
            # en passant capture
            or en_passant_vulnerable_piece is not None
            and en_passant_vulnerable_piece == game.passant_vulnerable_piece
        ):
            result.append(defender_coord)

    defender_coord = attacker.coord + (0, 2 * direction)
    if attacker.has_not_moved() and game[defender_coord - (0, direction)] is None:
        result.append(defender_coord)


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
