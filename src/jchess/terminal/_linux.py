import sys
from enum import Enum
from termios import TCSADRAIN, tcgetattr, tcsetattr  # pylint: disable=import-error
from tty import setraw

CSI = "\x1b["


class Action(Enum):
    QUIT = ("\x1b", "Q")
    SELECT = (" ", "\r")
    UP = ("W", "\x00H", CSI + "A")
    DOWN = ("S", "\x00P", CSI + "B")
    RIGHT = ("D", "\x00M", CSI + "C")
    LEFT = ("A", "\x00K", CSI + "D")
    IGNORE = ()

    @property
    def inputs(self):
        return self.value


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


def _linux_getch() -> str:
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


def get_user_action() -> Action:
    """Convert keystroke into a game action. Linux-compatible version."""
    # only checked to work with keystrokes repr by 1 char, and the direction arrows

    user_input = _linux_getch()
    # Account for direction keys.
    if user_input == "\x1b":
        user_input += _linux_getch()
        user_input += _linux_getch()

    for action in Action:
        if user_input.upper() in action.inputs:
            return action
    return Action.IGNORE
