from dataclasses import dataclass
from colorama import Fore, Style, Back
from jchess.pieces import Player


@dataclass
class Config:
    player_color: dict[Player, str]
    board_color: dict[int, str]
    cursor_color: str
    selected_color: str
    valid_color: str


VS_CODE_CONFIG = Config(
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
