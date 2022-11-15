"""Suite of terminal manipulation functions.

Designed to abstract away all os/terminal dependencies from the rest of the code,
including the collection of player input.
"""
import sys
from signal import CTRL_BREAK_EVENT

from colorama import Style

from jchess.geometry import V

if sys.platform == "win32":
    from ._windows import clear, get_input, hide_cursor, resize, show_cursor
else:
    from ._linux import clear, get_input, hide_cursor, resize, show_cursor

__all__ = [
    "clear",
    "resize",
    "show_cursor",
    "hide_cursor",
    "ctrlseq",
    "reset_cursor",
    "get_input",
]

CSI = "\x1b["


def reset_cursor() -> None:
    print(f"{CSI}H", end="")


def ctrlseq(
    s: str, *, clr: str = "", at: tuple[int, int] | V, edge: bool = False
) -> str:
    """Convert a string to a control sequence."""
    lines = s.split("\n")
    w, h = len(lines[0]), len(lines)
    x, y = at

    reset_clr = Style.RESET_ALL
    seq = clr + "".join(f"{CSI}{y+i};{x}H{l}" for i, l in enumerate(lines)) + reset_clr

    if edge:
        boundary = [
            ctrlseq("-" * w, at=(x, y - 1)),
            ctrlseq("-" * w, at=(x, y + h)),
            ctrlseq("\n".join("|" for _ in range(h)), at=(x - 1, y)),
            ctrlseq("\n".join("|" for _ in range(h)), at=(x + w, y)),
            ctrlseq("+", at=(x - 1, y - 1)),
            ctrlseq("+", at=(x - 1, y + h)),
            ctrlseq("+", at=(x + w, y - 1)),
            ctrlseq("+", at=(x + w, y + h)),
        ]
        seq += "".join(boundary)
    return seq


if __name__ == "__main__":
    # crude testing script, not obvious how to move into a unittest.
    while (a := get_input()) != "\x1b":
        print(f"{a=}")
