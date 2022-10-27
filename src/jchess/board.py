from copy import deepcopy
from itertools import product

from jchess.geometry import Vector, VectorLike, Vectors
from jchess.pieces import Piece, Player, Role

K, Q, R, B, N, P = list(Role)
BACK_ROW = [R, N, B, Q, K, B, N, R]
# TODO: del added in testing, integrate properly


class Board:
    """Represents the state of chess game & implements it's logic."""

    @staticmethod
    def has(coord: VectorLike) -> bool:
        """Check if a coordinate is within the board bounds."""
        return coord[0] in range(8) and coord[1] in range(8)

    def __init__(self) -> None:
        """Initialise a standard chessboard layout."""
        self.pieces: list[Piece] = [
            *[Piece(role, Player.TWO, (x, 0)) for x, role in enumerate(BACK_ROW)],
            *[Piece(Role.PAWN, Player.TWO, (x, 1)) for x in range(8)],
            *[Piece(Role.PAWN, Player.ONE, (x, 6)) for x in range(8)],
            *[Piece(role, Player.ONE, (x, 7)) for x, role in enumerate(BACK_ROW)],
        ]

        self.passant_defender: Piece | None = None
        self.ply = 0
        self.taken_pieces: dict[Player, list[Role]] = {Player.ONE: [], Player.TWO: []}

        self.protect_king = True

        self.update_targets()

    @property
    def active_player(self) -> Player:
        return list(Player)[self.ply % 2]

    def update_targets(self) -> None:
        """Update the targets attribute for each piece on the board."""
        for attacker in self.pieces:
            targets: Vectors = []

            # the pawn has unique behavior warranting it's own function
            if attacker.role is Role.PAWN:
                targets.extend(_pawn_targets(self, attacker))

            # the queen, bishop & rook always move along lines
            for line in LINES.get(attacker.role, []):
                for delta in line:
                    defender_coord = attacker.coord + delta
                    if self.has(defender_coord):
                        defender = self[defender_coord]
                        if defender is None:
                            targets.append(defender_coord)
                            continue
                        if defender.player is not attacker.player:
                            targets.append(defender_coord)
                        break

            # the king and knight always have fixed potential translations
            for delta in DELTAS.get(attacker.role, []):
                defender_coord = attacker.coord + delta
                if self.has(defender_coord):
                    defender = self[defender_coord]
                    if defender is None or defender.player != attacker.player:
                        targets.append(defender_coord)

            # extra logic for castling
            if attacker.role is Role.KING and attacker.unmoved():
                targets.extend(_castling_targets(self, attacker))

            # extra logic for check/checkmate
            if self.protect_king:
                bad_targets = _risky_targets(self, attacker, targets)
                targets = [t for t in targets if t not in bad_targets]

            attacker.targets = targets

    def process_attack(self, attacker: Piece, defender_coord: Vector) -> None:
        defender = self[defender_coord]
        delta = defender_coord - attacker.coord

        # remove any previous vulnerability to en passant
        if self.passant_defender and self.passant_defender.player is self.active_player:
            self.passant_defender = None

        # add any new vulnerability to en passant
        if attacker.role is Role.PAWN and delta in [(0, 2), (0, -2)]:
            self.passant_defender = attacker

        # en passant move chosen, so delete piece to the left/right
        if (
            attacker.role is Role.PAWN
            and delta in [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            and defender is None
            and self.passant_defender is not None  # pleases type checkers
        ):
            self.pieces.remove(self.passant_defender)
            self.taken_pieces[self.active_player].append(Role.PAWN)

        # castling
        if attacker.role is Role.KING:
            y_king = attacker.coord.y

            # king-side castle
            if delta.x == 2:
                castle = self[7, y_king]
                if castle is None:
                    raise RuntimeError(
                        "King-side castling shouldn't have been available."
                    )
                castle.coord = (5, y_king)

            # queen-side caste
            if delta.x == -2:
                castle = self[0, y_king]
                if castle is None:
                    raise RuntimeError(
                        "Queen-side castling shouldn't have been available."
                    )
                castle.coord = (3, y_king)

        # execute move
        attacker.coord = defender_coord
        if defender is not None:
            self.pieces.remove(defender)
            self.taken_pieces[self.active_player].append(defender.role)
        self.ply += 1
        self.update_targets()

    def score(self, player: Player) -> int:
        return sum(role.worth for role in self.taken_pieces[player])

    def __getitem__(self, key: VectorLike) -> Piece | None:
        for piece in self.pieces:
            if piece.coord == key:
                return piece
        return None

    def __setitem__(self, key: VectorLike, value: Piece) -> None:
        value.coord = key
        del self[key]
        self.pieces.append(value)

    def __delitem__(self, key: VectorLike) -> None:
        for i, piece in enumerate(self.pieces):
            if piece.coord == key:
                del self.pieces[i]
                return


def _risky_targets(board: Board, attacker: Piece, current_targets: Vectors) -> Vectors:
    """Compute the targets which, if attacked, would leave the king in check."""
    result = []

    for defender_coord in current_targets:
        board_copy = deepcopy(board)
        attacker_copy = deepcopy(attacker)

        # initiate the attack
        board_copy.protect_king = False
        board_copy.update_targets()
        board_copy.process_attack(attacker_copy, defender_coord)

        for piece in board_copy.pieces:
            if piece.player is not attacker_copy.player:
                for coord in piece.targets:
                    target = board_copy[coord]
                    if target is not None and target.role is Role.KING:
                        result.append(defender_coord)
    return result


def _castling_targets(board: Board, attacker: Piece) -> Vectors:
    """Compute the coords which the attacker (a king) can move to via castling."""

    result = []
    y_king = attacker.coord.y

    for x_rook, sign in zip((0, 7), (+1, -1)):
        rook = board[(x_rook, y_king)]
        path = range(x_rook + sign, 4 + sign, sign)

        unmoved_rook = rook and rook.role is Role.ROOK and rook.unmoved()
        empty_path = all(board[(x, y_king)] is None for x in path[:-1])
        safe_path = all(
            (x, y_king) not in p.targets
            for p, x in product(board.pieces, path)
            if p.player is not board.active_player
        )

        if unmoved_rook and empty_path and safe_path:
            result.append(attacker.coord + sign * Vector(2, 0))

    return result


def _pawn_targets(board: "Board", attacker: Piece) -> Vectors:
    """Compute the targets of a pawn attacker."""
    result = []
    attacker_coord = attacker.coord

    # map 1 to -1 and 2 to +1 (i.e up or down depending on player)
    dy = 2 * attacker.player.value - 3

    defender_coord = attacker_coord + (0, dy)
    if board[defender_coord] is None:
        result.append(defender_coord)

    for dx in [1, -1]:
        defender_coord = attacker_coord + (dx, dy)
        defender = board[defender_coord]
        passant_defender = board[attacker_coord + (dx, 0)]

        can_standard_capture = defender and defender.player is not attacker.player
        can_passant = passant_defender and passant_defender == board.passant_defender
        if can_standard_capture or can_passant:
            result.append(defender_coord)

    defender_coord = attacker_coord + (0, 2 * dy)
    if (
        attacker.unmoved()
        and board[attacker_coord + (0, dy)] is None
        and board[defender_coord] is None
    ):
        result.append(defender_coord)

    return result


DELTAS = {
    Role.KING: list(product([-1, 0, +1], [-1, 0, +1])),
    Role.KNIGHT: list(product((-1, 1), (-2, 2))) + list(product((-2, 2), (-1, 1))),
}


CARDINAL_DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
L1 = [[(s * d, t * d) for d in range(1, 8)] for s, t in CARDINAL_DIRECTIONS]
L2 = [[(s * d, t * d) for d in range(1, 8)] for s, t in product([1, -1], repeat=2)]
LINES = {
    Role.QUEEN: L1 + L2,
    Role.ROOK: L1,
    Role.BISHOP: L2,
}
