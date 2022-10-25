import sys
from termios import TCSADRAIN, tcgetattr, tcsetattr  # pylint: disable=import-error
from tty import setraw

CSI = "\x1b["
# TODO: bring back in line with windows version


def clear():
    print(CSI + "2J")


def resize(w: int, h: int):
    print(f"{CSI}8;{h};{w}t")


def reset_cursor():
    print(CSI + "H")


def show_cursor():
    print(CSI + "?25h", end="")


def hide_cursor():
    print(CSI + "?25l", end="")


def getch() -> str:
    """Get a single character string from the user. Linux-compatible version."""
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
    """Convert keystroke into a game action. Linux-compatible version."""
    # only checked to work with keystrokes repr by 1 char, and the direction arrows

    user_input = getch()

    # Direction keys in vscode
    if user_input == "\x00":
        return {"H": "↑", "P": "↓", "M": "→", "K": "←", "O": "⇲"}[getch()]

    # Direction keys in usual console
    # TODO: replace "?" as appropriate
    if user_input + getch() == CSI:
        return {"A": "↑", "B": "↓", "C": "→", "D": "←", "?": "⇲"}[getch()]

    return user_input
