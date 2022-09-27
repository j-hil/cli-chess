"""Contains display settings for different consoles."""

from dataclasses import dataclass
from colorama import Fore, Style, Back
from jchess.squares import Player, Role


@dataclass
class Config:
    """Represents display settings."""

    # fmt: off
    def __init__(self, *,
        symbols: str = "KQHIJi",
        board_clr1: str, board_clr2: str,
        cursor_clr: str, highlight_clr: str, valid_clr: str
    ) -> None:
        """Transform inputs into attrs better for implementation.

        :param board_clr1: Background color of 'even' squares.
        :param board_clr2: Background color of 'odd' squares.
        :param cursor_clr: Color of player controlled cursor.
        :param highlight_clr: Color of player selected piece.
        :param valid_clr: Color of squares available to move too.
        :param symbols: Characters to represent each piece; defaults to "KQHIJi"
        """
        self.cursor_color = cursor_clr
        self.highlight_color = highlight_clr
        self.valid_color = valid_clr
        self.role_symbol = dict(zip(Role, list(symbols + " ")))
        self.player_color = {
            Player.ONE: Style.BRIGHT + Fore.WHITE,
            Player.TWO: Style.NORMAL + Fore.BLACK,
            Player.NULL: "",
        }
        self.board_color = {0: board_clr1, 1: board_clr2}
    # fmt: on


# for Visual Studio Code
VSC_CONFIG = Config(
    # options to try/add: '♔♕♖♗♘♙', '♚♛♜♝♞♟',  'KQHIJi', or "KQRBNi"
    symbols="♚♛♜♝♞♟",
    board_clr1=Back.MAGENTA,
    board_clr2=Back.BLACK,
    cursor_clr=Back.YELLOW,
    highlight_clr=Back.RED,
    valid_clr=Back.GREEN,
)

# for Powershell
PS_CONFIG = Config(
    board_clr1=Back.LIGHTBLACK_EX,
    board_clr2=Back.CYAN,
    cursor_clr=Back.LIGHTMAGENTA_EX,
    highlight_clr=Back.LIGHTRED_EX,
    valid_clr=Back.LIGHTGREEN_EX,
)

# for Command Prompt
CMD_CONFIG = Config(
    board_clr1=Back.YELLOW,
    board_clr2=Back.GREEN,
    cursor_clr=Back.BLUE,
    highlight_clr=Back.RED,
    valid_clr=Back.CYAN,
)

CONFIG = {"cmd.exe": CMD_CONFIG, "powershell.exe": PS_CONFIG}
