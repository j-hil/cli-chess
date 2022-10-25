"""Contains display settings for different consoles."""

from dataclasses import KW_ONLY, dataclass

from colorama import Back, Fore, Style

from jchess.pieces import Player, Role


class SymbolDict(dict[Role, str]):
    def __init__(self, symbols: str) -> None:
        self.update(zip(Role, symbols))
        super().__init__()


UTF8_SYMBOLS = SymbolDict("♚♛♜♝♞♟")  # options to try/add: '♔♕♖♗♘♙'
DEFAULT_SYMBOLS = SymbolDict("KQHIJi")
STANDARD_SYMBOLS = SymbolDict("KQRBNi")


@dataclass
class Pallet:

    _: KW_ONLY
    square1: str = Back.LIGHTBLACK_EX
    square2: str = Back.CYAN
    cursor: str = Back.LIGHTMAGENTA_EX
    focus: str = Back.LIGHTRED_EX
    target: str = Back.LIGHTGREEN_EX
    piece1: str = Style.BRIGHT + Fore.WHITE
    piece2: str = Style.DIM + Fore.BLACK

    def __post_init__(self) -> None:
        # transform inputs into attrs for easier implementation
        self.piece = {Player.ONE: self.piece1, Player.TWO: self.piece2}
        self.board = {0: self.square1, 1: self.square2}
        self.text = {
            Player.ONE: self.piece1 + self.square2,
            Player.TWO: self.piece2 + self.square1,
        }


# for Visual Studio Code
VSC_PALLET = Pallet(
    square1=Back.MAGENTA,
    square2=Back.BLACK,
    cursor=Back.YELLOW,
    focus=Back.RED,
    target=Back.GREEN,
)

# this config actually works quite well in all the terminals I've tried
DEFAULT_PALLET = Pallet()
