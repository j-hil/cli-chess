from abc import ABC, abstractmethod
from enum import IntEnum
from itertools import product
from typing import TYPE_CHECKING

from jchess import __author__, __version__
from jchess.game import Mode
from jchess.geometry import V
from jchess.terminal import ctrlseq

if TYPE_CHECKING:
    from jchess.display._class import Display


class Height(IntEnum):
    START = 7

    MAIN = 25


class Width(IntEnum):
    START = 24

    MAIN = 85
    SIDE = 11
    MIDDLE = MAIN - 2 * (SIDE + 1)
    BOARD = MIDDLE - 2 * (SIDE + 4)
    TILE = BOARD // 8


class X(IntEnum):
    LH_SIDE = 2
    RH_SIDE = 2 + Width.MAIN - Width.SIDE
    MIDDLE = Width.SIDE + 3
    BOARD = Width.SIDE + 18
    START = (Width.MAIN - Width.START) // 2 + 1


class Y(IntEnum):
    GUTTER = 24
    BOARD = 6
    START = (Height.MAIN - Height.START) // 2 + 1


class DisplayElement(ABC):

    W: int = NotImplemented
    H: int = NotImplemented
    LOC: V = NotImplemented

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        # Manually make class attributes abstract. Using decorators abstractmethod,
        # property and classmethod seems to work... but type hints hate it.
        if NotImplemented in [cls.W, cls.H, cls.LOC]:
            raise NotImplementedError("Class attr(s) W, H or LOC missing.")

    def __init__(self, display: "Display") -> None:
        self.game = display.game
        self.pallet = display.pallet
        self.symbol = display.symbol

    @abstractmethod
    def init_seq(self) -> str:
        ...

    def refresh_seq(self) -> str:
        return self.init_seq()

    def clear_seq(self) -> str:
        return ctrlseq("\n".join([" " * (self.W + 1)] * (self.W + 1)), at=self.LOC)


# class StartMenu(DisplayElement):
#     def init_seq(self):
#         pass

#     def refresh_seq(self):
#         pass

#     def clear_seq(self):
#         pass


class Title(DisplayElement):

    W = Width.MAIN
    H = 1
    LOC = V(X.LH_SIDE, 2)

    def init_seq(self):
        quit_msg = "spam CTRL+C." if self.game.mode is Mode.TDB else "hit escape."
        headline = "Welcome to J-Chess! To quit " + quit_msg
        return ctrlseq(headline.center(self.W), at=self.LOC, edge=True)


class Author(DisplayElement):

    W = Width.SIDE
    H = 1
    LOC = V(X.RH_SIDE, Y.GUTTER)

    def init_seq(self) -> str:
        return ctrlseq(__author__.center(self.W), at=self.LOC, edge=True)


class Version(DisplayElement):

    W = Width.SIDE
    H = 1
    LOC = V(X.LH_SIDE, Y.GUTTER)

    def init_seq(self) -> str:
        return ctrlseq(__version__.center(self.W), at=self.LOC, edge=True)


class Gutter(DisplayElement):

    W = Width.MIDDLE
    H = 1
    LOC = V(X.MIDDLE, Y.GUTTER)

    def init_seq(self) -> str:
        return ctrlseq(" " * self.W, at=self.LOC, edge=True)


class Board(DisplayElement):

    W = Width.BOARD
    H = Height.MAIN
    LOC = V(X.BOARD, Y.BOARD)

    def init_seq(self) -> str:
        # init just creates the board outline
        return "".join(
            ctrlseq(
                " " * Width.TILE,
                at=self.LOC + V((Width.TILE + 1) * x, 2 * y),
                edge=True,
            )
            for x, y in product(range(8), range(8))
        )

    def refresh_seq(self) -> str:
        # refresh only updated the square (doesn't reprint boarder - to slow)
        cursor = self.game.bcursor
        focus = self.game.board[cursor]
        attacker = self.game.attacker
        board = self.game.board
        pallet = self.pallet

        parts = []
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

            display_loc = self.LOC + V((Width.TILE + 1) * coord.x, 2 * coord.y)
            parts.append(ctrlseq(square, clr="".join(color_parts), at=display_loc))
        return "".join(parts)


class Start(DisplayElement):

    W = Width.START
    H = Height.START
    LOC = V(X.START, Y.START)

    def __init__(self, display: "Display") -> None:
        super().__init__(display)

        self.mode_strings = [f"{m.value: ^{self.W}}" for m in Mode]
        self.scursor_prev = 0

    def init_seq(self) -> str:
        lines = [
            "Pick a game mode:",
            "=" * self.W,
            *[f"{m.value}" for m in Mode],
            "=" * self.W,
            "[esc: quit, space: pick]",
        ]
        text = "\n".join(l.center(self.W) for l in lines)
        return ctrlseq(text, at=self.LOC, edge=True)

    def refresh_seq(self) -> str:
        cursor_prev, cursor_curr = self.scursor_prev, self.game.scursor

        parts = []
        for color, cursor in (
            (self.pallet.focus, cursor_prev),
            (self.pallet.cursor, cursor_curr),
        ):
            mode_str = self.mode_strings[cursor]
            coord = self.LOC + V(0, 2 + self.scursor_prev)
            parts.append(ctrlseq(mode_str, clr=color, at=coord))

        self.scursor_prev = self.game.scursor
        return "".join(parts)
