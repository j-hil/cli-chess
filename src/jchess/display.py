"""Printing `GameState` information.

Contains helper functions to:
* process `GameState` information into readable & pretty strings. In principle these
could be methods but it's convenient to have them here.
* combine said strings according to desired relative positions
"""
from typing import TYPE_CHECKING
from colorama import Style
from jchess.geometry import Vector
from jchess.constants import DISPLAY_TEMPLATE

if TYPE_CHECKING:
    from jchess.state import GameState


class DisplayArray:
    """An array of arrays of strings. Designed to work with `Vector` and be mutable."""

    def __init__(self, string: str):
        self.array = [list(row) for row in string.split("\n")]

    def __getitem__(self, position: Vector) -> str:
        return self.array[position.y][position.x]

    def __setitem__(self, position: Vector, value: str):
        self.array[position.y][position.x] = value

    def __str__(self):
        return "\n".join("".join(c for c in row) for row in self.array)


def generate_board(game: "GameState") -> str:
    """Create a string representing the inputted `GameState`."""
    display = DisplayArray(DISPLAY_TEMPLATE)

    def coord_transform(v: Vector) -> Vector:
        return Vector(5 + 4 * v.x, 2 + 2 * v.y)

    for i, row in enumerate(game.board):
        for j, square in enumerate(row):
            board_position = Vector(j, i)

            if board_position == game.highlighted_coord:
                back_color = game.config.cursor_color
            elif board_position == game.selected_coord:
                back_color = game.config.selected_color
            elif game.is_defending(board_position):
                back_color = game.config.valid_color
            else:
                back_color = game.config.board_color[(i + j) % 2]

            fore_color = game.config.player_color[square.player]
            symbol = game.config.role_symbol[square.role]

            display_position = coord_transform(board_position)
            display[display_position - (1, 0)] = back_color + fore_color + " "
            display[display_position] = symbol
            display[display_position + (1, 0)] = " " + Style.RESET_ALL

    return str(display)

def generate_player_column(game: "GameState"):
    """Create a string representing the extra info to resent to the player."""

if __name__ == "__main__":
    my_display = DisplayArray(DISPLAY_TEMPLATE)

    x, y = 1, 2
    my_display[Vector(5 + 4 * x, 2 + 2 * y)] = "X"

    print(my_display)
