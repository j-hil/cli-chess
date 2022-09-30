"""Contains display settings for different consoles."""
# TODO: investigate if dataclass is really helping here

from dataclasses import dataclass
from colorama import Fore, Style, Back
from jchess.squares import Player, Role


@dataclass
class Config:
    """Represents display settings."""

    # fmt: off
    def __init__(self, *,
        symbols: str = "KQHIJi",
        board_color1: str, board_color2: str,
        cursor_color: str, highlight_color: str, valid_color: str
    ) -> None:
        """Transform inputs into attrs better for implementation.

        :param board_clr1: Background color of 'even' squares.
        :param board_clr2: Background color of 'odd' squares.
        :param cursor_clr: Color of player controlled cursor.
        :param highlight_clr: Color of player selected piece.
        :param valid_clr: Color of squares available to move too.
        :param symbols: Characters to represent each piece; defaults to "KQHIJi"
        """
        self.cursor_color = cursor_color
        self.highlight_color = highlight_color
        self.valid_color = valid_color
        self.role_symbol = dict(zip(Role, list(symbols + " ")))
        self.player_color = {
            Player.ONE: Fore.WHITE, #Style.BRIGHT + Fore.WHITE,
            Player.TWO: Fore.BLACK,#Style.NORMAL + Fore.BLACK,
            Player.NULL: "",
        }
        self.board_color = {0: board_color1, 1: board_color2}
    # fmt: on


# for Visual Studio Code
VSC_CONFIG = Config(
    # options to try/add: '♔♕♖♗♘♙', '♚♛♜♝♞♟',  'KQHIJi', or "KQRBNi"
    symbols="♚♛♜♝♞♟",
    board_color1=Back.MAGENTA,
    board_color2=Back.BLACK,
    cursor_color=Back.YELLOW,
    highlight_color=Back.RED,
    valid_color=Back.GREEN,
)

# for Powershell
PS_CONFIG = Config(
    board_color1=Back.LIGHTBLACK_EX,
    board_color2=Back.CYAN,
    cursor_color=Back.LIGHTMAGENTA_EX,
    highlight_color=Back.LIGHTRED_EX,
    valid_color=Back.LIGHTGREEN_EX,
)

# for Command Prompt
CMD_CONFIG = Config(
    board_color1=Back.YELLOW,
    board_color2=Back.GREEN,
    cursor_color=Back.BLUE,
    highlight_color=Back.RED,
    valid_color=Back.CYAN,
)

CONFIG = {"cmd.exe": CMD_CONFIG, "powershell.exe": PS_CONFIG}

print(CMD_CONFIG)
