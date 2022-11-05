from dataclasses import dataclass

from jchess import __author__ as author
from jchess import __version__ as version
from jchess.configs import Pallet, SymbolDict
from jchess.game import PROMOTION_OPTIONS, Game, Mode, Status
from jchess.pieces import Player, Role
from jchess.terminal import ctrlseq


@dataclass(slots=True, frozen=True)
class Display:
    pallet: Pallet
    symbol: SymbolDict

    def ctrlseq(self, game: Game) -> str:
        pallet = self.pallet
        parts = []

        # adjust for previous status of GameState
        if game.status is not game.status_prev:
            if game.status_prev is Status.UNINITIALIZED:
                parts.append(ctrlseq(START_MENU_CLEAR, at=(1, 1)))
            elif game.status_prev is Status.START_MENU:
                parts.append(MAIN_DISPLAY_TEMPLATE)
                parts.append(ctrlseq(f"{version: ^11}", at=(3, 24)))
                parts.append(ctrlseq(f"by {author}", at=(76, 24)))
                for i, p in enumerate(Player):
                    parts.append(ctrlseq(ROW_LABELS, at=(30, 18 * i + 4)))
                    parts.append(ctrlseq(COL_LABELS, at=(36 * i + 26, 6)))
                    info = INFO_TEMPLATE.format("ONE" if i == 0 else "TWO")
                    parts.append(ctrlseq(info, clr=pallet.text[p], at=(72 * i + 3, 4)))
            elif game.status_prev is Status.PROMOTING:
                parts.append(ctrlseq(PROMOTION_CLEAR, at=(3, 12)))

        if game.status is Status.START_MENU:
            parts.append(ctrlseq(START_MENU_TEMPLATE, at=(0, 1)))
            mode_str = f"(+) {list(Mode)[game.scursor]}"
            parts.append(ctrlseq(mode_str, clr=pallet.cursor, at=(1, 3 + game.scursor)))

        elif game.status is Status.BOARD_FOCUS:
            parts.append(self.__gutter_msg(game))
            parts.append(self.__board_ctrlseq(game))
            for i, p in enumerate(Player):
                score = f"{game.board.score(p):0>3}"
                parts.append(ctrlseq(score, clr=pallet.text[p], at=(72 * i + 11, 6)))
                parts.append(self.__taken_ctrlseq(game, p))

        elif game.status is Status.PROMOTING:
            role = PROMOTION_OPTIONS[game.pcursor]
            color = self.pallet.cursor
            parts.append(ctrlseq(PROMOTION_TEMPLATE, at=(3, 12)))
            option_str = f"({role.symbol}) {role}"
            parts.append(ctrlseq(option_str, clr=color, at=(3, 14 + game.pcursor)))

        return "".join(parts)

    # Helper methods for `Display.ctrlseq` ------------------------------------------- #

    def __board_ctrlseq(self, game: Game) -> str:
        pallet = self.pallet
        board = game.board
        cursor = game.bcursor
        focus = game.board[cursor]
        attacker = game.attacker

        parts = []
        for coord, piece in board.items():
            highlight_potential_targets = (
                not attacker
                and focus
                and focus.player is board.active_player
                and coord in board.targets[cursor]
            )
            show_actual_targets = attacker and coord in board.targets[attacker.coord]

            if coord == game.bcursor:
                back = pallet.cursor
            elif game.attacker and coord == game.attacker.coord:
                back = pallet.focus
            elif highlight_potential_targets or show_actual_targets:
                back = pallet.target
            else:
                back = pallet.board[sum(coord) % 2]

            fore = pallet.piece[piece.player] if piece else ""
            square = f" {self.symbol[piece.role]} " if piece else "   "
            display_location = 29 + 4 * coord.x, 6 + 2 * coord.y
            parts.append(ctrlseq(square, clr=(back + fore), at=display_location))
        return "".join(parts)

    def __taken_ctrlseq(self, game: Game, player: Player) -> str:
        taken_pieces = game.board.taken_pieces[player]
        symbol = self.symbol
        color = self.pallet.text[player]

        parts = []
        for i in range(15):
            (role,) = taken_pieces[i : i + 1] or [Role.BLANK]
            s = symbol[role]

            parts.append(f" {s}")
            if i % 5 == 4:
                parts.append(" \n")

        return ctrlseq("".join(parts), clr=color, at=(72 * player.value - 69, 8))

    @staticmethod
    def __gutter_msg(game: Game) -> str:
        b = game.board
        s1, s2, turn = b.score(Player.ONE), b.score(Player.TWO), b.ply // 2 + 1
        if s1 > s2:
            msg = f"Turn {turn}. Player ONE leads by {s1 - s2} point(s)."
        if s2 > s1:
            msg = f"Turn {turn}. Player TWO leads by {s2 - s1} point(s)."
        else:
            msg = f"Turn {turn}. Players ONE & TWO are equal in score."
        return ctrlseq(f"{msg: ^55}", at=(17, 24))


# Printing templates ----------------------------------------------------------------- #
# fmt: off
START_MENU_TEMPLATE = """\
Pick a game mode:
=================
""" + "\n".join(f"(+) {m}" for m in Mode)
START_MENU_CLEAR = "".join(" " if c != "\n" else "\n" for c in START_MENU_TEMPLATE)

INFO_TEMPLATE = """\
Player {}:
===========
SCORE = 000\
"""

PROMOTION_TEMPLATE = """\
Promote to:
===========
""" + "\n".join(f"({r.symbol}) {r}" for r in PROMOTION_OPTIONS)
PROMOTION_CLEAR = "".join(" " if c != "\n" else "\n" for c in PROMOTION_TEMPLATE)

ROW_LABELS = "8   7   6   5   4   3   2   1"
COL_LABELS = "a\n \nb\n \nc\n \nd\n \ne\n \nf\n \ng\n \nh"
MAIN_DISPLAY_TEMPLATE = """\
+-------------------------------------------------------------------------------------+
| Welcome to J-Chess! Controls: arrows to navigate, space to select, and 'q' to quit. |
+-------------------------------------------------------------------------------------+
|             |                                                         |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
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
