from dataclasses import dataclass
# from config import Config, VS_CODE_CONFIG
from pieces import Player, Piece, King, Queen, Bishop, Knight, Rook, Pawn
from colorama import Fore, Style, Back

BACK_ROW = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]


class GameState:

    def __init__(self): #, config: Config = VS_CODE_CONFIG):

        self.pieces: list[Piece] = (
            [Piece((7, i), Player.TWO) for i, Piece in enumerate(BACK_ROW)]
            + [Pawn((6, i), Player.TWO) for i in range(8)]
            + [Pawn((1, i), Player.ONE) for i in range(8)]
            + [Piece((0, i), Player.ONE) for i, Piece in enumerate(BACK_ROW)]
        )

        #self.config = config
        self.cursor: tuple[int, int] = (4, 5)
        self.selected: tuple[int, int] | None = None
        self.active_player = Player.ONE

    @property
    def board(self) -> list[list[Piece | None]]:
        result = [[None] * 8 for _ in range(8)]
        for piece in self.pieces:
            x, y = piece.coord
            result[y][x] = piece
        return result

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
        elif self.active_player is Player.TWO:
            self.active_player = Player.ONE
        else:
            raise RuntimeError("You shouldn't be here...")


    def __str__(self):
        row_strings = [Style.BRIGHT]

        row_strings.append(":      a   b   c   d   e   f   g   h  ")
        row_strings.append(":    +---+---+---+---+---+---+---+---+")

        for i in range(8):

            current_row = ""
            current_row += f":  {i} |"
            for j in range(8):

                # TODO: This is gross - maybe use (-1, -1) as a "None" surrogate
                if self.selected is not None:
                    x, y = self.selected

                # pick the tile color
                if (j, i) == self.cursor:
                    current_row += Back.YELLOW
                elif self.selected is not None and (j, i) == (x, y):
                    current_row += Back.RED
                elif self.selected is not None and (j, i) in self.board[y][x].accessible_coords(self):
                    current_row += Back.GREEN
                elif (i+j) % 2 == 0:
                    current_row += Back.MAGENTA
                else:
                    current_row += Back.BLACK

                # TODO: this would be cleaner with a "Null" piece and a config
                piece = self.board[i][j]
                if piece is None:
                    current_row += "   "
                elif piece.player is Player.ONE:
                    current_row += Fore.WHITE + f" {piece} " + Fore.RESET
                elif piece.player is Player.TWO:
                    current_row += Fore.BLACK + f" {piece} " + Fore.RESET

                current_row += (Back.RESET + "|")
            current_row += f" {i}"

            row_strings.append(current_row)
            row_strings.append(":    +---+---+---+---+---+---+---+---+")

        row_strings.append(":      a   b   c   d   e   f   g   h  ")
        row_strings.append(Style.NORMAL)
        return "\n".join(row_strings)
