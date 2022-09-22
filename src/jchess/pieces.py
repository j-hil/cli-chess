from abc import ABC, abstractclassmethod, abstractmethod
from copy import deepcopy
from enum import Enum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from jchess.state import GameState

class Player(Enum):
    ONE = "White"
    TWO = "Black"
    NULL = "Null"

class Piece(ABC):

    @property
    @abstractclassmethod
    def ICON(cls) -> str:
        pass

    def __init__(self, coord: tuple[int, int], player: Player) -> None:
        super().__init__()
        self.coord = coord
        self._start_coord = deepcopy(coord)
        self.player = player

    @property
    def start_coord(self):
        return self._start_coord

    @abstractmethod
    def accessible_coords(self, state: "GameState") -> list[tuple[int, int]]:
        pass

    def __repr__(self):
        return self.ICON

class Null(Piece):
    ICON = " "

    def accessible_coords(self, state: "GameState") -> list[tuple[int, int]]:
        return []


class King(Piece):
    ICON = "K"

    def accessible_coords(self, state: "GameState"):
        deltas = [
            (0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)
        ]
        x, y = self.coord
        result = []
        for dx, dy in deltas:
            if y+dy in range(8) and x+dx in range(8):
                target = state.board[y+dy][x+dx]
                if not isinstance(target, Null) and target.player != self.player:
                    result.append((x + dx, y + dy))
                if isinstance(target, Null):
                    result.append((x + dx, y + dy))
        return result

class Queen(Piece):
    ICON = "Q"

    def accessible_coords(self, state: "GameState") -> list[tuple[int, int]]:
        rook = Rook(self.coord, self.player)
        bishop = Bishop(self.coord, self.player)
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
                    target = state.board[y+s1*dx][x+s2*dx]
                    if not isinstance(target, Null) and target.player == self.player:
                        break
                    if not isinstance(target, Null) and target.player != self.player:
                        result.append((xt, yt))
                        break
                    result.append((xt, yt))

        return result

class Knight(Piece):
    ICON = "J"

    def accessible_coords(self, state: "GameState") -> list[tuple[int, int]]:
        deltas = [
            (2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2),
        ]
        x, y = self.coord
        result = []
        for dx, dy in deltas:
            if x + dx in range(8) and y + dy in range(8):
                target = state.board[y+dy][x+dx]
                if not isinstance(target, Null) and target.player != self.player:
                    result.append((x + dx, y + dy))
                if isinstance(target, Null):
                    result.append((x + dx, y + dy))
        return result

class Rook(Piece):
    ICON = "H"

    def accessible_coords(self, state: "GameState") -> list[tuple[int, int]]:
        x, y = self.coord
        result = []

        for s in [1, -1]:
            for dx in range(1, 8):
                if (x + s*dx) in range(8):
                    target= state.board[y][x+s*dx]
                    if not isinstance(target, Null) and target.player == self.player:
                        break
                    if not isinstance(target, Null) and target.player != self.player:
                        result.append((x + s*dx, y))
                        break
                    result.append((x + s*dx, y))

            for dy in range(1, 8):
                if (y + dy) in range(8):
                    target = state.board[y+s*dy][x]
                    if not isinstance(target, Null) and target.player == self.player:
                        break
                    if not isinstance(target, Null) and target.player != self.player:
                        result.append((x, y+s*dy))
                        break
                    result.append((x, y+s*dy))

        return result


class Pawn(Piece):
    ICON = "i"

    def accessible_coords(self, state: "GameState") -> list[tuple[int, int]]:
        x, y = self.coord

        if self.player == Player.ONE:
            s = 1
        elif self.player == Player.TWO:
            s = -1


        result = [(x + s , y)]
        if self.coord == self.start_coord:
            result.append((x + 2*s, y))

        board = state.board
        target1 = board[y + 1][x + s]
        target2 = board[y - 1][x + s]
        if not isinstance(target1, Null) and target1.player != self.player:
            result.append(target1.coord)
        if not isinstance(target2, Null) and target2.player != self.player:
            result.append(target2.coord)

        return result

