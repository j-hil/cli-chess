from enum import Enum
from jchess.game.state import GameState

def evolve_state_(game: GameState, action: Action | None = ...) -> None: ...

class Mode(Enum):
    ONE: str
    TWO: str
    THREE: str

class Action(Enum):
    UP: int
    DOWN: int
    LEFT: int
    RIGHT: int
    SELECT: int
    QUIT: int
    IGNORE: int

CARDINAL_DIRECTION: dict[Action, tuple[int, int]]
ACTION_INPUTS: dict[Action, list[bytes]]
ROTATE: dict[Action, Action]
