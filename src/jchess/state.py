from cmath import pi
from pieces import Color, Piece, King, Queen, Bishop, Knight, Rook, Pawn
from colorama import Fore, Style, Back

BACK_ROW = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]


class GameState:
    def __init__(self):
        self.pieces: list[Piece] = [
            *[Piece((i, 7), Color.B) for Piece, i in zip(BACK_ROW, range(8))],
            *[Pawn((i, 6), Color.B) for i in range(8)],
            *[Pawn((i, 1), Color.W) for i in range(8)],
            *[Piece((i, 0), Color.W) for Piece, i in zip(BACK_ROW, range(8))],
        ]

    @property
    def board(self) -> list[list[Piece | None]]:
        result = [[None] * 8 for _ in range(8)]
        for piece in self.pieces:
            x, y = piece.coord
            result[x][y] = piece
        return result

    def __str__(self):
        row_strings = []

        row_strings.append(":      a   b   c   d   e   f   g   h  ")
        row_strings.append(":    +---+---+---+---+---+---+---+---+")

        for i in range(8):

            current_row = ""
            current_row += f":  {i} |"
            for j in range(8):
                piece = self.board[i][j]
                if (i + j) % 2 == 0:
                    square_color = Back.MAGENTA
                else:
                    square_color = Back.BLACK
                current_row += (
                    square_color
                    + ("   " if piece is None else f" {piece} ")
                    + Back.RESET
                    + "|"
                )

            current_row += f" {i}"

            row_strings.append(current_row)
            row_strings.append(":    +---+---+---+---+---+---+---+---+")

        row_strings.append(":      a   b   c   d   e   f   g   h  ")
        return "\n".join(row_strings)
