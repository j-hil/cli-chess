from enum import Enum

from jchess.terminal import get_input

CSI = "\x1b["


class Action(Enum):
    SELECT = "↲"
    UP = "↑"
    DOWN = "↓"
    RIGHT = "→"
    LEFT = "←"
    IGNORE = "~"
    QUIT = "!"

    def __repr__(self) -> str:
        return self.value


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
