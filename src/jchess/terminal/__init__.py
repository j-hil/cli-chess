"""Suite of terminal manipulation functions.

Designed to abstract away all os/terminal dependencies from the rest of the code,
including the collection of player input in the form of an `Action`.
"""

import os

from colorama import Style

__all__ = [
    "clear",
    "resize",
    "show_cursor",
    "hide_cursor",
    "ctrlseq",
    "reset_cursor",
    "get_input",
]

if os.name == "nt":
    from ._windows import clear, get_input, hide_cursor, resize, show_cursor
else:
    from ._linux import clear, get_input, hide_cursor, resize, show_cursor

CSI = "\x1b["


def reset_cursor() -> None:
    print(f"{CSI}H", end="")


def ctrlseq(s: str, *, clr: str = "", at: tuple[int, int]) -> str:
    """Convert a string to a control sequence."""
    x, y = at
    return (
        f"{CSI}{y};{x}H"
        + clr
        + f"\n{CSI}{x-1}C".join(s.split("\n"))  # why is it x - 1...?
        + Style.RESET_ALL
    )


if __name__ == "__main__":
    # crude testing script, not sure how to move into a unittest.
    a = None
    while a != "\x1b":
        a = get_input()
        print(f"{a=}")
