from jchess.geometry import VectorLike
from jchess.pieces import Piece, Role, Player
from jchess.game.logic import update_targets_

K, Q, R, B, N, P = list(Role)
BACK_ROW = [R, N, B, Q, K, B, N, R]

class Board:
    """Represents the state of chess game & implements it's logic."""

    @staticmethod
    def has(coord: VectorLike) -> bool:
        return coord[0] in range(8) and coord[1] in range(8)

    def __init__(self):
        """Initialise a standard chessboard layout."""
        self.pieces = [
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

    def update_targets(self):
        update_targets_(self)

    def score(self, player: Player) -> int:
        return sum(role.worth for role in self.taken_pieces[player])

    def active_player(self) -> Player:
        return list(Player)[self.turn % 2]

    def __getitem__(self, key: VectorLike) -> Piece | None:
        for piece in self.pieces:
            if piece._coord == key:
                return piece
        return None

    def __setitem__(self, key: VectorLike, value: Piece) -> None:
        value.coord = key
        self.pieces.append(value)
