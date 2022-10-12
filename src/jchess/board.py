from copy import deepcopy
from itertools import product

from jchess.geometry import Vector, VectorLike, Vectors
from jchess.pieces import Piece, Role, Player

K, Q, R, B, N, P = list(Role)
BACK_ROW = [R, N, B, Q, K, B, N, R]


class Board:
    """Represents the state of chess game & implements it's logic."""

    @staticmethod
    def has(coord: VectorLike) -> bool:
        """Check if a coordinate is within the board bounds."""
        return coord[0] in range(8) and coord[1] in range(8)

    def __init__(self):
        """Initialise a standard chessboard layout."""
        self.pieces: list[Piece] = [
            *[Piece(role, Player.TWO, (x, 0)) for x, role in enumerate(BACK_ROW)],
            *[Piece(Role.PAWN, Player.TWO, (x, 1)) for x in range(8)],
            *[Piece(Role.PAWN, Player.ONE, (x, 6)) for x in range(8)],
            *[Piece(role, Player.ONE, (x, 7)) for x, role in enumerate(BACK_ROW)],
        ]

        self.passant_vulnerable_piece: Piece | None = None
        self.turn = 0
        self.taken_pieces: dict[Player, list[Role]] = {Player.ONE: [], Player.TWO: []}

        self.protect_king = True

        self.update_targets()

    @property
    def active_player(self) -> Player:
        return list(Player)[self.turn % 2]  # type: ignore  # (wrong as x % 2 in [0, 1])

    def update_targets(self):
        """Update the targets attribute for each piece on the board."""
        _update_targets(self)

    def process_attack(self, attacker: Piece, defender_coord: Vector):
        _process_attack(self, attacker, defender_coord)

    def score(self, player: Player) -> int:
        return sum(role.worth for role in self.taken_pieces[player])

    def __getitem__(self, key: VectorLike) -> Piece | None:
        for piece in self.pieces:
            if piece._coord == key:
                return piece
        return None

    def __setitem__(self, key: VectorLike, value: Piece) -> None:
        value.coord = key
        self.pieces.append(value)


def _update_targets(game: Board):
    """Implement of `Board.update_targets`."""

    for attacker in game.pieces:
        targets: Vectors = []

        # the pawn has unique behavior warranting it's own function
        if attacker.role is Role.PAWN:
            targets.extend(_pawn_targets(game, attacker))

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
            targets.extend(_castling_targets(game, attacker))

        # extra logic for check
        if game.protect_king:
            bad_targets = _risky_targets(game, attacker, targets)
            targets = [t for t in targets if t not in bad_targets]

        attacker.targets = targets


def _risky_targets(board: Board, attacker: Piece, current_targets: Vectors) -> Vectors:
    """Compute the targets which, if attacked, would leave the king in check."""
    result = []

    for defender_coord in current_targets:
        board_copy = deepcopy(board)
        attacker_copy = deepcopy(attacker)

        # initiate the attack
        board_copy.protect_king = False
        board_copy.update_targets()
        _process_attack(board_copy, attacker_copy, defender_coord)

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


def _pawn_targets(board: "Board", attacker: Piece) -> list[Vector]:
    """Compute the targets of a pawn attacker."""
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


def _process_attack(board: "Board", attacker: Piece, defender_coord: Vector) -> None:
    """Implement of `Board.process_attack`."""

    defender = board[defender_coord]
    delta = defender_coord - attacker.coord

    # remove any previous vulnerability to en passant
    if (
        board.passant_vulnerable_piece is not None
        and board.passant_vulnerable_piece.player is board.active_player
    ):
        board.passant_vulnerable_piece = None

    # add any new vulnerability to en passant
    if attacker.role is Role.PAWN and delta in [(0, 2), (0, -2)]:
        board.passant_vulnerable_piece = attacker

    # en passant move chosen, so delete piece to the left/right
    if (
        attacker.role is Role.PAWN
        and delta in [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        and defender is None
        # not really required: pleases type checker
        and board.passant_vulnerable_piece is not None
    ):
        board.pieces.remove(board.passant_vulnerable_piece)
        board.taken_pieces[board.active_player].append(Role.PAWN)

    # castling
    if attacker.role is Role.KING:
        y_king = attacker.coord.y

        # king-side castle
        if delta.x == 2:
            castle = board[7, y_king]
            if castle is None:
                raise RuntimeError("King-side castling shouldn't have been available.")
            castle.coord = (5, y_king)

        # queen-side caste
        if delta.x == -2:
            castle = board[0, y_king]
            if castle is None:
                raise RuntimeError("Queen-side castling shouldn't have been available.")
            castle.coord = (3, y_king)

    # execute move
    attacker.coord = defender_coord
    if defender is not None:
        board.pieces.remove(defender)
        board.taken_pieces[board.active_player].append(defender.role)
    board.turn += 1
    board.update_targets()


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
