from enum import Enum, auto

from jchess.terminal import get_input

CSI = "\x1b["


class Action(Enum):
    SELECT = auto()
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()
    IGNORE = auto()
    QUIT = auto()


def get_action_rhs() -> Action:
    x = get_input()
    return {
        "↑": Action.UP,
        "↓": Action.DOWN,
        "→": Action.RIGHT,
        "←": Action.LEFT,
        "⇲": Action.QUIT,
        "\r": Action.SELECT,
        " ": Action.SELECT,
    }.get(x, Action.IGNORE)


def get_action_lhs() -> Action:
    x = get_input().lower()
    return {
        "w": Action.UP,
        "s": Action.DOWN,
        "d": Action.RIGHT,
        "a": Action.LEFT,
        "\x1b": Action.QUIT,
        "\t": Action.SELECT,
        " ": Action.SELECT,
    }.get(x, Action.IGNORE)
