"""Contains display settings for different consoles."""
from dataclasses import dataclass
from colorama import Fore, Style, Back
from jchess.squares import Player, Role

# TODO: add defaults to config - reduce duplication
@dataclass
class Config:
    """Represents display settings."""

    role_symbol: dict[Role, str]
    player_color: dict[Player, str]
    board_color: dict[int, str]
    cursor_color: str
    selected_color: str
    valid_color: str

def _unpack(syms: str) -> dict[Role, str]:
    return dict(zip(Role, list(syms)))


# for Visual Studio Code
VSC_CONFIG = Config(
    # options to try/add: '♔♕♖♗♘♙ ', '♚♛♜♝♞♟ ',  'KQHIJi ', or "KQRBNi"
    role_symbol=_unpack("♚♛♜♝♞♟ "),
    player_color={
        Player.ONE: Style.BRIGHT + Fore.WHITE,
        Player.TWO: Style.NORMAL + Fore.BLACK,
        Player.NULL: "",
    },
    board_color={0: Back.MAGENTA, 1: Back.BLACK},
    cursor_color=Back.YELLOW,
    selected_color=Back.RED,
    valid_color=Back.GREEN,
)

# for Powershell
PS_CONFIG = Config(
    role_symbol=_unpack('KQHIJi '),
    player_color={
        Player.ONE: Style.BRIGHT + Fore.WHITE,
        Player.TWO: Style.NORMAL + Fore.BLACK,
        Player.NULL: "",
    },
    board_color={0: Back.LIGHTBLACK_EX, 1: Back.CYAN},
    cursor_color=Back.LIGHTMAGENTA_EX,
    selected_color=Back.LIGHTRED_EX,
    valid_color=Back.LIGHTGREEN_EX,
)

# for Command Prompt
CMD_CONFIG = Config(
    role_symbol=_unpack('KQHIJi '),
    player_color={
        Player.ONE: Style.BRIGHT + Fore.WHITE,
        Player.TWO: Style.NORMAL + Fore.BLACK,
        Player.NULL: "",
    },
    board_color={0: Back.YELLOW, 1: Back.GREEN},
    cursor_color=Back.BLUE,
    selected_color=Back.RED,
    valid_color=Back.CYAN,
)

CONFIG = {"cmd.exe": CMD_CONFIG, "powershell.exe": PS_CONFIG}
