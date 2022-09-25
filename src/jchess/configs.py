"""Contains display settings for different consoles."""
# TODO: A lot of repetition in configs so maybe rethink
from dataclasses import dataclass
from colorama import Fore, Style, Back
from jchess.squares import Player, Role

_STANDARD_SYMBOLS = {
    Role.KING: "K",
    Role.QUEEN: "Q",
    Role.ROOK: "H",
    Role.BISHOP: "I",
    Role.KNIGHT: "J",
    Role.PAWN: "i",
    Role.NULL: " ",
}

_STANDARD_COLORS = {
        Player.ONE: Style.BRIGHT + Fore.WHITE,
        Player.TWO: Style.NORMAL + Fore.BLACK,
        Player.NULL: "",
    }


@dataclass
class Config:
    """Represents display settings."""

    role_symbol: dict[Role, str]
    player_color: dict[Player, str]
    board_color: dict[int, str]
    cursor_color: str
    selected_color: str
    valid_color: str


# for Visual Studio Code
VSC_CONFIG = Config(
    role_symbol=_STANDARD_SYMBOLS,
    player_color=_STANDARD_COLORS,
    board_color={0: Back.MAGENTA, 1: Back.BLACK},
    cursor_color=Back.YELLOW,
    selected_color=Back.RED,
    valid_color=Back.GREEN,
)

# for Powershell
PS_CONFIG = Config(
    role_symbol=_STANDARD_SYMBOLS,
    player_color=_STANDARD_COLORS,
    board_color={0: Back.WHITE, 1: Back.LIGHTBLACK_EX},
    cursor_color=Back.YELLOW,
    selected_color=Back.RED,
    valid_color=Back.GREEN,
)

# for Command Prompt
CMD_CONFIG = Config(
    role_symbol=_STANDARD_SYMBOLS,
    player_color=_STANDARD_COLORS,
    board_color={0: Back.YELLOW, 1: Back.GREEN},
    cursor_color=Back.CYAN,
    selected_color=Back.BLUE,
    valid_color=Back.CYAN,
)
