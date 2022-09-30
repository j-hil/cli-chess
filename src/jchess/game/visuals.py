"""Defines the various on-screen elements generated from a `GameState`.

Each display element is generated as a `DisplayArray` and then merged into the main
display which will already display the pieces. There are the following elements:
* Rank/file labels (4)
* Player one/two titles, score and taken pieces (6)
* Left, middle and right gutter messages (3)
"""
# TODO: generally clean

from itertools import product
from typing import TYPE_CHECKING
from colorama import Style
import jchess

from jchess.display import DisplayArray, PrintableChar
from jchess.game.engine import UNSELECTED_COORD, Mode
from jchess.squares import Player
from jchess.geometry import Vector

if TYPE_CHECKING:
    from jchess.game.state import GameState


def generate_main_display(game: "GameState") -> DisplayArray:
    """Use the helper functions above to generate the main display of the game."""
    row_labels, col_labels = list("abcdefgh"), list("87654321")
    if game.mode is Mode.TWO:
        row_labels, col_labels = col_labels[::], row_labels

    main_display = DisplayArray(MAIN_DISPLAY_TEMPLATE)
    _add_pieces(game, main_display)

    display_elements = (
        # must be in correct order
        _generate_player_header(game, Player.ONE),
        DisplayArray("   ".join(row_labels)),
        _generate_player_header(game, Player.TWO),
        DisplayArray(f"SCORE = {game.score(Player.ONE)}"),
        DisplayArray("\n \n".join(col_labels)),
        DisplayArray("\n \n".join(col_labels)),
        DisplayArray(f"SCORE = {game.score(Player.TWO)}"),
        _generate_player_info(game, Player.ONE),
        _generate_player_info(game, Player.TWO),
        DisplayArray("   ".join(row_labels)),
        DisplayArray(jchess.__version__[:11]),
        _generate_gutter(game),
        DisplayArray(f"by {jchess.__author__}"),
    )
    for display in display_elements:
        main_display.merge_in(display, anchor="@")

    return main_display


def _generate_gutter(game: "GameState") -> DisplayArray:
    score1, score2 = game.score(Player.ONE), game.score(Player.TWO)
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
        gutter_msg = "PLAYERS ONE & TWO are equal in score; close game!"
    return DisplayArray(f"{gutter_msg: ^55}")


def _add_pieces(game: "GameState", display: DisplayArray) -> None:

    # fmt: off
    if game.mode is Mode.TWO:
        def coord_transform(v: Vector) -> Vector:
            return Vector(30 - 4 * v.y, 1 + 2 * v.x)
    else:
        def coord_transform(v: Vector) -> Vector:
            return Vector(29 + 4 * v.x, 5 + 2 * v.y)
    # fmt: on

    for i, row in enumerate(game.board):
        for j, square in enumerate(row):
            coord = Vector(j, i)

            show_highlighted_targets = (
                game.selected_coord is UNSELECTED_COORD
                and game.cursor.player is game.active_player()
                and coord in game.defending_coords(game.cursor_coord)
            )
            show_selected_targets = (
                game.selected_coord is not UNSELECTED_COORD
                and coord in game.defending_coords(game.selected_coord)
            )
            if coord == game.cursor_coord:
                back_color = game.config.cursor_color
            elif coord == game.selected_coord:
                back_color = game.config.highlight_color
            elif show_highlighted_targets:
                back_color = game.config.valid_color
            elif show_selected_targets:
                back_color = game.config.valid_color
            else:
                back_color = game.config.board_color[(i + j) % 2]

            fore_color = game.config.player_color[square.player]
            symbol = game.config.role_symbol[square.role]

            display_position = coord_transform(coord)
            display[display_position - (1, 0)].color = fore_color, back_color, ""
            display[display_position] = PrintableChar(symbol, fore_color, back_color)
            display[display_position + (1, 0)].color = fore_color, back_color, ""


def _generate_player_info(game: "GameState", player: Player) -> DisplayArray:
    n_rows, n_cols = 4, 11
    display = DisplayArray("\n".join(" " * n_cols for _ in range(n_rows)))

    taken_pieces = game.taken_pieces[player]
    symbol = game.config.role_symbol
    plain_string = ", ".join(symbol[role] for role in taken_pieces)
    plain_string = f"{plain_string: <48}"

    s = 0 if player is Player.ONE else 1
    for i, j in product(range(n_rows), range(n_cols)):
        position = Vector(j, i)
        display[position] = PrintableChar(
            plain_string[n_cols * i + j],
            fore=game.config.player_color[player],
            back=game.config.board_color[s],
        )
    return display


def _generate_player_header(game: "GameState", player: Player) -> DisplayArray:
    display = DisplayArray(f"{player}:")
    s = 0 if player is Player.ONE else 1
    for j in range(display.n_cols):
        display[j, 0].color = (
            game.config.player_color[player],
            game.config.board_color[s],
            "",
        )
    return display


# 25 * 87
MAIN_DISPLAY_TEMPLATE = """\
+-------------------------------------------------------------------------------------+
| Welcome to J-Chess! Controls: arrows to navigate, space to select, and 'q' to quit. |
+-------------------------------------------------------------------------------------+
| @           |              @                                          | @           |
+ - - - - - - +            +---+---+---+---+---+---+---+---+            + - - - - - - +
| @           |          @ |   |   |   |   |   |   |   |   | @          | @           |
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
|             |              @                                          |             |
+-------------+---------------------------------------------------------+-------------+
| @           | @                                                       | @           |
+-------------------------------------------------------------------------------------+\
"""
MAIN_DISPLAY_ROWS = len(MAIN_DISPLAY_TEMPLATE.split("\n"))
