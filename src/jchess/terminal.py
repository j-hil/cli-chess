"""Suite of terminal manipulation functions.

Designed to abstract away all os/terminal dependencies from the rest of the code,
including the collection of player input in the form of an `Action`.
"""
import sys
from enum import Enum, auto


class Action(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    SELECT = auto()
    QUIT = auto()
    IGNORE = auto()


ESC = "\x1b"
CSI = ESC + "["
OSC = ESC + "]"


def clear():
    print(CSI + "2J")


def show_cursor():
    print(CSI + "?25h", end="")


def hide_cursor():
    # TODO: not working :(
    print(CSI + "?25l", end="")


def reset_console():
    # TODO: check in powershell
    print(CSI + "H")


try:
    from msvcrt import getch  # type: ignore

    ACTION_BYTES = {
        Action.QUIT: [b"\x1b", b"Q"],
        Action.SELECT: [b" ", b"\r"],
        Action.UP: [b"W", b"\x00H", b"\xe0H"],
        Action.DOWN: [b"S", b"\x00P", b"\xe0P"],
        Action.RIGHT: [b"D", b"\x00M", b"\xe0M"],
        Action.LEFT: [b"A", b"\x00K", b"\xe0K"],
    }

    def get_user_action() -> Action:
        """Convert keystroke into a game action. Windows-compatible version."""
        # only checked to work with keystrokes repr by 1 char, and the direction arrows

        user_input = getch()
        # Hex codes for direction arrows. NB *cannot* decode b"\xe0".
        if user_input in [b"\x00", b"\xe0"]:
            user_input += getch()

        for action in Action:
            if user_input.upper() in ACTION_BYTES.get(action, []):
                return action
        return Action.IGNORE

except ImportError:
    import tty
    from termios import tcsetattr, tcgetattr, TCSADRAIN  # type: ignore

    ACTION_CHARS = {
        Action.QUIT: ["\x1b", "Q"],
        Action.SELECT: [" ", "\r"],
        Action.UP: ["W", "\x00H", CSI + "A"],
        Action.DOWN: ["S", "\x00P", CSI + "B"],
        Action.RIGHT: ["D", "\x00M", CSI + "C"],
        Action.LEFT: ["A", "\x00K", CSI + "D"],
    }

    def _linux_getch() -> str:
        """Get a single character string from the user. Linux-compatible version."""
        # Based on https://stackoverflow.com/questions/71548267/. Somewhat magic to me.

        sys.stdout.flush()
        ch = ""
        fd = sys.stdin.fileno()
        old_settings = tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())  # type: ignore
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
            if user_input.upper() in ACTION_CHARS.get(action, []):
                return action
        return Action.IGNORE


if __name__ == "__main__":
    # crude testing script, not sure how to move into a unittest.
    x = ""
    while x != Action.QUIT:
        x = get_user_action()
        print(f"{x=}")
