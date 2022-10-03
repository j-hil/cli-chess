from jchess.pieces import Player as Player, Role as Role

class Config:
    cursor_color: str
    highlight_color: str
    valid_color: str
    role_symbol: dict[Role, str]
    player_color: dict[Player, str]
    board_color: dict[int, str]

    # fmt: off
    def __init__(self, *,
        symbols: str = ...,
        board_color1: str, board_color2: str,
        cursor_color: str, highlight_color: str, valid_color: str
    ) -> None: ...
    # fmt: on

VSC_CONFIG: Config
PS_CONFIG: Config
CMD_CONFIG: Config
CONFIG: Config
