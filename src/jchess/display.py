"""Printing `GameState` information.

Contains helper functions to:
* process `GameState` information into readable & pretty strings. In principle these
could be methods but it's convenient to have them here.
* combine said strings according to desired relative positions

I think a lot of the manipulations of the display could probably be simplified with the
built in `curses` module which I was unaware of when I begin this project.
"""

import os
from typing import TYPE_CHECKING

from colorama import Style

from jchess.geometry import Vector, VectorLike
from jchess.constants import BOARD_TEMPLATE, PIECE_VALUE, PLAYER_INFO_TEMPLATE
from jchess.squares import Player

if TYPE_CHECKING:
    from jchess.state import GameState


class DisplayArray:
    """An array of arrays of strings, but the strings should be a single printable char.

    Designed to work with `Vector` and have mutable elements. Length of strings not
    enforced.
    """

    def __init__(self, string: str):
        n_rows = 0
        row_len = string.find("\n")
        rows = []
        for row in string.split("\n"):
            if len(row) != row_len:
                raise ValueError("Each line in `string` must be of equal length.")
            n_rows += 1
            rows.append(list(row))

        self.array = rows
        self.width = row_len
        self.height = n_rows

    def __getitem__(self, position: VectorLike) -> str:
        if isinstance(position, tuple):
            return self.array[position[1]][position[0]]
        return self.array[position.y][position.x]

    def __setitem__(self, position: Vector, value: str):
        self.array[position.y][position.x] = value

    def __str__(self):
        return "\n".join("".join(c for c in row) for row in self.array)

    def merge_in(self, other: "DisplayArray", *, at: VectorLike):
        translation = Vector(*at) if isinstance(at, tuple) else at

        w, h = self.width - translation.x, self.height - translation.y
        if w < other.width or h < other.height:
            raise ValueError("The incoming display must fit in the allocated space")

        for i in range(other.height):
            for j in range(other.width):
                old_position = Vector(j, i)
                new_position = old_position + translation
                self[new_position] = other[old_position]


def generate_board(game: "GameState") -> DisplayArray:
    """Create a string representing the inputted `GameState`."""
    display = DisplayArray(BOARD_TEMPLATE)

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

    return display


def generate_player_column(game: "GameState", player: Player) -> DisplayArray:
    """Create a string representing the extra info to present to the player."""

    score = game.score[player]
    display = DisplayArray(PLAYER_INFO_TEMPLATE.format(player.value, score))

    taken_pieces = sorted(
        game.taken_pieces[player], key=lambda p: PIECE_VALUE[p.role], reverse=True
    )
    symbol = game.config.role_symbol
    plain_string = ", ".join(symbol[p.role] for p in taken_pieces)
    plain_string = f"{plain_string: <48}"

    for i in range(3):
        for j in range(16):
            position = Vector(j, i + 3)
            display[position] = plain_string[16 * i + j]
    display
    return display


def generate_main_display(game: "GameState") -> DisplayArray:
    """Use the helper functions above to generate the main display of the game."""

    board_display = generate_board(game)
    player1_display = generate_player_column(game, Player.ONE)
    player2_display = generate_player_column(game, Player.TWO)

    blank_template = "\n".join(" " * 88 for _ in range(21))
    main_display = DisplayArray(blank_template)

    main_display.merge_in(player1_display, at=(0, 0))
    main_display.merge_in(board_display, at=(18, 0))
    main_display.merge_in(player2_display, at=(60, 0))

    return main_display


if __name__ == "__main__":
    my_display = DisplayArray(BOARD_TEMPLATE)

    x, y = 1, 2
    my_display[Vector(5 + 4 * x, 2 + 2 * y)] = "X"

    print(my_display)

    os.system("cls")
