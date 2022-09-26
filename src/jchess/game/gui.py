"""Defines the various on-screen elements generated from a `GameState`

To call this a GUI is a little generous. This file in particular (and display itself)
are big targets for better implementation.
"""
from typing import TYPE_CHECKING
from colorama import Style

from jchess.display import DisplayArray, DisplaySize
from jchess.squares import Player
from jchess.geometry import Vector

if TYPE_CHECKING:
    from jchess.game.state import GameState


def generate_main_display(game: "GameState") -> DisplayArray:
    """Use the helper functions above to generate the main display of the game."""

    board = _generate_board(game)
    player1_info = _generate_player_info(game, Player.ONE)
    player2_info = _generate_player_info(game, Player.TWO)
    gutter = _generate_gutter(game)

    main_display = DisplayArray(MAIN_DISPLAY_TEMPLATE)

    main_display.merge_in(player1_info, at=(0, 3))
    main_display.merge_in(board, at=(23, 3))
    main_display.merge_in(player2_info, at=(72, 3))
    main_display.merge_in(gutter, at=(2, 23))

    return main_display


def _generate_gutter(game: "GameState") -> DisplayArray:
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

    return DisplayArray(f"{gutter_msg: ^83}")


def _generate_board(game: "GameState") -> DisplayArray:
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


def _generate_player_info(game: "GameState", player: Player) -> DisplayArray:
    score = game.score[player]
    display = DisplayArray(PLAYER_INFO_TEMPLATE.format(player.value, score))

    taken_pieces = game.taken_pieces[player]
    symbol = game.config.role_symbol
    plain_string = ", ".join(symbol[p.role] for p in taken_pieces)
    plain_string = f"{plain_string: <48}"

    # TODO: remove all magic numbers in this file... :/ eg those 4's aren't the same
    for i in range(4):
        for j in range(12):
            position = Vector(2 + j, i + 4)
            display[position] = plain_string[12 * i + j]
    return display


# 25 * 87
MAIN_DISPLAY_TEMPLATE = """\
+-------------------------------------------------------------------------------------+
| Welcome to J-Chess! Controls: arrows to navigate, space to select, and 'q' to quit. |
+-------------------------------------------------------------------------------------+
| PLAYER ONE: |              a   b   c   d   e   f   g   h              | PLAYER TWO: |
+ - - - - - - +            +---+---+---+---+---+---+---+---+            + - - - - - - +
| SCORE = NNN |          0 |   |   |   |   |   |   |   |   | 0          | SCORE = NNN |
+ - - - - - - +            +---+---+---+---+---+---+---+---+            + - - - - - - +
| X, X, X, X, |          1 |   |   |   |   |   |   |   |   | 1          | X, X, X, X, |
| X, X, X, X, |            +---+---+---+---+---+---+---+---+            | X, X, X, X, |
| X, X, X, X, |          2 |   |   |   |   |   |   |   |   | 2          | X, X, X, X, |
| X, X, X, X, |            +---+---+---+---+---+---+---+---+            | X, X, X, X, |
+ - - - - - - +          3 |   |   |   |   |   |   |   |   | 3          + - - - - - - +
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |          4 |   |   |   |   |   |   |   |   | 4          |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |          5 |   |   |   |   |   |   |   |   | 5          |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |          6 |   |   |   |   |   |   |   |   | 6          |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |          7 |   |   |   |   |   |   |   |   | 7          |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |              a   b   c   d   e   f   g   h              | (by j-hil.) |
+-------------+---------------------------------------------------------+-------------+
| Gutter message.                                                                     |
+-------------------------------------------------------------------------------------+\
"""

# TODO: can probably remove
_LINES = MAIN_DISPLAY_TEMPLATE.split("\n")
MAIN_DISPLAY_SIZE = DisplaySize(len(_LINES), len(_LINES[0]))

# 19 x 39
BOARD_TEMPLATE = (
    "     a   b   c   d   e   f   g   h     \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 0 |   |   |   |   |   |   |   |   | 0 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 1 |   |   |   |   |   |   |   |   | 1 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 2 |   |   |   |   |   |   |   |   | 2 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 3 |   |   |   |   |   |   |   |   | 3 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 4 |   |   |   |   |   |   |   |   | 4 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 5 |   |   |   |   |   |   |   |   | 5 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 6 |   |   |   |   |   |   |   |   | 6 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    " 7 |   |   |   |   |   |   |   |   | 7 \n"
    "   +---+---+---+---+---+---+---+---+   \n"
    "     a   b   c   d   e   f   g   h     "
)

# 8 x 15
PLAYER_INFO_TEMPLATE = """\
| PLAYER {: <3}: |
+ - - - - - - +
| SCORE = {:0>3} |
+ - - - - - - +
| X, X, X, X, |
| X, X, X, X, |
| X, X, X, X, |
| X, X, X, X, |\
"""
