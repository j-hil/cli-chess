"""Defines the various on-screen elements generated from a `GameState`.

To call this a GUI is a little generous. This file in particular (and display itself)
are big targets for better implementation.
"""
# TODO: generally clean

from typing import TYPE_CHECKING
from colorama import Style

from jchess.display import DisplayArray
from jchess.game.engine import Mode
from jchess.squares import Player
from jchess.geometry import Vector

if TYPE_CHECKING:
    from jchess.game.state import GameState


def generate_main_display(game: "GameState") -> DisplayArray:
    """Use the helper functions above to generate the main display of the game."""
    row_labels, col_labels = list("abcdefgh"), list("87654321")
    if game.mode is Mode.TWO:
        row_labels, col_labels = col_labels[::], row_labels

    # fmt: off
    main_display = DisplayArray(MAIN_DISPLAY_TEMPLATE.format(
        "   ".join(row_labels), game.score(Player.ONE),
        "temp solution for line-to-long", game.score(Player.TWO),
        "   ".join(row_labels), "v0.0.1", _generate_gutter_str(game), "by j-hil"
    ))
    # fmt: on

    player_one = DisplayArray("PLAYER ONE:")
    player_one[0, 0] = game.config.board_color[0] + player_one[0, 0]
    player_one[-1, 0] += Style.RESET_ALL
    player_two = DisplayArray("PLAYER TWO:")
    player_two[0, 0] = game.config.board_color[1] + player_two[0, 0]
    player_two[-1, 0] += Style.RESET_ALL
    display_elements = (
        player_one,
        player_two,
        _generate_board(game),
        DisplayArray("\n \n".join(col_labels)),
        DisplayArray("\n \n".join(col_labels)),
        _generate_player_info(game, Player.ONE),
        _generate_player_info(game, Player.TWO),
    )

    for display in display_elements:
        main_display.merge_in(display, anchor="@")
    return main_display


def _generate_gutter_str(game: "GameState") -> str:
    score1 = game.score(Player.ONE)
    score2 = game.score(Player.TWO)
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

    return f"{gutter_msg: ^55}"


def _generate_board(game: "GameState") -> DisplayArray:
    display = DisplayArray(BOARD_TEMPLATE)

    # fmt: off
    if game.mode is Mode.TWO:
        def coord_transform(v: Vector) -> Vector:
            return Vector(30 - 4 * v.y, 1 + 2 * v.x)
    else:
        def coord_transform(v: Vector) -> Vector:
            return Vector(2 + 4 * v.x, 1 + 2 * v.y)
    # fmt: on

    for i, row in enumerate(game.board):
        for j, square in enumerate(row):
            board_position = Vector(j, i)

            if board_position == game.highlighted_coord:
                back_color = game.config.cursor_color
            elif board_position == game.selected_coord:
                back_color = game.config.highlight_color
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
    n_rows, n_cols = 4, 11
    display = DisplayArray("\n".join(" " * n_cols for _ in range(n_rows)))

    taken_pieces = game.taken_pieces[player]
    symbol = game.config.role_symbol
    plain_string = ", ".join(symbol[role] for role in taken_pieces)
    plain_string = f"{plain_string: <48}"

    s = 0 if player is Player.ONE else 1
    for i in range(n_rows):
        for j in range(n_cols):
            position = Vector(j, i)
            display[position] = (
                game.config.board_color[s]
                + plain_string[n_cols * i + j]
                + Style.RESET_ALL
            )
    return display


# 25 * 87
MAIN_DISPLAY_TEMPLATE = """\
+-------------------------------------------------------------------------------------+
| Welcome to J-Chess! Controls: arrows to navigate, space to select, and 'q' to quit. |
+-------------------------------------------------------------------------------------+
| @           |              {: ^29}              | @           |
+ - - - - - - +            @---+---+---+---+---+---+---+---+            + - - - - - - +
| SCORE = {:0>3} |          @ {: ^33} @          | SCORE = {:0>3} |
+ - - - - - - +            +---+---+---+---+---+---+---+---+            + - - - - - - +
| @           |            |   |   |   |   |   |   |   |   |            | @           |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
+ - - - - - - +            |   |   |   |   |   |   |   |   |            + - - - - - - +
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |              {: ^29}              |             |
+-------------+---------------------------------------------------------+-------------+
| {: ^11} | {: ^55} | {: ^11} |
+-------------------------------------------------------------------------------------+\
"""
MAIN_DISPLAY_ROWS = len(MAIN_DISPLAY_TEMPLATE.split("\n"))

# 19 x 39
BOARD_TEMPLATE = """\
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+\
"""
