"""Functions to generate various on-screen elements from a `GameState`."""

from itertools import product

from jchess import __version__, __author__
from jchess.geometry import VectorLike
from jchess.board import Board
from jchess.pieces import Player
from jchess.state import GameState, Mode
from jchess.terminal import ctrlseq


def update(game: GameState) -> None:
    board = game.board
    config = game.config

    # Gutter message
    output = ctrlseq(_gutter_msg(board), at=(17, 24))

    # Score and taken pieces
    for i, p in enumerate(Player):
        output += ctrlseq(
            f"{board.score(p):0>3}",
            color=config.board_color[1 - i] + config.player_color[p],
            at=(72 * i + 11, 6),
        )
        output += _gen_taken_pieces(game, p)

    # Board
    output += _generate_pieces(game)

    print(output, end="")


def init(game: GameState) -> None:
    config = game.config
    output = (
        MAIN_DISPLAY_TEMPLATE
        + ctrlseq(f"{__version__[:11]: ^11}", at=(3, 24))
        + ctrlseq(f"by {__author__}", at=(76, 24))
    )

    if game.mode is Mode.TWO:
        row_labels = "   ".join(list("abcdefgh"))
        col_labels = "\n \n".join(list("87654321"))
    else:
        row_labels = "   ".join(list("87654321"))
        col_labels = "\n \n".join(list("abcdefgh"))

    # Board labels
    for i, p in enumerate(Player):
        output += (
            ctrlseq(row_labels, at=(30, 18 * i + 4))
            + ctrlseq(col_labels, at=(36 * i + 26, 6))
            + ctrlseq(
                f" Player {i+1}: \n===========\nSCORE = 000",
                color=config.board_color[1 - i] + config.player_color[p],
                at=(72 * i + 3, 4),
            )
        )

    print(output, end="")


def _generate_pieces(game: GameState) -> str:
    output = ""
    board = game.board

    if game.mode is Mode.TWO:

        # won't work at current
        def coord_transform(v: VectorLike) -> tuple[int, int]:
            return (30 - 4 * v[1], 1 + 2 * v[0])

    else:

        def coord_transform(v: VectorLike) -> tuple[int, int]:
            return (29 + 4 * v[0], 6 + 2 * v[1])

    # TODO: wildly inefficient as now game.pieces replaces game.board
    # iterate over game.pieces instead. also just entirely rework this function
    for i, j in product(range(8), repeat=2):
        coord = (j, i)

        cursor_piece = board[game.cursor_coord]
        highlight_potential_targets = (
            game.attacking_piece is None
            and cursor_piece is not None
            and cursor_piece.player is board.active_player
            and coord in cursor_piece.targets
        )
        show_actual_targets = (
            game.attacking_piece is not None and coord in game.attacking_piece.targets
        )
        if coord == game.cursor_coord:
            back_color = game.config.cursor_color
        elif game.attacking_piece is not None and coord == game.attacking_piece.coord:
            back_color = game.config.highlight_color
        elif highlight_potential_targets:
            back_color = game.config.target_color
        elif show_actual_targets:
            back_color = game.config.target_color
        else:
            back_color = game.config.board_color[(i + j) % 2]

        piece = board[coord]
        if piece is not None:
            fore_color = game.config.player_color[piece.player]
            symbol = game.config.role_symbol[piece.role]
        else:
            fore_color = ""
            symbol = " "

        display_position = coord_transform(coord)
        output += ctrlseq(
            f" {symbol} ", color=(back_color + fore_color), at=display_position
        )
    return output


def _gutter_msg(board: Board) -> str:
    score1, score2 = board.score(Player.ONE), board.score(Player.TWO)
    gutter_msg = f"Turn {board.ply // 2 + 1}. "
    if score1 > score2:
        gutter_msg += f"Player ONE leads by {score1 - score2} point(s)."
    elif score2 > score1:
        gutter_msg += f"Player TWO leads by {score2 - score1} point(s)."
    else:
        gutter_msg += "Players ONE & TWO are equal in score."
    return f"{gutter_msg: ^55}"


def _gen_taken_pieces(game: GameState, player: Player) -> str:
    taken_pieces = game.board.taken_pieces[player]
    symbol = game.config.role_symbol

    plain_str = ""
    for i in range(15):
        try:
            p = taken_pieces[i]
            s = symbol[p]
        except IndexError:
            s = " "

        if i % 5 == 4:
            plain_str += f" {s} \n"
        else:
            plain_str += f" {s}"

    back = game.config.board_color[player.value - 1]
    fore = game.config.player_color[Player.TWO if player is Player.ONE else Player.ONE]
    return ctrlseq(plain_str, color=(back + fore), at=(72 * (player.value - 1) + 3, 8))


# 25 * 87
MAIN_DISPLAY_TEMPLATE = """\
+-------------------------------------------------------------------------------------+
| Welcome to J-Chess! Controls: arrows to navigate, space to select, and 'q' to quit. |
+-------------------------------------------------------------------------------------+
|             |                                                         |             |
| =========== |            +---+---+---+---+---+---+---+---+            | =========== |
| SCORE =     |            |   |   |   |   |   |   |   |   |            | SCORE =     |
+-------------+            +---+---+---+---+---+---+---+---+            +-------------+
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
+-------------+            +---+---+---+---+---+---+---+---+            +-------------+
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |                                                         |             |
+-------------+---------------------------------------------------------+-------------+
|             |                                                         |             |
+-------------------------------------------------------------------------------------+\
"""
