from abc import ABC, abstractclassmethod, abstractmethod
from enum import Enum
from colorama import Fore, Back, Style

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from state import GameState

class Color(Enum):
    # TODO: can probably remove in favour of using colorama.Fore.Black etc,
    # (might mess up typing)
    B = "Black"
    W = "White"
    N = "Null"

class Piece(ABC):

    @property
    @abstractclassmethod
    def ICON(cls) -> str:
        pass

    def __init__(self, coord: tuple[int, int], color: Color) -> None:
        super().__init__()
        self.coord = self._start_coord =coord
        self.color = color


    @property
    def start_coord(self):
        return self._start_coord

    @abstractmethod
    def accessible_coords(self, state: "GameState") -> list[tuple[int, int]]:
        pass

    def __repr__(self):
        # TODO: coloring should be decided by GameState
        if self.color == Color.B:
            return Fore.BLACK + self.ICON + Fore.RESET
        if self.color == Color.W:
            return Fore.WHITE + self.ICON + Fore.RESET
        return self.ICON


class King(Piece):
    ICON = "K"

    def accessible_coords(self, state: "GameState"):
        deltas = [
            (0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)
        ]
        x, y = self.coord
        result = []
        for dx, dy in deltas:
            target: Piece | None = state.board[y+dy][x+dx]
            if target is not None and target.color != self.color:
                result.append((x + dx, y + dy))
            if target is None:
                result.append((x + dx, y + dy))
        return result

class Queen(Piece):
    ICON = "Q"

    def accessible_coords(self, state: "GameState") -> list[tuple[int, int]]:
        rook = Rook(self.coord, self.color)
        bishop = Bishop(self.coord, self.color)
        return rook.accessible_coords(state) + bishop.accessible_coords(state)

class Bishop(Piece):
    ICON = "I"

    def accessible_coords(self, state: "GameState") -> list[tuple[int, int]]:
        x, y = self.coord
        result = []
        for s1, s2 in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            for dx in range(1, 8):
                xt, yt = x+s2*dx, y+s1*dx
                if y+s1*dx in range(8) and x+s2*dx in range(8):
                    target_square: Piece | None = state.board[y+s1*dx][x+s2*dx]
                    if target_square is not None and target_square.color == self.color:
                        break
                    if target_square is not None and target_square.color != self.color:
                        result.append((xt, yt))
                        break
                    result.append((xt, yt))

        return result

class Knight(Piece):
    ICON = "J"

    def accessible_coords(self, state: "GameState") -> list[tuple[int, int]]:
        deltas = [
            (2, 1), (-2, 1), (2, -1), (-2, -1),
            (1, 2), (-1, 2), (1, -2), (-1, -2),
        ]
        x, y = self.coord
        result = []
        for dx, dy in deltas:
            if x + dx in range(8) and y + dy in range(8):
                target: Piece | None = state.board[y+dy][x+dx]
                if target is not None and target.color != self.color:
                    result.append((x + dx, y + dy))
                if target is None:
                    result.append((x + dx, y + dy))
        return result

class Rook(Piece):
    ICON = "H"

    def accessible_coords(self, state: "GameState") -> list[tuple[int, int]]:
        x, y = self.coord
        result = []

        for dx in range(1, 8):
            if (x + dx) in range(8):
                target_square: Piece | None = state.board[y][x+dx]
                if target_square is not None and target_square.color == self.color:
                    break
                if target_square is not None and target_square.color != self.color:
                    result.append((x + dx, y))
                    break
                result.append((x + dx, y))

        for dy in range(1, 8):
            if (y + dy) in range(8):
                target_square: Piece | None = state.board[y+dy][x]
                if target_square is not None and target_square.color == self.color:
                    break
                if target_square is not None and target_square.color != self.color:
                    result.append((x, y+dy))
                    break
                result.append((x, y+dy))

        for dx in range(1, 8):
            if (x - dx) in range(8):
                target_square: Piece | None = state.board[y][x-dx]
                if target_square is not None and target_square.color == self.color:
                    break
                if target_square is not None and target_square.color != self.color:
                    result.append((x - dx, y))
                    break
                result.append((x - dx, y))

        for dy in range(1, 8):
            if (y - dy) in range(8):
                target_square: Piece | None = state.board[y-dy][x]
                if target_square is not None and target_square.color == self.color:
                    break
                if target_square is not None and target_square.color != self.color:
                    result.append((x, y-dy))
                    break
                result.append((x, y-dy))

        return result


class Pawn(Piece):
    ICON = "i"

    def accessible_coords(self, state: "GameState") -> list[tuple[int, int]]:
        x, y = self.coord

        result = []
        if self.color == Color.W:
            result.append((x + 1, y))
        else: # self.color == Color.B:
            result.append((x - 1, y))

        if self.coord == self.start_coord:
            if self.color == Color.W:
                result.append((x + 2, y))
            else: # self.color == Color.B:
                result.append((x - 2, y))
        return result

