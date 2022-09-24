"""The 'Engine' of the game - kicks things in motion."""

import os
from msvcrt import getch
from colorama import init
import psutil

from jchess.state import GameState
from jchess.display import MAIN_DISPLAY_SIZE


def get_one_key_input():
    r"""Get one key input from the console.

    The check for a second character is necessary as in VS Code's console the direction
    keys register as '\x00{c}' where `c` is some capital letter.
    """
    char1 = getch().decode()
    char2 = getch().decode() if char1 == "\x00" else ""
    return char1 + char2


def hide_cursor():
    """Hide the terminal's cursor using ANSI codes."""
    print("\033[?25l", end="")


def show_cursor():
    """Show the terminal's cursor using ANSI codes."""
    print("\033[?25h", end="")


def reset_cursor():
    """Move the cursor up by the number of lines displayed. Next print occurs there.

    This is used instead of `os.system('cls')` which creates an 'flickering' effect.
    """
    print(f"\033[{MAIN_DISPLAY_SIZE.rows}A\033[2K", end="")


def main():
    """Entry point to begin the game.

    The game state is updated and re-printed after each keystroke.
    """
    init()
    os.system("cls")
    hide_cursor()

    game = GameState()
    while not game.quitting:
        reset_cursor()
        hide_cursor()
        print(game)
        key = get_one_key_input()
        game.process_input_key(key)
    show_cursor()


if __name__ == "__main__":
    # getting shell experention
    # parent_pid = os.getppid()
    # process_name = psutil.Process(parent_pid).parent().name()
    # print(f"{parent_pid=}")
    # print(f"{process_name=}")
    # quit()
    try:
        main()
    except Exception:
        os.system("cls")
        raise

