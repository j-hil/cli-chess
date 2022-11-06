from copy import deepcopy
from itertools import product

from jchess.geometry import V, Vector, VectorSet
from jchess.pieces import LocPiece, Piece, Player, Role

KING, QUEEN, ROOK, BISHOP, KNIGHT, PAWN, _ = list(Role)

BACK_ROW_ROLES = (ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK)
BOARD_TEMPLATE = (
    *((V(x, 0), Piece(role, Player.TWO)) for x, role in enumerate(BACK_ROW_ROLES)),
    *((V(x, 1), Piece(PAWN, Player.TWO)) for x in range(8)),
    *((V(x, y), None) for x, y in product(range(8), range(2, 6))),
    *((V(x, 6), Piece(PAWN, Player.ONE)) for x in range(8)),
    *((V(x, 7), Piece(role, Player.ONE)) for x, role in enumerate(BACK_ROW_ROLES)),
)

DIAGONAL_VECS = V(1, 1), V(1, -1), V(-1, 1), V(-1, -1)
CARDINAL_VECS = V(1, 0), V(0, 1), V(-1, 0), V(0, -1)
L_VECS = V(-1, -2), V(-1, 2), V(1, -2), V(1, 2), V(-2, -1), V(-2, 1), V(2, -1), V(2, 1)
DIAGONALS = tuple(tuple(d * v for d in range(1, 8)) for v in DIAGONAL_VECS)
AXES = tuple(tuple(d * v for d in range(1, 8)) for v in CARDINAL_VECS)
DELTAS = {KING: DIAGONAL_VECS + CARDINAL_VECS, KNIGHT: L_VECS}
LINES = {QUEEN: DIAGONALS + AXES, ROOK: AXES, BISHOP: DIAGONALS}


class Board(dict[Vector, Piece | None]):
    """Represents the state of chess game & implements it's logic."""

    def __init__(self) -> None:
        self.update(BOARD_TEMPLATE)
        self.targets_of = {V(*v): VectorSet() for v in product(range(8), range(8))}
        self.passant: LocPiece | None = None
        self.ply = 0
        self.taken_pieces: dict[Player, list[Role]] = {Player.ONE: [], Player.TWO: []}
        self.protect_king = True
        self.update_targets()

    @property
    def active_player(self) -> Player:
        return list(Player)[self.ply % 2]

    def score(self, player: Player) -> int:
        return sum(role.worth for role in self.taken_pieces[player])

    def can_move_from(self, v: Vector) -> bool:
        piece = self[v]
        return bool(piece and piece.player is self.active_player and self.targets_of[v])

    def update_targets(self) -> None:
        """Update the `targets` attr of each piece."""

        for coord, attacker in self.items():
            if not attacker:
                self.targets_of[coord] = VectorSet()
                continue
            targets = VectorSet()

            if attacker.role is Role.PAWN:
                targets.update(self._pawn_targets(coord))

            # the queen, bishop & rook always move along lines
            for line in LINES.get(attacker.role, []):
                for delta in line:
                    target = coord + delta
                    if target not in self:
                        continue
                    defender = self[target]
                    if not defender:
                        targets.add(target)
                        continue
                    if defender.player is not attacker.player:
                        targets.add(target)
                    break

            # the king and knight always have fixed potential translations
            for delta in DELTAS.get(attacker.role, []):
                target = coord + delta
                if target in self:
                    defender = self[target]
                    if not defender or defender.player != attacker.player:
                        targets.add(target)

            # extra logic for castling
            if attacker.role is Role.KING and not attacker.moved:
                targets.update(self._casting_targets(coord))

            # extra logic exclude moves resulting in check/checkmate
            if self.protect_king:
                risky_targets = self._risky_targets(coord, targets)
                targets = {t for t in targets if t not in risky_targets}

            self.targets_of[coord] = targets

    def process_move(self, src: V, dst: V, *, promote_to: Role | None = None) -> None:
        attacker = self[src]
        defender = self[dst]
        delta = dst - src

        assert attacker, f"Move only processed when a piece is at {src=}."

        # remove any previous vulnerability to en passant
        if self.passant and self.passant.piece.player is self.active_player:
            self.passant = None

        # en passant capture
        if attacker.role is Role.PAWN and not defender and delta in DIAGONAL_VECS:
            self[src + V(delta.x, 0)] = None
            self.taken_pieces[self.active_player].append(Role.PAWN)

        # castling
        if attacker.role is Role.KING and abs(delta.x) == 2:
            y_king = src.y
            old_coord = V(7, y_king) if delta.x == 2 else V(0, y_king)
            new_coord = V(5, y_king) if delta.x == 2 else V(3, y_king)

            self[new_coord] = Piece(Role.ROOK, attacker.player, moved=True)
            self[old_coord] = None

        # execute standard move/capture
        if defender:
            self.taken_pieces[self.active_player].append(defender.role)
        self[src] = None
        attacker = Piece(promote_to or attacker.role, attacker.player, moved=True)
        self[dst] = attacker
        self.ply += 1

        # add any en passant vulnerability
        if attacker.role is Role.PAWN and abs(delta.y) == 2:
            self.passant = LocPiece(attacker, dst)

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

    def _pawn_targets(self, pawn_coord: Vector) -> VectorSet:

        pawn = self[pawn_coord]
        assert pawn and pawn.role is Role.PAWN, "Only call this function on a PAWN."
        dy = -1 if pawn.player is Player.ONE else 1
        targets = VectorSet()

        # standard forward step
        step_target = pawn_coord + V(0, dy)
        if step_target in self and not self[step_target]:
            targets.add(step_target)

        # double step (aka jump) move
        jump_target = pawn_coord + 2 * V(0, dy)
        can_jump = not pawn.moved and not self[step_target] and not self[jump_target]
        if can_jump:
            targets.add(jump_target)

        # standard and en passant captures
        for dx in [1, -1]:
            capture_target = pawn_coord + V(dx, dy)
            passant_coord = pawn_coord + V(dx, 0)

            defender = self.get(capture_target, None)
            neighbor = self.get(passant_coord, None)

            can_std_capture = defender and defender.player is not pawn.player
            can_passant = neighbor and self.passant == LocPiece(neighbor, passant_coord)
            if can_std_capture or can_passant:
                targets.add(capture_target)

        return targets

    def _casting_targets(self, coord: Vector) -> VectorSet:
        king = self[coord]
        assert king and king.role is Role.KING, "Only call this function on a KING."
        y_king = coord.y

        targets = VectorSet()
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
                    V(x, y_king) not in self.targets_of[v]
                    for (v, p), x in product(self.items(), path_xvals)
                    if p and p.player is not self.active_player
                )
            ):
                targets.add(coord + sign * V(2, 0))
        return targets

    def _risky_targets(self, source: Vector, current_targets: VectorSet) -> VectorSet:
        attacker = self[source]
        assert attacker, f"Only call if there is a piece at {source=}"
        risky_targets = VectorSet()

        for current_target in current_targets:
            # try out the attack without concern for check/checkmate
            board_copy = deepcopy(self)
            board_copy.protect_king = False
            board_copy.update_targets()
            board_copy.process_move(source, current_target)

            # note if the move caused check/checkmate
            if board_copy.in_check(attacker.player):
                risky_targets.add(current_target)
                continue

        return risky_targets

    def in_check(self, player: Player) -> bool:
        # ap = attacking_piece, tp = target_piece
        return any(
            (ap and ap.player is not player)
            and any((tp := self[t]) and tp.role is KING for t in self.targets_of[v])
            for v, ap in self.items()
        )
