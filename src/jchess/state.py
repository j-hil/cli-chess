from colorama import Fore, Style, Back

from jchess.pieces import Player, Piece, Null, King, Queen, Bishop, Knight, Rook, Pawn
from jchess.configs import Config, VS_CODE_CONFIG

BACK_ROW = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]


class GameState:
    def __init__(self, config: Config = VS_CODE_CONFIG):

        self.pieces: list[Piece] = (
            [Piece((7, i), Player.TWO) for i, Piece in enumerate(BACK_ROW)]
            + [Pawn((6, i), Player.TWO) for i in range(8)]
            + [Pawn((1, i), Player.ONE) for i in range(8)]
            + [Piece((0, i), Player.ONE) for i, Piece in enumerate(BACK_ROW)]
        )
        self.config = config

        self.cursor = (4, 4)
        self.selected: tuple[int, int] | None = None
        self.active_player = Player.ONE

    @property
    def board(self) -> list[list[Piece | None]]:
        result = [[Null((x, y), Player.NULL) for y in range(8)] for x in range(8)]
        for piece in self.pieces:
            x, y = piece.coord
            result[y][x] = piece
        return result

    def remove(self, piece: Piece):
        if isinstance(piece, Null):
            return
        self.pieces.remove(piece)

    def valid_selection(self):
        x, y = self.cursor
        piece = self.board[y][x]
        return (
            piece is not None
            and piece.accessible_coords(self)
            and piece.player == self.active_player
        )

    def valid_move(self):
        x, y = self.selected
        piece = self.board[y][x]
        return self.cursor in piece.accessible_coords(self)

    def swap_player(self):
        if self.active_player is Player.ONE:
            self.active_player = Player.TWO
        else:
            self.active_player = Player.ONE

    def __str__(self):
        row_strings = [
            ":      a   b   c   d   e   f   g   h  ",
            ":    +---+---+---+---+---+---+---+---+",
        ]

        for i in range(8):

            current_row = f":  {i} |"
            for j in range(8):

                # TODO: This is gross - maybe use (-1, -1) as a "None" surrogate
                if self.selected is not None:
                    x, y = self.selected

                # pick the tile color
                if (j, i) == self.cursor:
                    current_row += self.config.cursor_color
                elif self.selected is not None and (j, i) == (x, y):
                    current_row += self.config.selected_color
                elif self.selected is not None and (j, i) in self.board[y][x].accessible_coords(self):
                    current_row += self.config.valid_color
                else:
                    current_row += self.config.board_color[(i + j) % 2]

                piece = self.board[i][j]  # TODO: should this not be [j][i] ...?
                fore_color = self.config.player_color[piece.player]
                current_row += fore_color + f" {piece} " + Style.RESET_ALL + "|"
            current_row += f" {i}"

            row_strings.append(current_row)
            row_strings.append(":    +---+---+---+---+---+---+---+---+")

        row_strings.append(":      a   b   c   d   e   f   g   h  ")
        row_strings.append(Style.NORMAL)
        return "\n".join(row_strings)
