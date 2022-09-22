from itertools import product
from colorama import Style

from jchess.pieces import Piece, Role, Player
from jchess.configs import Config, VS_CODE_CONFIG

BACK_ROW = [Role.ROOK, Role.KNIGHT, Role.BISHOP, Role.QUEEN, Role.KING, Role.BISHOP, Role.KNIGHT, Role.ROOK]


class GameState:
    def __init__(self, config: Config = VS_CODE_CONFIG):
        m = [
            [Piece(role, Player.ONE) for role in BACK_ROW],
            [Piece(Role.PAWN, Player.ONE) for _ in range(8)],
            *[[Piece(Role.NULL, Player.NULL) for _ in range(8)] for _ in range(4)],
            [Piece(Role.PAWN, Player.TWO) for _ in range(8)],
            [Piece(role, Player.TWO) for role in BACK_ROW],
        ]
        self.board: list[list[Piece]] = list(map(list, zip(*m)))
        self.config = config

        self.cursor = (4, 4)
        self.selected: tuple[int, int] | None = None
        self.active_player = Player.ONE

    def can_select_attacker(self):
        x, y = self.cursor
        piece = self.board[y][x]
        return (
            self.selected is None
            and piece.role is not Role.NULL
            and self.defending_coords((x, y))
            and piece.player == self.active_player
        )

    def defending_coords(self, coord: tuple[int, int] | None):
        if coord is None:
            return []
        x, y = coord
        attacker = self.board[y][x]

        result = []
        if attacker.role is Role.KING:
            for d, dy in product([-1, 0, +1], repeat=2):
                if y + dy in range(8) and x + d in range(8):
                    target = self.board[y+dy][x + d]
                    if target.player != self.active_player:
                        result.append((x + d, y+dy))

        if attacker.role in [Role.ROOK, Role.QUEEN]:
            for s in [1, -1]:
                for dx in range(1, 8):
                    if (x + s*dx) in range(8):
                        target= self.board[y][x+s*dx]
                        if target.player != Player.NULL and target.player == attacker.player:
                            break
                        if target.player != Player.NULL and target.player != attacker.player:
                            result.append((x + s*dx, y))
                            break
                        result.append((x + s*dx, y))

                for dy in range(1, 8):
                    if (y + dy) in range(8):
                        target = self.board[y+s*dy][x]
                        if target.player != Player.NULL and target.player == attacker.player:
                            break
                        if target.player != Player.NULL and target.player != attacker.player:
                            result.append((x, y+s*dy))
                            break
                        result.append((x, y+s*dy))

        if attacker.role in [Role.BISHOP, Role.QUEEN]:
            for s1, s2 in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                for d in range(1, 8):
                    xt, yt = x+s1*d, y+s2*d
                    if y+s2*d in range(8) and x+s1*d in range(8):
                        target = self.board[y+s2*d][x+s1*d]
                        if target.player != Player.NULL and target.player == attacker.player:
                            break
                        if target.player != Player.NULL and target.player != attacker.player:
                            result.append((xt, yt))
                            break
                        result.append((xt, yt))

        if attacker.role is Role.KNIGHT:
            deltas = [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]
            for dx, dy in deltas:
                if x + dx in range(8) and y + dy in range(8):
                    target = self.board[y+dy][x+dx]
                    if target.player != Player.NULL and target.player != attacker.player:
                        result.append((x + dx, y + dy))
                    if target.player == Player.NULL:
                        result.append((x + dx, y + dy))

        if attacker.role is Role.PAWN:
            if attacker.player is Player.ONE:
                direction = 1
                x_start = 1
            else: # player is TWO
                direction = -1
                x_start = 6

            target = self.board[y][x+direction]
            if target.role is Role.NULL:
                result.append((x+direction, y))

            target = self.board[y+1][x+direction]
            if target.player not in [Player.NULL, self.active_player]:
                result.append((x+direction, y+1))

            target = self.board[y-1][x+direction]
            if target.player not in [Player.NULL, self.active_player]:
                result.append((x+direction, y-1))

            if x == x_start:
                result.append((x+2 * direction, y))

        return result

    def make_move(self):
        xa, ya = self.selected
        xd, yd = self.cursor

        self.board[yd][xd] = self.board[ya][xa]
        self.board[ya][xa]  = Piece(Role.NULL, Player.NULL)

        if self.active_player is Player.ONE:
            self.active_player = Player.TWO
        else:
            self.active_player = Player.ONE

        self.selected = None

    def __repr__(self) -> str:
        return "\n".join(
            "|".join(" " + self.config.role_symbol[piece.role] + " " for piece in row)
            for row in self.board
        )

    def __str__(self):
        row_strings = [
            ":      a   b   c   d   e   f   g   h  ",
            ":    +---+---+---+---+---+---+---+---+",
        ]

        for i in range(8):

            current_row = f":  {i} |"
            for j in range(8):

                # pick the tile color
                if (j, i) == self.cursor:
                    current_row += self.config.cursor_color
                elif (j, i) == self.selected:
                    current_row += self.config.selected_color
                elif self.selected and (j, i) in self.defending_coords(self.selected):
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
