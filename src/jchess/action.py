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


ACTION_LOOKUP_RHS = {
    " ": Action.SELECT,
    "UP": Action.UP,
    "DOWN": Action.DOWN,
    "RIGHT": Action.RIGHT,
    "LEFT": Action.LEFT,
    "F12": Action.FORFEIT,
}

ACTION_LOOKUP_LHS = {
    " ": Action.SELECT,
    "W": Action.UP,
    "S": Action.DOWN,
    "D": Action.RIGHT,
    "A": Action.LEFT,
    "F1": Action.FORFEIT,
}

ACTION_LOOKUP_GENERIC = ACTION_LOOKUP_LHS | ACTION_LOOKUP_RHS


def get_action_rhs() -> Action:
    """Get input form the right hand side of keyboard (arrow, enter and end keys)."""
    x = get_input()
    if x == ESC:
        raise ExitGame
    return ACTION_LOOKUP_RHS.get(x, Action.IGNORE)


def get_action_lhs() -> Action:
    """Get input from the left hand side of keyboard (WASD, tab and Q keys)."""
    x = get_input().upper()
    if x == ESC:
        raise ExitGame
    return ACTION_LOOKUP_LHS.get(x, Action.IGNORE)


def get_action() -> Action:
    """Get input from either side of the keyboard."""
    x = get_input().upper()
    if x == ESC:
        raise ExitGame
    return ACTION_LOOKUP_GENERIC.get(x, Action.IGNORE)
