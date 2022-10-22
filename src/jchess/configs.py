"""Contains display settings for different consoles."""

from dataclasses import KW_ONLY, dataclass

from colorama import Back, Fore, Style

from jchess.pieces import Player, Role


@dataclass
class Config:
    """Represents display settings, including sensible defaults."""

    _: KW_ONLY
    symbols: str = "KQHIJi"
    square1_color: str = Back.LIGHTBLACK_EX
    square2_color: str = Back.CYAN
    cursor_color: str = Back.LIGHTMAGENTA_EX
    highlight_color: str = Back.LIGHTRED_EX
    target_color: str = Back.LIGHTGREEN_EX
    player1_color: str = Style.BRIGHT + Fore.WHITE
    player2_color: str = Style.DIM + Fore.BLACK

    def __post_init__(self) -> None:
        """Transform inputs into attrs better for implementation."""
        self.role_symbol = dict(zip(Role, list(self.symbols)))
        self.player_color = {
            Player.ONE: self.player1_color,
            Player.TWO: self.player2_color,
        }
        self.board_color = {0: self.square1_color, 1: self.square2_color}


# for Visual Studio Code
VSC_CONFIG = Config(
    # options to try/add: '♔♕♖♗♘♙', '♚♛♜♝♞♟',  'KQHIJi', or "KQRBNi"
    symbols="♚♛♜♝♞♟",
    square1_color=Back.MAGENTA,
    square2_color=Back.BLACK,
    cursor_color=Back.YELLOW,
    highlight_color=Back.RED,
    target_color=Back.GREEN,
)

# this config actually works quite well in all the terminals I've tried
DEFAULT_CONFIG = Config()
