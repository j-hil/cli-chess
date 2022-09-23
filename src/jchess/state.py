from itertools import product
from colorama import Style

from jchess.geometry import Vector
from jchess.pieces import Piece, Role, Player
from jchess.configs import Config, VS_CODE_CONFIG

BACK_ROW = [Role.ROOK, Role.KNIGHT, Role.BISHOP, Role.QUEEN, Role.KING, Role.BISHOP, Role.KNIGHT, Role.ROOK]


class GameState:
    def __init__(self, config: Config = VS_CODE_CONFIG):
        self.board: list[list[Piece]] = list(map(list, zip(*[
            [Piece(role, Player.ONE) for role in BACK_ROW],
            [Piece(Role.PAWN, Player.ONE) for _ in range(8)],
            *[[Piece(Role.NULL, Player.NULL) for _ in range(8)] for _ in range(4)],
            [Piece(Role.PAWN, Player.TWO) for _ in range(8)],
            [Piece(role, Player.TWO) for role in BACK_ROW],
        ])))
        self.config = config

        self.cursor_coord = Vector(4, 4)
        self.attacker_coord: Vector | None = None
        self.active_player = Player.ONE
        self.inactive_player = Player.TWO

    @property
    def attacker(self):
        if self.attacker_coord is None:
            return None
        return self[self.attacker_coord]

    @property
    def highlighted(self):
        return self[self.cursor_coord]

    def can_select_attacker(self):
        highlighted = self.highlighted
        return (
            self.attacker_coord is None
            and highlighted.role is not Role.NULL
            and highlighted.player == self.active_player
            and self.defending_coords(self.cursor_coord)  # check non-empty
        )

    def defending_coords(self, attacker_coord: Vector | None) -> list[Vector]:
        if attacker_coord is None:
            return []

        attacker = self[attacker_coord]

        if attacker is None:
            return []

        result = []
        if attacker.role is Role.KING:
            deltas: list[tuple[int, int]] = product([-1, 0, +1], repeat=2)
            for delta in deltas:
                defender_coord = attacker_coord + delta
                defender = self[defender_coord]
                if defender is not None and defender.player != self.active_player:
                    result.append(defender_coord)

        if attacker.role in [Role.ROOK, Role.QUEEN]:
            lines = [
                [attacker_coord + (s * d, t * d) for d in range(1, 8)]
                for s, t in [(0, 1), (1, 0), (-1, 0), (0, -1)]
            ]
            for line in lines:
                for defender_coord in line:
                    defender = self[defender_coord]
                    if defender is not None:
                        if defender.player is Player.NULL:
                            result.append(defender_coord)
                            continue
                        if defender.player is self.active_player:
                            break
                        result.append(defender_coord)
                        break

        if attacker.role in [Role.BISHOP, Role.QUEEN]:
            lines = [
                [attacker_coord + ( s* d,  t* d) for d in range(1, 8)]
                for s, t in product([1, -1], repeat=2)
            ]
            for line in lines:
                for defender_coord in line:
                    defender = self[defender_coord]
                    if defender is not None:
                        if defender.player is self.inactive_player:
                            result.append(defender_coord)
                            break
                        if defender.player is self.active_player:
                            break
                        result.append(defender_coord)

        if attacker.role is Role.KNIGHT:
            deltas =( [(s*2, t*1) for s, t in product([1, -1], repeat=2)]
             +    [(s*1, t*2) for s, t in product([1, -1], repeat=2)])
            for delta in deltas:
                defender_coord = attacker_coord + delta
                defender = self[defender_coord]
                if defender is not None and defender.player != self.active_player:
                    result.append(defender_coord)

        if attacker.role is Role.PAWN:
            if attacker.player is Player.ONE:
                direction = 1
                x_start = 1
            else: # player is TWO
                direction = -1
                x_start = 6

            defender_coord = attacker_coord + (direction, 0)
            defender = self[defender_coord]
            if defender is not None and defender.role is Role.NULL:
                result.append(defender_coord)

            defender_coord = attacker_coord + (direction, 1)
            defender = self[defender_coord]
            if defender is not None and defender.player not in [Player.NULL, self.active_player]:
                result.append(defender_coord)

            defender_coord = attacker_coord + (direction, -1)
            defender = self[defender_coord]
            if defender is not None and defender.player not in [Player.NULL, self.active_player]:
                result.append(defender_coord)

            defender_coord = attacker_coord + (2 * direction, 0)
            if attacker_coord.x == x_start:
                result.append(defender_coord)

        return result

    def make_move(self):
        self[self.cursor_coord] = self[self.attacker_coord]
        self[self.attacker_coord]  = Piece(Role.NULL, Player.NULL)

        self.active_player, self.inactive_player = self.inactive_player, self.active_player
        self.attacker_coord = None

    def __getitem__(self, key: Vector) -> Piece | None:
        if key.in_bounds():
            return self.board[key.y][key.x]
        return None

    def __setitem__(self, key: Vector, value: Piece):
        self.board[key.y][key.x] = value

    def __str__(self):
        row_strings = [
            ":      a   b   c   d   e   f   g   h  ",
            ":    +---+---+---+---+---+---+---+---+",
        ]

        for i in range(8):
            current_row = f":  {i} |"
            for j in range(8):
                if Vector(j, i) == self.cursor_coord:
                    current_row += self.config.cursor_color
                elif Vector(j, i) == self.attacker_coord:
                    current_row += self.config.selected_color
                elif self.attacker_coord is not None and Vector(j, i) in self.defending_coords(self.attacker_coord):
                    current_row += self.config.valid_color
                else:
                    current_row += self.config.board_color[(i + j) % 2]

                piece = self.board[i][j]
                fore_color = self.config.player_color[piece.player]
                symbol = self.config.role_symbol[piece.role]
                current_row += fore_color + f" {symbol} " + Style.RESET_ALL + "|"
            current_row += f" {i}"

            row_strings.append(current_row)
            row_strings.append(":    +---+---+---+---+---+---+---+---+")

        row_strings.append(":      a   b   c   d   e   f   g   h  ")
        row_strings.append(Style.NORMAL)
        return "\n".join(row_strings)
