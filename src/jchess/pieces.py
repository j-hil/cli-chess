from abc import ABC, abstractclassmethod
from enum import Enum
from colorama import Fore, Back, Style

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
        self.coord = coord
        self.color = color

    def __repr__(self):
        if self.color == Color.B:
            return Fore.BLACK + self.ICON + Fore.RESET
        if self.color == Color.W:
            return Fore.WHITE + self.ICON + Fore.RESET
        return self.ICON


class King(Piece):
    ICON = "K"

class Queen(Piece):
    ICON = "Q"

class Bishop(Piece):
    ICON = "I"

class Knight(Piece):
    ICON = "$"

class Rook(Piece):
    ICON = "H"

class Pawn(Piece):
    ICON = "i"
