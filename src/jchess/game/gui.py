"""Defines the various on-screen elements generated from a `GameState`

To call this a GUI is a little generous.
"""
from typing import TYPE_CHECKING
from colorama import Style

from jchess.display import DisplayArray
from jchess.squares import Player
from jchess.geometry import Vector
from jchess.constants import BOARD_TEMPLATE, PLAYER_INFO_TEMPLATE, MAIN_DISPLAY_SIZE

if TYPE_CHECKING:
    from jchess.game.state import GameState


def generate_main_display(game: "GameState") -> DisplayArray:
    """Use the helper functions above to generate the main display of the game."""
    board = generate_board(game)
    player1_info = generate_player_column(game, Player.ONE)
    player2_info = generate_player_column(game, Player.TWO)
    headline = DisplayArray(
        "Welcome to J-Chess. Use the arrow keys to navigate, "
        "space to select, and 'q' to quit."
    )
    gutter = generate_gutter(game)

    h, w = MAIN_DISPLAY_SIZE.rows, MAIN_DISPLAY_SIZE.cols
    blank_template = "\n".join(" " * w for _ in range(h))
    main_display = DisplayArray(blank_template)

    main_display.merge_in(headline, at=(0, 0))
    main_display.merge_in(player1_info, at=(0, 2))
    main_display.merge_in(board, at=(18, 2))
    main_display.merge_in(player2_info, at=(60, 2))
    main_display.merge_in(gutter, at=(0, 21))

    return main_display


def generate_gutter(game: "GameState") -> DisplayArray:
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

    return DisplayArray(gutter_msg)


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
