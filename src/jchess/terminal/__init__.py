"""Suite of terminal manipulation functions.

Designed to abstract away all os/terminal dependencies from the rest of the code,
including the collection of player input in the form of an `Action`.
"""
import os


if os.name == "nt":
    from ._windows import (
        Action,
        get_user_action,
        clear,
        resize,
        show_cursor,
        hide_cursor,
    )
else:
    from ._linux import (
        Action,
        get_user_action,
        clear,
        resize,
        show_cursor,
        hide_cursor,
    )


def reset_cursor():
    print("\x1b[H")


if __name__ == "__main__":
    # crude testing script, not sure how to move into a unittest.
    x = None
    while x != Action.QUIT:
        x = get_user_action()
        print(f"{x=}")
