"""Enum to restrict/define user inputs and functions to get & translate inputs."""

from enum import Enum

from jchess.terminal import get_input

ESC = "\x1b"


class ExitGame(Exception):
    """Error to raise when exiting the game."""


class Action(Enum):
    """Allowed user inputs."""

    SELECT = "↲"
    UP = "↑"
    DOWN = "↓"
    RIGHT = "→"
    LEFT = "←"
    IGNORE = "~"
    FORFEIT = "!"

    def __repr__(self) -> str:
        return self.value


def get_action_rhs() -> Action:
    """Get input form the right hand side of keyboard (arrow, enter and end keys)."""
    x = get_input()
    if x == ESC:
        raise ExitGame
    return {
        "\r": Action.SELECT,
        "↑": Action.UP,
        "↓": Action.DOWN,
        "→": Action.RIGHT,
        "←": Action.LEFT,
        "⇲": Action.FORFEIT,
    }.get(x, Action.IGNORE)


def get_action_lhs() -> Action:
    """Get input from the left hand side of keyboard (WASD, tab and Q keys)."""
    x = get_input().lower()
    if x == ESC:
        raise ExitGame
    return {
        " ": Action.SELECT,
        "w": Action.UP,
        "s": Action.DOWN,
        "d": Action.RIGHT,
        "a": Action.LEFT,
        "q": Action.FORFEIT,
        "\x1b": Action.FORFEIT,
    }.get(x, Action.IGNORE)
