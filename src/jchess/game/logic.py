"""Implements rules/logic associate with each piece.

We use 3 different methods:
* Queen, Bishop, Rook: check along each line of movement; terminate when a blocker met
* King, Knight: check each viable translation vector
* Pawn: specialized function.
"""

from itertools import product
from typing import TYPE_CHECKING

from jchess.game.engine import CARDINAL_DIRECTION, EMPTY_SQUARE
from jchess.geometry import Vector
from jchess.squares import Role, Player

if TYPE_CHECKING:
    from jchess.game.state import GameState


def defending_coords_(game: "GameState", attacker_coord: Vector) -> list[Vector]:
    """Implement `GameState.defending_coords`."""
    attacker = game[attacker_coord]

    # the pawn has unique behavior warranting it's own function
    if attacker.role is Role.PAWN:
        return _def_coords_pawn(game, attacker_coord, attacker.player)

    result = []

    # the queen, bishop & rook always move along lines
    for line in LINES.get(attacker.role, []):
        for delta in line:
            defender_coord = attacker_coord + delta
            if game.has(defender_coord):
                defender = game[defender_coord]
                if defender.player is game.inactive_player():
                    result.append(defender_coord)
                    break
                if defender.player is game.active_player():
                    break
                result.append(defender_coord)

    # the king and knight always have fixed potential translations
    for delta in DELTAS.get(attacker.role, []):
        defender_coord = attacker_coord + delta
        if (
            game.has(defender_coord)
            and game[defender_coord].player != game.active_player()
        ):
            result.append(defender_coord)

    return result


def _def_coords_pawn(game: "GameState", coord: Vector, player: Player) -> list[Vector]:
    """Implement `GameState.defending_coords` for pawns."""
    result = []

    if player is Player.TWO:
        direction = 1
        start_row = 1
    else:  # player is ONE
        direction = -1
        start_row = 6

    defender_coord = coord + (0, direction)
    if game.has(defender_coord) and game[defender_coord] is EMPTY_SQUARE:
        result.append(defender_coord)

    for dx in [1, -1]:
        defender_coord = coord + (dx, direction)
        # TODO: look into reducing this code pattern
        if (
            game.has(defender_coord)
            and game[defender_coord].player is game.inactive_player()
        ):
            result.append(defender_coord)

    defender_coord = coord + (0, 2 * direction)
    if coord.y == start_row:
        result.append(defender_coord)

    return result


DELTAS = {
    Role.KING: list(product([-1, 0, +1], [-1, 0, +1])),
    Role.KNIGHT: list(product((-1, 1), (-2, 2))) + list(product((-1, 1), (-2, 2))),
}


L1 = [[(s * d, t * d) for d in range(1, 8)] for s, t in CARDINAL_DIRECTION.values()]
L2 = [[(s * d, t * d) for d in range(1, 8)] for s, t in product([1, -1], repeat=2)]
LINES = {
    Role.QUEEN: L1 + L2,
    Role.ROOK: L1,
    Role.BISHOP: L2,
}
