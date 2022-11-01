from copy import deepcopy
from itertools import product

from jchess.geometry import V, Vector, Vectors
from jchess.pieces import Piece, Player, Role

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


class Board(dict[Vector, Piece | None]):
    """Represents the state of chess game & implements it's logic."""

    def __init__(self) -> None:
        self.update(
            {v: Piece(role, Player.TWO, v) for v, role in _P2_BACK_ROW}
            | {V(x, 1): Piece(Role.PAWN, Player.TWO, V(x, 1)) for x in range(8)}
            | {V(x, y): None for x, y in product(range(8), range(2, 6))}
            | {V(x, 6): Piece(Role.PAWN, Player.ONE, V(x, 6)) for x in range(8)}
            | {v: Piece(role, Player.ONE, v) for v, role in _P1_BACK_ROW}
        )

        self.passant_defender: Piece | None = None
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
                continue
            targets: Vectors = []

            if attacker.role is Role.PAWN:
                targets.extend(self._pawn_targets(attacker))

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
            if attacker.role is Role.KING and attacker.unmoved():
                targets.extend(self._casting_targets(attacker))

            # extra logic exclude moves resulting in check/checkmate
            if self.protect_king:
                risky_targets = self._risky_targets(attacker, targets)
                targets = [t for t in targets if t not in risky_targets]

            attacker.targets = targets

    def process_move(self, attacker: Piece, target: Vector) -> None:

        defender = self[target]
        delta = target - attacker.coord

        # remove any previous vulnerability to en passant
        if self.passant_defender and self.passant_defender.player is self.active_player:
            self.passant_defender = None

        if attacker.role is Role.PAWN:
            if abs(delta.y) == 2:
                # add any new vulnerability to en passant
                self.passant_defender = attacker
            elif not defender and delta in [V(1, 1), V(1, -1), V(-1, 1), V(-1, -1)]:
                # en passant chosen, so delete piece to left/right
                self[attacker.coord + V(delta.x, 0)] = None
                self.taken_pieces[self.active_player].append(Role.PAWN)

        if attacker.role is Role.KING and abs(delta.x) == 2:
            y_king = attacker.coord.y

            old_coord = V(7, y_king) if delta.x == 2 else V(0, y_king)
            new_coord = V(5, y_king) if delta.x == 2 else V(3, y_king)

            # this section could be simplified if use pieces are frozen dataclass
            rook = self[old_coord]
            assert rook, f"Must be rook at {old_coord}."
            rook.coord = new_coord
            self[new_coord] = rook
            self[old_coord] = None

        # execute move
        if defender:
            self.taken_pieces[self.active_player].append(defender.role)
        self[attacker.coord] = None
        attacker.coord = target
        self[target] = attacker
        self.ply += 1
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

    def _pawn_targets(self, pawn: Piece) -> Vectors:

        assert pawn.role is Role.PAWN, "Only call this function on a PAWN."
        targets = []

        pawn_coord = pawn.coord
        dy = -1 if pawn.player is Player.ONE else 1

        # standard forward step
        step_target = pawn_coord + V(0, dy)
        if step_target in self and not self[step_target]:
            targets.append(step_target)

        # double step (aka jump) move
        jump_target = pawn_coord + 2 * V(0, dy)
        can_jump = pawn.unmoved() and not self[step_target] and not self[jump_target]
        if can_jump:
            targets.append(jump_target)

        # standard and passant captures
        for dx in [1, -1]:
            capture_target = pawn_coord + V(dx, dy)

            std_defender = self.get(capture_target, None)
            passant_defender = self.get(pawn_coord + V(dx, 0), None)

            can_std_capture = std_defender and std_defender.player is not pawn.player
            can_passant = passant_defender and passant_defender is self.passant_defender
            if can_std_capture or can_passant:
                targets.append(capture_target)

        return targets

    def _casting_targets(self, king: Piece) -> Vectors:

        assert king.role is Role.KING, "Only call this function on a KING."
        y_king = king.coord.y

        targets = []
        for x_rook, sign in zip((0, 7), (1, -1)):
            rook = self[V(x_rook, y_king)]
            path_xvals = range(x_rook + sign, 4 + sign, sign)
            if (
                (rook and rook.role is Role.ROOK and rook.unmoved())  # unmoved rook
                and all(not self[V(x, y_king)] for x in path_xvals[:-1])  # empty path
                and all(  # safe path
                    V(x, y_king) not in p.targets
                    for p, x in product(self.values(), path_xvals)
                    if p and p.player is not self.active_player
                )
            ):
                targets.append(king.coord + sign * V(2, 0))
        return targets

    def _risky_targets(self, attacker: Piece, current_targets: Vectors) -> Vectors:
        # TODO: add a test for risky targets
        risky_targets = []

        for target in current_targets:

            board_copy = deepcopy(self)

            # wouldn't be necessary to copy if Piece were frozen dataclass
            attacker_copy = board_copy[attacker.coord]
            assert attacker_copy, "`attacker != None` => `attacker_copy != None`"

            # try out the attack without concern for check/checkmate
            board_copy.protect_king = False
            board_copy.update_targets()
            board_copy.process_move(attacker_copy, target)

            # note if the move caused check/checkmate
            for piece in board_copy.values():
                if piece and piece.player is not attacker_copy.player:
                    if any(
                        (defender := self[next_target]) and defender.role is Role.KING
                        for next_target in piece.targets
                    ):
                        risky_targets.append(target)

        return risky_targets
