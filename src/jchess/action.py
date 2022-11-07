"""Enum to restrict/define user inputs and functions to get & translate inputs."""

from enum import Enum

from jchess.terminal import get_input


class Action(Enum):
    """Allowed user inputs."""

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
    """Get input form the right hand side of keyboard (arrow, enter and end keys)."""
    x = get_input()
    return {
        # Specific to rhs:
        "\r": Action.SELECT,
        "↑": Action.UP,
        "↓": Action.DOWN,
        "→": Action.RIGHT,
        "←": Action.LEFT,
        "⇲": Action.QUIT,
        # Should always be available to both players:
        " ": Action.SELECT,
        "\x1b": Action.QUIT,
    }.get(x, Action.IGNORE)


def get_action_lhs() -> Action:
    """Get input from the left hand side of keyboard (WASD, tab and Q keys)."""
    x = get_input().lower()
    return {
        # Specific to lhs:
        "\t": Action.SELECT,
        "w": Action.UP,
        "s": Action.DOWN,
        "d": Action.RIGHT,
        "a": Action.LEFT,
        "q": Action.QUIT,
        # Should always be available to both players:
        " ": Action.SELECT,
        "\x1b": Action.QUIT,
    }.get(x, Action.IGNORE)
