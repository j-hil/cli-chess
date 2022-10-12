"""Contains the class representing the internal state of the game."""
import sys
from enum import Enum
from itertools import product
from colorama import Style

import jchess
from jchess.board import Board
from jchess.pieces import Piece, Player
from jchess.display import DisplayArray
from jchess.configs import VSC_CONFIG, Config
from jchess.geometry import Vector, VectorLike
from jchess.terminal import Action, get_user_action


class Mode(Enum):
    ONE = "single player"
    TWO = "online multi-player"
    THREE = "local multi-player"


class GameState:
    """Interface layer between the player and chess game."""

    def __init__(self, config: Config = VSC_CONFIG, board: Board | None = None):
        """Initialise a `GameState`.

        :param config: Controls settings such as color, symbols etc. Several pre-made
            configs available in jchess.config. Defaults to VSC_CONFIG
        """
        if board is None:
            self.board = Board()

        self.attacking_piece: Piece | None = None
        self.cursor_coord = Vector(4, 7)

        self.config = config
        self.mode = Mode.ONE

    def evolve_state(self) -> None:

        board = self.board
        action = get_user_action()

        if action in CARDINAL_DIRECTION:

            # account for fact that user's view is rotated from the internal view
            if self.mode is Mode.TWO:
                action = ROTATE.get(action, action)

            new_cursor_coord = self.cursor_coord + CARDINAL_DIRECTION[action]
            if board.has(new_cursor_coord):
                self.cursor_coord = new_cursor_coord

        elif action is Action.SELECT:
            attacker = self.attacking_piece
            cursor_piece = board[self.cursor_coord]
            if (
                attacker is None
                and cursor_piece is not None
                and cursor_piece.player is board.active_player
                and cursor_piece.targets != []
            ):
                self.attacking_piece = cursor_piece
            elif attacker is not None and self.cursor_coord in attacker.targets:
                board.process_attack(attacker, self.cursor_coord)
                self.attacking_piece = None

        elif action is Action.QUIT:
            sys.exit()

    def __str__(self) -> str:
        """Use the helper functions below to generate the main display of the game."""
        # TODO: generally clean

        game = self
        board = game.board

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
            DisplayArray(f"SCORE = {board.score(Player.ONE):0>3}"),
            DisplayArray("\n \n".join(col_labels)),
            DisplayArray("\n \n".join(col_labels)),
            DisplayArray(f"SCORE = {board.score(Player.TWO):0>3}"),
            _generate_taken_pieces(game, Player.ONE),
            _generate_taken_pieces(game, Player.TWO),
            DisplayArray("   ".join(row_labels)),
            DisplayArray(jchess.__version__[:11]),
            _generate_gutter(board),
            DisplayArray(f"by {jchess.__author__}"),
        )
        for display in display_elements:
            main_display.merge_in(display, anchor="@")

        return str(main_display)


# Defines the various on-screen elements generated from a `GameState`.
#
# Each display element is generated as a `DisplayArray` and then merged into the main
# display which will already display the pieces. There are the following elements:
# * Rank/file labels (4)
# * Player one/two titles, score and taken pieces (6)
# * Left, middle and right gutter messages (3)

def _generate_gutter(game: "Board") -> DisplayArray:

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
    board = game.board

    # fmt: off
    if game.mode is Mode.TWO:
        def coord_transform(v: VectorLike) -> Vector:
            return Vector(30 - 4 * v[1], 1 + 2 * v[0])
    else:
        def coord_transform(v: VectorLike) -> Vector:
            return Vector(29 + 4 * v[0], 5 + 2 * v[1])
    # fmt: on

    # TODO: wildly inefficient as now game.pieces replaces game.board
    # iterate over game.pieces instead
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
            back_color = game.config.valid_color
        elif show_actual_targets:
            back_color = game.config.valid_color
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
        display[display_position - (1, 0)] = back_color + fore_color + " "
        display[display_position] = symbol
        display[display_position + (1, 0)] = " " + Style.RESET_ALL


def _generate_taken_pieces(game: "GameState", player: Player) -> DisplayArray:
    board = game.board
    n_rows, n_cols = 4, 11
    display = DisplayArray("\n".join(" " * n_cols for _ in range(n_rows)))

    symbol = game.config.role_symbol
    back = game.config.board_color[player.value - 1]
    fore = game.config.player_color[Player.TWO if player is Player.ONE else Player.ONE]

    taken_pieces = board.taken_pieces[player]
    plain_string = ", ".join(symbol[role] for role in taken_pieces)
    plain_string = f"{plain_string: <48}"

    for i, j in product(range(n_rows), range(n_cols)):
        position = Vector(j, i)
        display[position] = back + fore + plain_string[n_cols * i + j] + Style.RESET_ALL
    return display


def _generate_player_header(game: "GameState", player: Player) -> DisplayArray:
    display = DisplayArray(f" Player {player.value}: ")
    display[0, 0] = game.config.board_color[2 - player.value] + display[0, 0]
    display[-1, 0] += Style.RESET_ALL
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


CARDINAL_DIRECTION = {
    Action.UP: (0, -1),
    Action.DOWN: (0, +1),
    Action.LEFT: (-1, 0),
    Action.RIGHT: (+1, 0),
}

ROTATE = {
    Action.UP: Action.LEFT,
    Action.DOWN: Action.RIGHT,
    Action.RIGHT: Action.UP,
    Action.LEFT: Action.DOWN,
}
