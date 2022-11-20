"""Linux implementation of some `terminal` functionality."""

import sys

assert sys.platform != "win32"

import os
from termios import TCSADRAIN, tcgetattr, tcsetattr  # pylint: disable=import-error
from tty import setraw

ESC = "\x1b"
CSI = "\x1b["


def clear() -> None:
    os.system("clear")


def resize(w: int, h: int) -> None:
    print(f"{CSI}8;{h};{w}t")


def reset_cursor() -> None:
    print(CSI + "H")


def show_cursor() -> None:
    print(CSI + "?25h", end="")


def hide_cursor() -> None:
    print(CSI + "?25l", end="")


def getch() -> str:
    """Get a single character string from the user - linux-compatible version."""
    # taken from https://stackoverflow.com/questions/71548267/

    sys.stdout.flush()
    ch = ""
    fd = sys.stdin.fileno()
    old_settings = tcgetattr(fd)
    try:
        setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        tcsetattr(fd, TCSADRAIN, old_settings)
    return ch


def get_input() -> str:
    """Convert keystroke into a game action - linux-compatible version."""
    # only checked to work with keystrokes repr by 1 char, and the direction arrows

    user_input = getch()

    # Direction keys in vscode
    if user_input == "\x00":
        return {
            "H": "UP",
            "P": "DOWN",
            "M": "RIGHT",
            "K": "LEFT",
        }[getch()]

    if user_input != ESC:
        return user_input

    next_part = getch()

    # double tapped escape (this is why escape must be hit twice on linux)
    if next_part == ESC:
        return ESC

    final_part = getch()

    if user_input + next_part + final_part == ESC + "OP":
        return "F1"

    # Direction keys in usual console
    if user_input + next_part == CSI:
        return {
            "A": "UP",
            "B": "DOWN",
            "C": "RIGHT",
            "D": "LEFT",
            "2": "F12",
        }[final_part]

    raise RuntimeError(f"Unrecognized input: {user_input + next_part + final_part}")
