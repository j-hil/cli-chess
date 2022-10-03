from jchess.display import DisplayArray
from jchess.game.state import GameState

def generate_main_display(game: GameState) -> DisplayArray: ...

MAIN_DISPLAY_TEMPLATE: str
MAIN_DISPLAY_ROWS: int
