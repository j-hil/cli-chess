"""Contains display settings for different consoles."""
from dataclasses import dataclass, KW_ONLY
from colorama import Fore, Style, Back
from jchess.squares import Player, Role


@dataclass
class Config:
    """Represents display settings."""

    _: KW_ONLY
    symbols: str = "KQHIJi"
    player1_color: str = Style.BRIGHT + Fore.WHITE
    player2_color: str = Style.NORMAL + Fore.BLACK
    board_color1: str
    board_color2: str
    cursor_color: str
    selected_color: str
    valid_color: str

    def __post_init__(self) -> None:
        self.role_symbol = dict(zip(Role, list(self.symbols + " ")))
        self.player_color = {
            Player.ONE: self.player1_color,
            Player.TWO: self.player2_color,
            Player.NULL: "",
        }
        self.board_color = {0: self.board_color1, 1: self.board_color2}


# for Visual Studio Code
VSC_CONFIG = Config(
    # options to try/add: '♔♕♖♗♘♙', '♚♛♜♝♞♟',  'KQHIJi', or "KQRBNi"
    symbols="♚♛♜♝♞♟",
    board_color1=Back.MAGENTA,
    board_color2=Back.BLACK,
    cursor_color=Back.YELLOW,
    selected_color=Back.RED,
    valid_color=Back.GREEN,
)

# for Powershell
PS_CONFIG = Config(
    board_color1=Back.LIGHTBLACK_EX,
    board_color2=Back.CYAN,
    cursor_color=Back.LIGHTMAGENTA_EX,
    selected_color=Back.LIGHTRED_EX,
    valid_color=Back.LIGHTGREEN_EX,
)

# for Command Prompt
CMD_CONFIG = Config(
    board_color1=Back.YELLOW,
    board_color2=Back.GREEN,
    cursor_color=Back.BLUE,
    selected_color=Back.RED,
    valid_color=Back.CYAN,
)

CONFIG = {"cmd.exe": CMD_CONFIG, "powershell.exe": PS_CONFIG}
