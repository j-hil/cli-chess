"""Implements rules associate with each piece."""

from itertools import product
from typing import TYPE_CHECKING
from jchess.engine import CARDINAL_DIRECTION

from jchess.geometry import Vector
from jchess.squares import Role, Player

if TYPE_CHECKING:
    from jchess.state import GameState


def defending_coords_(game: "GameState", attacker_coord: Vector | None) -> list[Vector]:
    """Implement `GameState.defending_coords`."""
    attacker = game[attacker_coord]
    if attacker is None or attacker_coord is None:
        return []

    # the pawn has unique behavior warranting it's own function
    if attacker.role is Role.PAWN:
        return _def_coords_pawn(game, attacker_coord, attacker.player)

    result = []

    # the queen, bishop & rook always move along lines
    for line in LINES.get(attacker.role, []):
        for delta in line:
            defender_coord = attacker_coord + delta
            defender = game[defender_coord]
            if defender is not None:
                if defender.player is game.inactive:
                    result.append(defender_coord)
                    break
                if defender.player is game.active:
                    break
                result.append(defender_coord)

    # the king and knight always have fixed potential translations
    for delta in DELTAS.get(attacker.role, []):
        defender_coord = attacker_coord + delta
        defender = game[defender_coord]
        if defender is not None and defender.player != game.active:
            result.append(defender_coord)
    return result


def _def_coords_pawn(game: "GameState", coord: Vector, player: Player) -> list[Vector]:
    """Implement `GameState.defending_coords` for pawns."""
    result = []

    if player is Player.ONE:
        direction = 1
        x_start = 1
    else:  # player is TWO
        direction = -1
        x_start = 6

    defender_coord = coord + (direction, 0)
    defender = game[defender_coord]
    if defender is not None and defender.role is Role.NULL:
        result.append(defender_coord)

    for dy in [1, -1]:
        defender_coord = coord + (direction, dy)
        defender = game[defender_coord]
        if defender is not None and defender.player == game.inactive:
            result.append(defender_coord)

    defender_coord = coord + (2 * direction, 0)
    if coord.x == x_start:
        result.append(defender_coord)

    return result


DELTAS = {
    # pylint: disable=unnecessary-comprehension  # mypy can't tell types if `list` used
    Role.KING: [(x, y) for x, y in product([-1, 0, +1], repeat=2)],
    Role.KNIGHT: (
        [(s * 2, t * 1) for s, t in product([1, -1], repeat=2)]
        + [(s * 1, t * 2) for s, t in product([1, -1], repeat=2)]
    ),
}


L1 = [[(s * d, t * d) for d in range(1, 8)] for s, t in CARDINAL_DIRECTION.values()]
L2 = [[(s * d, t * d) for d in range(1, 8)] for s, t in product([1, -1], repeat=2)]
LINES = {
    Role.QUEEN: L1 + L2,
    Role.ROOK: L1,
    Role.BISHOP: L2,
}
