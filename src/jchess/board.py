from copy import deepcopy
from itertools import product
from typing import cast

from jchess.geometry import V, Vector, Vectors
from jchess.pieces import Piece, Player, Role, Square

K, Q, R, B, N, _, _ = list(Role)
_P2_BACK_ROW = list((V(x, 0), r) for x, r in enumerate((R, N, B, Q, K, B, N, R)))
_P1_BACK_ROW = list((V(x, 7), r) for x, r in enumerate((R, N, B, Q, K, B, N, R)))

_KNIGHT_DELTAS = tuple(product((-1, 1), (-2, 2))) + tuple(product((-2, 2), (-1, 1)))
DELTAS = {
    Role.KING: tuple(V(x, y) for x, y in tuple(product([-1, 0, +1], [-1, 0, +1]))),
    Role.KNIGHT: tuple(V(x, y) for x, y in _KNIGHT_DELTAS),
}

_CARDINAL_DIRECTIONS = ((1, 0), (0, 1), (-1, 0), (0, -1))
_L = tuple(tuple(d * V(*v) for d in range(1, 8)) for v in _CARDINAL_DIRECTIONS)
_M = tuple(tuple(d * V(*v) for d in range(1, 8)) for v in product((1, -1), (1, -1)))
LINES = {Role.QUEEN: _L + _M, Role.ROOK: _L, Role.BISHOP: _M}

DIAGONALS = (V(1, 1), V(1, -1), V(-1, 1), V(-1, -1))


class Board(dict[Vector, Piece | None]):
    """Represents the state of chess game & implements it's logic."""

    def __init__(self) -> None:
        self.update(
            {v: Piece(role, Player.TWO) for v, role in _P2_BACK_ROW}
            | {V(x, 1): Piece(Role.PAWN, Player.TWO) for x in range(8)}
            | {V(x, y): None for x, y in product(range(8), range(2, 6))}
            | {V(x, 6): Piece(Role.PAWN, Player.ONE) for x in range(8)}
            | {v: Piece(role, Player.ONE) for v, role in _P1_BACK_ROW}
        )

        self.targets = {V(*v): cast(Vectors, []) for v in product(range(8), range(8))}
        self.passant: Square | None = None
        self.ply = 0
        self.taken_pieces: dict[Player, list[Role]] = {Player.ONE: [], Player.TWO: []}
        self.protect_king = True

        self.update_targets()

    @property
    def active_player(self) -> Player:
        return list(Player)[self.ply % 2]

    def score(self, player: Player) -> int:
        return sum(role.worth for role in self.taken_pieces[player])

    def update_targets(self) -> None:
        """Update the `targets` attr of each piece."""
        # TODO: king seems to be wrong in specific situations eg after promoted knight

        for coord, attacker in self.items():
            if not attacker:
                self.targets[coord] = []
                continue
            targets: Vectors = []

            if attacker.role is Role.PAWN:
                targets.extend(self._pawn_targets(coord))

            # the queen, bishop & rook always move along lines
            for line in LINES.get(attacker.role, []):
                for delta in line:
                    target = coord + delta
                    if target not in self:
                        continue
                    defender = self[target]
                    if not defender:
                        targets.append(target)
                        continue
                    if defender.player is not attacker.player:
                        targets.append(target)
                    break

            # the king and knight always have fixed potential translations
            for delta in DELTAS.get(attacker.role, []):
                target = coord + delta
                if target in self:
                    defender = self[target]
                    if not defender or defender.player != attacker.player:
                        targets.append(target)

            # extra logic for castling
            if attacker.role is Role.KING and not attacker.moved:
                targets.extend(self._casting_targets(coord))

            # extra logic exclude moves resulting in check/checkmate
            if self.protect_king:
                risky_targets = self._risky_targets(coord, targets)
                targets = [t for t in targets if t not in risky_targets]

            self.targets[coord] = targets

    def process_move(
        self, source: Vector, target: Vector, *, promote_to: Role | None = None
    ) -> None:
        attacker = self[source]
        defender = self[target]
        delta = target - source

        assert attacker, f"Move only processed when a piece is at {source=}."

        # remove any previous vulnerability to en passant
        if self.passant and self.passant.piece.player is self.active_player:
            self.passant = None

        # en passant capture
        if attacker.role is Role.PAWN and not defender and delta in DIAGONALS:
            self[source + V(delta.x, 0)] = None
            self.taken_pieces[self.active_player].append(Role.PAWN)

        # castling
        if attacker.role is Role.KING and abs(delta.x) == 2:
            y_king = source.y
            old_coord = V(7, y_king) if delta.x == 2 else V(0, y_king)
            new_coord = V(5, y_king) if delta.x == 2 else V(3, y_king)

            self[new_coord] = Piece(Role.ROOK, attacker.player, moved=True)
            self[old_coord] = None

        # execute standard move/capture
        if defender:
            self.taken_pieces[self.active_player].append(defender.role)
        self[source] = None
        attacker = Piece(promote_to or attacker.role, attacker.player, moved=True)
        self[target] = attacker
        self.ply += 1

        # add any en passant vulnerability
        if attacker.role is Role.PAWN and abs(delta.y) == 2:
            self.passant = Square(attacker, target)

        self.update_targets()

    def __repr__(self) -> str:
        parts = []
        for y, x in product(range(8), range(8)):
            key = V(x, y)
            if piece := self[key]:
                parts.append(f"{piece.role.symbol}{piece.player.value}")
            else:
                parts.append("--")
            parts.append(" " if x != 7 else "\n")
        return "".join(parts)

    # Helper methods for `self.update_targets` --------------------------------------- #

    def _pawn_targets(self, pawn_coord: Vector) -> Vectors:

        pawn = self[pawn_coord]
        assert pawn and pawn.role is Role.PAWN, "Only call this function on a PAWN."
        dy = -1 if pawn.player is Player.ONE else 1
        targets = []

        # standard forward step
        step_target = pawn_coord + V(0, dy)
        if step_target in self and not self[step_target]:
            targets.append(step_target)

        # double step (aka jump) move
        jump_target = pawn_coord + 2 * V(0, dy)
        can_jump = not pawn.moved and not self[step_target] and not self[jump_target]
        if can_jump:
            targets.append(jump_target)

        # standard and en passant captures
        for dx in [1, -1]:
            capture_target = pawn_coord + V(dx, dy)
            passant_coord = pawn_coord + V(dx, 0)

            defender = self.get(capture_target, None)
            neighbor = self.get(passant_coord, None)

            can_std_capture = defender and defender.player is not pawn.player
            can_passant = neighbor and self.passant == Square(neighbor, passant_coord)
            if can_std_capture or can_passant:
                targets.append(capture_target)

        return targets

    def _casting_targets(self, coord: Vector) -> Vectors:
        king = self[coord]
        assert king and king.role is Role.KING, "Only call this function on a KING."
        y_king = coord.y

        targets = []
        for x_rook, sign in zip((0, 7), (1, -1)):
            rook = self[V(x_rook, y_king)]
            path_xvals = range(x_rook + sign, 4 + sign, sign)
            if (
                # unmoved rook
                (rook and rook.role is Role.ROOK and not rook.moved)
                # empty path
                and all(not self[V(x, y_king)] for x in path_xvals[:-1])
                # safe path
                and all(
                    V(x, y_king) not in self.targets[v]
                    for v, x in product(self, path_xvals)
                    if (p := self[v]) and p.player is not self.active_player
                )
            ):
                targets.append(coord + sign * V(2, 0))
        return targets

    def _risky_targets(self, source: Vector, current_targets: Vectors) -> Vectors:
        attacker = self[source]
        assert attacker, f"Only call if there is a piece at {source=}"
        risky_targets: Vectors = []

        for current_target in current_targets:
            # try out the attack without concern for check/checkmate
            board_copy = deepcopy(self)
            board_copy.protect_king = False
            board_copy.update_targets()
            board_copy.process_move(source, current_target)

            # note if the move caused check/checkmate
            if board_copy.in_check(attacker.player):
                risky_targets.append(current_target)
                continue

        return risky_targets

    def in_check(self, player: Player):
        # ap = attacking_piece, tp = target_piece
        return any(
            (ap and ap.player is not player)
            and any((tp := self[t]) and tp.role is K for t in self.targets[v])
            for v, ap in self.items()
        )
