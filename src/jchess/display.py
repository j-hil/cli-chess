from itertools import product

from jchess import __author__ as author
from jchess import __version__ as version
from jchess.board import Board
from jchess.configs import Pallet, SymbolDict
from jchess.geometry import VectorLike
from jchess.pieces import Player
from jchess.state import PROMOTION_OPTIONS, GameState, Mode, Status
from jchess.terminal import ctrlseq

# TODO:
#  * _gen_pieces: wildly inefficient as now game.pieces replaces game.board
#  iterate over game.pieces instead. also just entirely rework this function
#  * should go over this, pdisplay and config with a fine comb


class Display:
    def __init__(self, pallet: Pallet, symbols: SymbolDict) -> None:
        self.pallet = pallet
        self.symbol = symbols

    def ctrlseq(self, game: GameState) -> str:
        pallet = self.pallet
        parts = []

        # adjust for previous status of GameState
        if game.status is not game.status_prev:
            if game.status_prev is Status.UNINITIALIZED:
                parts.append(ctrlseq(START_MENU_CLEAR, at=(1, 1)))
            elif game.status_prev is Status.START_MENU:
                parts.append(MAIN_DISPLAY_TEMPLATE)
                parts.append(ctrlseq(f"{version[:11]: ^11}", at=(3, 24)))
                parts.append(ctrlseq(f"by {author}", at=(76, 2)))

                for i, p in enumerate(Player):
                    parts.append(ctrlseq(ROW_LABELS, at=(30, 18 * i + 4)))
                    parts.append(ctrlseq(COL_LABELS, at=(36 * i + 26, 6)))
                    info = INFO_TEMPLATE.format(i + 1)
                    parts.append(ctrlseq(info, clr=pallet.text[p], at=(72 * i + 3, 4)))
            elif game.status_prev is Status.PROMOTING:
                parts.append(ctrlseq(PROMOTION_CLEAR, at=(3, 12)))

        if game.status is Status.START_MENU:
            mode = list(Mode)[game.scursor]
            parts.append(ctrlseq(START_MENU_TEMPLATE, at=(1, 1)))
            mode_str = f"(+) {mode}"
            parts.append(ctrlseq(mode_str, clr=pallet.cursor, at=(1, 3 + game.scursor)))

        elif game.status is Status.BOARD_FOCUS:
            board = game.board

            parts.append(ctrlseq(f"{gutter_msg(board): ^55}", at=(17, 24)))
            parts.append(self.gen_board(game))
            for i, p in enumerate(Player):
                score = f"{board.score(p):0>3}"
                parts.append(ctrlseq(score, clr=pallet.text[p], at=(72 * i + 11, 6)))
                parts.append(self.gen_taken(game, p))

        elif game.status is Status.PROMOTING:
            role = PROMOTION_OPTIONS[game.pcursor]
            color = self.pallet.cursor
            parts.append(ctrlseq(PROMOTION_TEMPLATE, at=(3, 12)))
            option_str = f"({role.symbol}) {role}"
            parts.append(ctrlseq(option_str, clr=color, at=(3, 14 + game.pcursor)))

        return "".join(parts)

    def gen_board(self, game: GameState) -> str:
        output = ""
        board = game.board
        pallet = self.pallet

        def coord_transform(v: VectorLike) -> tuple[int, int]:
            return (29 + 4 * v[0], 6 + 2 * v[1])

        for coord in product(range(8), range(8)):

            cursor_piece = board[game.bcursor]
            highlight_potential_targets = (
                game.attacker is None
                and cursor_piece is not None
                and cursor_piece.player is board.active_player
                and coord in cursor_piece.targets
            )
            show_actual_targets = (
                game.attacker is not None and coord in game.attacker.targets
            )
            if coord == game.bcursor:
                back = pallet.cursor
            elif game.attacker is not None and coord == game.attacker.coord:
                back = pallet.focus
            elif highlight_potential_targets or show_actual_targets:
                back = pallet.target
            else:
                back = pallet.board[sum(coord) % 2]

            piece = board[coord]
            if piece is not None:
                fore = pallet.piece[piece.player]
                symbol = self.symbol[piece.role]
            else:
                fore = ""
                symbol = " "

            display_position = coord_transform(coord)
            output += ctrlseq(f" {symbol} ", clr=(back + fore), at=display_position)
        return output

    def gen_taken(self, game: GameState, player: Player) -> str:
        taken_pieces = game.board.taken_pieces[player]
        symbol = self.symbol
        color = self.pallet.text[player]

        parts = []
        for i in range(15):
            try:
                p = taken_pieces[i]
                s = symbol[p]
            except IndexError:
                s = " "

            parts.append(f" {s}")
            if i % 5 == 4:
                parts.append(" \n")

        return ctrlseq("".join(parts), clr=color, at=(72 * player.value - 69, 8))


def gutter_msg(board: Board) -> str:
    s1, s2, turn = board.score(Player.ONE), board.score(Player.TWO), board.ply // 2 + 1
    if s1 > s2:
        return f"Turn {turn}. Player ONE leads by {s1 - s2} point(s)."
    if s2 > s1:
        return f"Turn {turn}. Player TWO leads by {s2 - s1} point(s)."
    return f"Turn {turn}. Players ONE & TWO are equal in score."


_TITLE = "Pick a game mode:"
START_MENU_TEMPLATE = "\n".join([_TITLE, "=" * 17] + [f"(+) {mode}" for mode in Mode])
START_MENU_CLEAR = "".join(" " if c != "\n" else "\n" for c in START_MENU_TEMPLATE)
INFO_TEMPLATE = "\n".join([" Player {}: ", "===========", "SCORE = 000"])
PROMOTION_TEMPLATE = "\n".join(
    ["Promote to:", "=" * 11] + [f"({r.symbol}) {r}" for r in PROMOTION_OPTIONS]
)
PROMOTION_CLEAR = "".join(" " if c != "\n" else "\n" for c in PROMOTION_TEMPLATE)
ROW_LABELS = "   ".join(list("87654321"))
COL_LABELS = "\n \n".join(list("abcdefgh"))
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
