import os
from dataclasses import dataclass
from types import TracebackType
from typing import Type

import colorama

from jchess import __author__ as author
from jchess import __version__ as version
from jchess import terminal
from jchess.action import ExitGame
from jchess.game import MAX_PLY_COUNT, PROMOTION_OPTIONS, Game, Status
from jchess.geometry import V
from jchess.pieces import Player, Role
from jchess.terminal import ctrlseq

from ._configs import Pallet, SymbolDict
from ._constants import (
    COL_LABELS,
    HELP_TEMPLATES,
    INFO_TEMPLATE,
    MAIN_DISPLAY_TEMPLATE,
    MODE_STRINGS,
    PROMOTION_CLEAR,
    PROMOTION_TEMPLATE,
    ROW_LABELS,
    START_MENU_ANCHOR,
    START_MENU_CLEAR,
    START_MENU_TEMPLATE,
)


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
        terminal.resize(87, 25)
        terminal.reset_cursor()
        terminal.hide_cursor()
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException],
        exc_val: Type[BaseException],
        exc_tb: TracebackType,
    ) -> bool:
        terminal.clear()
        terminal.show_cursor()
        terminal.resize(*self.original_terminal_size)
        return exc_type is ExitGame

    def refresh(self) -> None:
        """Update and re-show the display."""
        game = self.game
        pallet = self.pallet

        parts = []

        # adjust for previous status of game
        if game.status is not game.status_prev:
            if game.status_prev is Status.UNINITIALIZED:
                parts.append(ctrlseq(START_MENU_CLEAR, at=START_MENU_ANCHOR))
            elif game.status_prev is Status.START_MENU:
                parts.append(ctrlseq(MAIN_DISPLAY_TEMPLATE, at=(0, 0)))
                parts.append(ctrlseq(f"{version: ^11}", at=(3, 24)))
                parts.append(ctrlseq(f"by {author}", at=(76, 24)))
                for i, p in enumerate(Player):
                    parts.append(ctrlseq(ROW_LABELS, at=(30, 18 * i + 4)))
                    parts.append(ctrlseq(COL_LABELS, at=(36 * i + 26, 6)))
                    info = INFO_TEMPLATE.format(str(p))
                    parts.append(ctrlseq(info, clr=pallet.text[p], at=(72 * i + 3, 4)))
            elif game.status_prev is Status.PROMOTING:
                parts.append(ctrlseq(PROMOTION_CLEAR, at=(3, 12)))

        if game.status is Status.GAME_OVER:
            parts.append(self.__gutter_msg(game))

        elif game.status is Status.START_MENU:
            parts.append(ctrlseq(START_MENU_TEMPLATE, at=START_MENU_ANCHOR))
            mode_str = MODE_STRINGS[game.scursor]
            coord = START_MENU_ANCHOR + V(2, 3 + game.scursor)
            parts.append(ctrlseq(mode_str, clr=pallet.cursor, at=coord))

        elif game.status is Status.BOARD_FOCUS:

            parts.append(self.__gutter_msg(game))
            parts.append(self.__board_ctrlseq(game))
            for i, p in enumerate(Player):
                score = f"{game.board.score(p):0>3}"
                parts.append(ctrlseq(score, clr=pallet.text[p], at=(72 * i + 11, 6)))
                parts.append(self.__taken_ctrlseq(game, p))
                assert game.mode, "Mode should be set by this point in the game."
                parts.append(ctrlseq(HELP_TEMPLATES[p][game.mode], at=(72 * i + 3, 12)))

        elif game.status is Status.PROMOTING:
            role = PROMOTION_OPTIONS[game.pcursor]
            color = self.pallet.cursor
            parts.append(ctrlseq(PROMOTION_TEMPLATE, at=(3, 12)))
            option_str = f"({role.symbol}) {role}"
            parts.append(ctrlseq(option_str, clr=color, at=(3, 14 + game.pcursor)))

        print("".join(parts))

    # Helper methods for `Display.update()` ------------------------------------------ #

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
                and coord in board.targets_of[cursor]
            )
            show_actual_targets = attacker and coord in board.targets_of[attacker.coord]

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
        color = self.pallet.piece[~player] + self.pallet.board[player.value % 2]

        parts = []
        for i in range(15):
            (role,) = taken_pieces[i : i + 1] or [Role.BLANK]
            s = symbol[role]

            parts.append(f" {s}")
            if i % 5 == 4:
                parts.append(" \n")

        return ctrlseq("".join(parts), clr=color, at=(72 * player.value - 69, 8))

    def __gutter_msg(self, game: Game) -> str:
        board = game.board
        t, max_t = board.ply // 2 + 1, MAX_PLY_COUNT // 2
        s1, s2 = board.score(Player.ONE), board.score(Player.TWO)

        if game.status is not Status.GAME_OVER:

            color = ""
            if s1 > s2:
                msg = f"Turn {t} of {max_t}. Player ONE leads by {s1 - s2} point(s)."
            elif s2 > s1:
                msg = f"Turn {t} of {max_t}. Player TWO leads by {s2 - s1} point(s)."
            else:
                msg = f"Turn {t} of {max_t}. Players ONE & TWO are equal in score."
        else:
            player = board.active_player
            color = self.pallet.focus
            if board.ply >= MAX_PLY_COUNT:
                msg = f"Draw: {max_t} turn limit reached."
            elif not board.can_move() and board.in_check():
                msg = f"Player {player} wins by checkmate!"
            elif not board.can_move() and not board.in_check():
                msg = "Draw: Stalemate."
            else:
                msg = f"Player {~player} wins by forfeit."
            msg += " Hit any key to quit."
        return ctrlseq(f"{msg: ^55}", clr=color, at=(17, 24))
