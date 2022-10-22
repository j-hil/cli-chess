from msvcrt import getch
import ctypes
from enum import Enum
import os

KERNEL32 = ctypes.windll.kernel32


class Action(Enum):
    QUIT = (b"\x1b", b"Q")
    SELECT = (b" ", b"\r")
    UP = (b"W", b"\x00H", b"\xe0H")
    DOWN = (b"S", b"\x00P", b"\xe0P")
    RIGHT = (b"D", b"\x00M", b"\xe0M")
    LEFT = (b"A", b"\x00K", b"\xe0K")
    IGNORE = ()

    @property
    def inputs(self):
        return self.value


class _CursorInfo(ctypes.Structure):
    # taken from https://stackoverflow.com/questions/5174810/

    visible: bool  # a white lie for pylint
    _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]


def _show_cursor(visible: bool):
    ci = _CursorInfo()
    handle = KERNEL32.GetStdHandle(-11)
    KERNEL32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
    ci.visible = visible
    KERNEL32.SetConsoleCursorInfo(handle, ctypes.byref(ci))


def clear() -> None:
    os.system("cls")


def resize(w: int, h: int) -> None:
    os.system(f"mode con: cols={w} lines={h}")


def show_cursor() -> None:
    _show_cursor(True)


def hide_cursor() -> None:
    _show_cursor(False)


def get_user_action() -> Action:
    """Convert keystroke into a game action. Windows-compatible version."""
    # only checked to work with keystrokes repr by 1 char, and the direction arrows

    user_input = getch()
    # Hex codes for direction arrows. NB *cannot* decode b"\xe0".
    if user_input in [b"\x00", b"\xe0"]:
        user_input += getch()

    for action in Action:
        if user_input.upper() in action.inputs:
            return action
    return Action.IGNORE
