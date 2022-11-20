import os
from dataclasses import dataclass
from itertools import product
from textwrap import fill
from types import TracebackType as TbType
from typing import Type

import colorama

from jchess import __author__, __version__, terminal
from jchess.action import ExitGame
from jchess.game import MAX_PLY_COUNT, PROMOTION_OPTIONS, Game, Mode, Status
from jchess.geometry import V
from jchess.pieces import Player
from jchess.terminal import ctrlseq

from ._configs import Pallet, SymbolDict
from ._constants import MODE_STRINGS, H, Loc, Templates, W

TypeExc = Type[BaseException]

UNINITIALIZED, START_MENU, PROMOTING, BOARD_FOCUS, GAME_OVER = list(Status)


@dataclass()
class Display:
    """Simple context manager to manipulate a terminal display showing a `Game`."""

    game: Game
    pallet: Pallet
    symbol: SymbolDict

    def __post_init__(self) -> None:
        self.original_terminal_size = (-1, -1)  # set in __enter__

    def __enter__(self) -> "Display":
        self.original_terminal_size = os.get_terminal_size()
        colorama.init()
        terminal.clear()
        terminal.resize(W.MAIN + 2, H.MAIN + 2)  # +2 to account for boarder
        terminal.reset_cursor()
        terminal.hide_cursor()
        return self

    def __exit__(self, exc_type: TypeExc, exc_val: TypeExc, exc_tb: TbType) -> bool:
        terminal.clear()
        terminal.show_cursor()
        terminal.resize(*self.original_terminal_size)
        return exc_type is ExitGame

    def refresh(self) -> None:
        """Update and re-show the display."""
        status, status_prev = self.game.status, self.game.status_prev
        parts = []

        # adjust for previous status of game
        if status is not status_prev:
            if status_prev is UNINITIALIZED:
                pass  # should clear start menu, but it's overridden by main board
            elif status_prev is START_MENU:
                parts.extend(self.__init_main())
            elif status_prev is PROMOTING:
                parts.extend(self.__clear_promotion())

        if status is START_MENU:
            parts.extend(self.__refresh_start())
        elif status is BOARD_FOCUS:
            parts.extend(self.__refresh_main())
        elif status is PROMOTING:
            parts.extend(self.__refresh_promotion())
        elif status is GAME_OVER:
            parts.extend(self.__init_game_over())

        print("".join(parts))

    # Helper methods for `Display.refresh` ------------------------------------------- #

    def __init_main(self) -> list[str]:
        quit_msg = "spam CTRL+C." if self.game.mode is Mode.TDB else "hit escape."
        headline = "Welcome to J-Chess! To quit " + quit_msg

        mode = self.game.mode
        assert mode, "Mode should be set by this point in the game."

        taken_blank = "\n".join([" " * W.SIDE] * H.SIDE_SMALL)

        return [
            # parts same each run - but __init_main is only run once so not wasteful
            ctrlseq(__version__.center(W.SIDE), at=Loc.VERSION, edge=True),
            ctrlseq(__author__.center(W.SIDE), at=Loc.AUTHOR, edge=True),
            ctrlseq(" " * W.GUTTER, at=Loc.GUTTER, edge=True),
            *[  # board
                ctrlseq(
                    " " * W.TILE,
                    at=V(*Loc.BOARD) + V((W.TILE + 1) * x, 2 * y),
                    edge=True,
                )
                for x, y in product(range(8), range(8))
            ],
            # dynamic parts
            ctrlseq(headline.center(W.MAIN), at=Loc.HEADLINE, edge=True),
            ctrlseq(taken_blank, clr=self.pallet.board[1], at=Loc.LH_TAKEN, edge=True),
            ctrlseq(taken_blank, clr=self.pallet.board[0], at=Loc.RH_TAKEN, edge=True),
            ctrlseq(Templates.README[Player.ONE][mode], at=Loc.LH_README, edge=True),
            ctrlseq(Templates.README[Player.TWO][mode], at=Loc.RH_README, edge=True),
            ctrlseq(Templates.COL_LABELS, at=Loc.COL_LABELS1),
            ctrlseq(Templates.ROW_LABELS, at=Loc.ROW_LABELS1),
            ctrlseq(Templates.COL_LABELS, at=Loc.COL_LABELS2),
            ctrlseq(Templates.ROW_LABELS, at=Loc.ROW_LABELS2),
        ]

    def __clear_promotion(self) -> list[str]:
        mode = self.game.mode
        assert mode, "Mode should be set by this point in the game."
        return [
            ctrlseq(Templates.README[Player.ONE][mode], at=Loc.LH_README, edge=True),
            ctrlseq(Templates.README[Player.TWO][mode], at=Loc.RH_README, edge=True),
        ]

    def __init_game_over(self) -> list[str]:
        board = self.game.board
        if board.ply >= MAX_PLY_COUNT:
            msg = f"Draw: {MAX_PLY_COUNT // 2} turn limit reached."
        elif not board.can_move() and board.in_check():
            msg = f"Player {board.active_player} wins by checkmate!"
        elif not board.can_move() and not board.in_check():
            msg = "Draw: Stalemate."
        else:
            msg = f"Player {~board.active_player} wins by forfeit."
        msg += " Hit any key to quit."
        return [ctrlseq(msg.center(W.GUTTER), clr=self.pallet.focus, at=Loc.GUTTER)]

    def __refresh_start(self) -> list[str]:
        mode_str = MODE_STRINGS[self.game.scursor]
        coord = (Loc.START[0], Loc.START[1] + 2 + self.game.scursor)
        return [
            ctrlseq(Templates.START, at=Loc.START, edge=True),
            ctrlseq(mode_str, clr=self.pallet.cursor, at=coord),
        ]

    def __refresh_main(self) -> list[str]:
        pallet = self.pallet
        board = self.game.board

        s = board.score(Player.ONE), board.score(Player.TWO)

        parts = []

        # taken pieces & scores
        for i, player in enumerate(Player):
            # scores
            coord = Loc.LH_SCORE if player is Player.ONE else Loc.RH_SCORE
            parts.append(
                ctrlseq(
                    Templates.INFO.format(player, s[i]),
                    clr=pallet.text[player],
                    at=coord,
                    edge=True,
                )
            )
            # taken pieces
            taken_pieces = self.game.board.taken_pieces[player]
            color = self.pallet.piece[~player] + self.pallet.board[player.value % 2]
            text = fill(" ".join(self.symbol[role] for role in taken_pieces), W.SIDE)
            coord = Loc.LH_TAKEN if player is Player.ONE else Loc.RH_TAKEN
            parts.append(ctrlseq(text, clr=color, at=coord))

        # gutter message
        msg = f"Turn {board.ply // 2 + 1} of {MAX_PLY_COUNT // 2}. "
        if s[0] > s[1]:
            msg += f"Player ONE leads by {s[0] - s[1]} point(s)."
        elif s[1] > s[0]:
            msg += f"Player TWO leads by {s[1] - s[0]} point(s)."
        else:
            msg += "Players ONE & TWO are equal in score."
        parts.append(ctrlseq(msg.center(W.GUTTER), at=Loc.GUTTER))

        # update board:
        cursor = self.game.bcursor
        focus = self.game.board[cursor]
        attacker = self.game.attacker
        for coord, piece in board.items():
            show_targets = (
                # show *potential* targets
                not attacker
                and focus
                and focus.player is board.active_player
                and coord in board.targets_of[cursor]
                # or show *actual* targets
                or (attacker and coord in board.targets_of[attacker.coord])
            )

            color_parts = []
            if coord == cursor:
                color_parts.append(pallet.cursor)
            elif attacker and coord == attacker.coord:
                color_parts.append(pallet.focus)
            elif show_targets:
                color_parts.append(pallet.target)
            else:
                color_parts.append(pallet.board[sum(coord) % 2])

            color_parts.append(pallet.piece[piece.player] if piece else "")
            square = f" {self.symbol[piece.role]} " if piece else "   "

            display_loc = Loc.BOARD + V((W.TILE + 1) * coord.x, 2 * coord.y)
            parts.append(ctrlseq(square, clr="".join(color_parts), at=display_loc))

        return parts

    def __refresh_promotion(self) -> list[str]:
        xp, yp = (
            Loc.LH_PROMOTION
            if self.game.board.active_player is Player.ONE
            else Loc.RH_PROMOTION
        )
        role = PROMOTION_OPTIONS[self.game.pcursor]
        color = self.pallet.cursor
        option_str = f"({role.symbol}) {role}"
        return [
            ctrlseq(Templates.PROMOTION, at=(xp, yp)),
            ctrlseq(option_str, clr=color, at=(xp, yp + 4 + self.game.pcursor)),
        ]
