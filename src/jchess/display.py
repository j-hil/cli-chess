"""Printing `GameState` information.

Contains helper functions to:
* process `GameState` information into readable & pretty strings. In principle these
could be methods but it's convenient to have them here.
* combine said strings according to desired relative positions

I think a lot of the manipulations of the display could probably be simplified with the
built in `curses` module which I was unaware of when I begin this project.
"""

from dataclasses import dataclass
import os
from typing import TYPE_CHECKING, Iterator

from colorama import Style

from jchess.geometry import Vector, VectorLike
from jchess.squares import Player
from jchess.constants import BOARD_TEMPLATE, PLAYER_INFO_TEMPLATE

if TYPE_CHECKING:
    from jchess.state import GameState


@dataclass
class DisplaySize:
    """Used to measure the size of a display."""

    rows: int
    cols: int

    def __iter__(self) -> Iterator[int]:
        return iter([self.rows, self.cols])


MAIN_DISPLAY_SIZE = DisplaySize(25, 88)


class DisplayArray:
    """An array of arrays of strings, but the strings should be a single printable char.

    Designed to work with `Vector` and have mutable elements. Length of strings not
    enforced.
    """

    def __init__(self, string: str):
        """Initialize a `DisplayArray`.

        :param string: Each line becomes a row, and each character in a line becomes an
            element of it's corresponding row.
        :raises ValueError: Each line must be of equal length.
        """
        n_rows = 0
        row_len = string.find("\n")
        row_len = row_len if row_len > 0 else len(string)
        rows = []
        for row in string.split("\n"):
            if len(row) != row_len:
                raise ValueError("Each line in `string` must be of equal length.")
            n_rows += 1
            rows.append(list(row))

        self.array = rows
        self.size = DisplaySize(n_rows, row_len)

    def __getitem__(self, position: VectorLike) -> str:
        if isinstance(position, tuple):
            return self.array[position[1]][position[0]]
        return self.array[position.y][position.x]

    def __setitem__(self, position: Vector, value: str) -> None:
        self.array[position.y][position.x] = value

    def __str__(self) -> str:
        return "\n".join("".join(c for c in row) for row in self.array)

    def merge_in(self, other: "DisplayArray", *, at: VectorLike) -> None:
        """Merge another `DisplayArray` into this one.

        :param other: Display to merge into the current one
        :param at: Coordinate to start the merge at (top-left corner)
        :raises ValueError: If `other` display doesn't fit inside `self` from `at`
        """
        translation = Vector(*at) if isinstance(at, tuple) else at

        w, h = self.size.cols - translation.x, self.size.cols - translation.y
        if w < other.size.cols or h < other.size.rows:
            raise ValueError("The incoming display must fit in the allocated space")

        for i in range(other.size.rows):
            for j in range(other.size.cols):
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

    taken_pieces = game.taken_pieces[player]
    symbol = game.config.role_symbol
    plain_string = ", ".join(symbol[p.role] for p in taken_pieces)
    plain_string = f"{plain_string: <48}"

    for i in range(3):
        for j in range(16):
            position = Vector(j, i + 3)
            display[position] = plain_string[16 * i + j]
    return display


def generate_main_display(game: "GameState") -> DisplayArray:
    """Use the helper functions above to generate the main display of the game."""
    board = generate_board(game)
    player1_info = generate_player_column(game, Player.ONE)
    player2_info = generate_player_column(game, Player.TWO)
    headline = DisplayArray(
        "Welcome to J-Chess. Use the arrow keys to navigate, "
        "space to select, and 'q' to quit."
    )

    score1 = game.score[Player.ONE]
    score2 = game.score[Player.TWO]
    if score1 > 104:
        gutter_msg = f"PLAYER ONE wins with an effective score of {score1 - 104}!"
    elif score1 > score2:
        gutter_msg = f"PLAYER ONE leads by {score1 - score2} point(s)."
    elif score2 > 104:
        gutter_msg = f"PLAYER TWO wins with an effective score of {score2 - 104}!"
    elif score2 > score1:
        gutter_msg = f"PLAYER TWO leads by {score2 - score1} point(s)."
    elif score1 == score2 == 0:
        gutter_msg = "Start playing!"
    else:
        gutter_msg = "This game is close! PLAYERS ONE & TWO are equal in score."

    gutter = DisplayArray(gutter_msg)

    h, w = MAIN_DISPLAY_SIZE
    blank_template = "\n".join(" " * w for _ in range(h))
    main_display = DisplayArray(blank_template)

    main_display.merge_in(headline, at=(0, 0))
    main_display.merge_in(player1_info, at=(0, 2))
    main_display.merge_in(board, at=(18, 2))
    main_display.merge_in(player2_info, at=(60, 2))
    main_display.merge_in(gutter, at=(0, 21))

    return main_display


if __name__ == "__main__":
    my_display = DisplayArray(BOARD_TEMPLATE)

    x, y = 1, 2
    my_display[Vector(5 + 4 * x, 2 + 2 * y)] = "X"

    print(my_display)

    os.system("cls")

    for x in MAIN_DISPLAY_SIZE:
        print(x)
