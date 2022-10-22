from itertools import product
from typing import TYPE_CHECKING

from jchess import __author__ as author, __version__ as version
from jchess.board import Board
from jchess.pieces import Player
from jchess.geometry import VectorLike
from jchess.terminal import ctrlseq

if TYPE_CHECKING:
    from jchess.state._state import GameState

# TODO:
#  * _gen_pieces: wildly inefficient as now game.pieces replaces game.board
#  iterate over game.pieces instead. also just entirely rework this function
#  * should go over this, pdisplay and config with a fine comb


def update(game: "GameState") -> str:
    config = game.config
    board = game.board

    output = ctrlseq(_gutter_msg(board), at=(17, 24)) + _generate_pieces(game)
    for i, p in enumerate(Player):
        output += ctrlseq(
            f"{board.score(p):0>3}",
            color=config.board_color[1 - i] + config.player_color[p],
            at=(72 * i + 11, 6),
        )
        output += _gen_taken_pieces(game, p)
    return output


def init(game: "GameState") -> str:
    config = game.config
    row_labels = "   ".join(list("87654321"))
    col_labels = "\n \n".join(list("abcdefgh"))

    output = (
        MAIN_DISPLAY_TEMPLATE
        + ctrlseq(f"{version[:11]: ^11}", at=(3, 24))
        + ctrlseq(f"by {author}", at=(76, 24))
    )
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
    return output


def _generate_pieces(game: "GameState") -> str:
    output = ""
    board = game.board

    def coord_transform(v: VectorLike) -> tuple[int, int]:
        return (29 + 4 * v[0], 6 + 2 * v[1])

    for i, j in product(range(8), repeat=2):
        coord = (j, i)

        cursor_piece = board[game.cursor_b]
        highlight_potential_targets = (
            game.attacker is None
            and cursor_piece is not None
            and cursor_piece.player is board.player
            and coord in cursor_piece.targets
        )
        show_actual_targets = (
            game.attacker is not None and coord in game.attacker.targets
        )
        if coord == game.cursor_b:
            back_color = game.config.cursor_color
        elif game.attacker is not None and coord == game.attacker.coord:
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


def _gen_taken_pieces(game: "GameState", player: Player) -> str:
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
