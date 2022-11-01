import sys

assert sys.platform == "win32"

import ctypes
import os
from msvcrt import getch

KERNEL32 = ctypes.windll.kernel32


class _CursorInfo(ctypes.Structure):
    # taken from https://stackoverflow.com/questions/5174810/

    visible: bool  # a white lie for pylint
    _fields_ = [("size", ctypes.c_int), ("visible", ctypes.c_byte)]


def _show_cursor(visible: bool) -> None:
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


def get_input() -> str:
    """Convert keystroke into a char. Windows-compatible version."""
    # only checked to work with keystrokes represented by 1 char and direction arrows

    user_input = getch()

    # Hex codes for direction arrows. NB: *cannot* decode b"\xe0".
    if user_input in [b"\x00", b"\xe0"]:
        return {b"H": "↑", b"P": "↓", b"M": "→", b"K": "←", b"O": "⇲"}[getch()]

    # Anything else is assumed to be a represented by a single decodable char
    return user_input.decode()
