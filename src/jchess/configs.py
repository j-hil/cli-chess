from dataclasses import dataclass
from colorama import Fore, Style, Back
from jchess.pieces import Player, Role

_STANDARD_SYMBOLS = {
    Role.KING: "K",
    Role.QUEEN: "Q",
    Role.ROOK: "H",
    Role.BISHOP: "I",
    Role.KNIGHT: "J",
    Role.PAWN: "i",
    Role.NULL: " ",
}


@dataclass
class Config:
    role_symbol: dict[Role, str]
    player_color: dict[Player, str]
    board_color: dict[int, str]
    cursor_color: str
    selected_color: str
    valid_color: str


VS_CODE_CONFIG = Config(
    role_symbol=_STANDARD_SYMBOLS,
    player_color={
        Player.ONE: Style.BRIGHT + Fore.WHITE,
        Player.TWO: Style.BRIGHT + Fore.BLACK,
        Player.NULL: "",
    },
    board_color={0: Back.MAGENTA, 1: Back.BLACK},
    cursor_color=Back.YELLOW,
    selected_color=Back.RED,
    valid_color=Back.GREEN,
)

POWERSHELL_CONFIG = Config(
    role_symbol=_STANDARD_SYMBOLS,
    player_color={
        Player.ONE: Style.BRIGHT + Fore.WHITE,
        Player.TWO: Style.NORMAL + Fore.BLACK,
        Player.NULL: "",
    },
    board_color={0: Back.WHITE, 1: Back.LIGHTBLACK_EX},
    cursor_color=Back.YELLOW,
    selected_color=Back.RED,
    valid_color=Back.GREEN,
)
