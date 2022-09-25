"""The 'Engine' of the game - kicks things in motion."""

import os
from msvcrt import getch
import sys
from warnings import warn

from colorama import init
from psutil import Process

from jchess.state import GameState
from jchess.display import MAIN_DISPLAY_SIZE
from jchess.configs import CMD_CONFIG, PS_CONFIG, VSC_CONFIG

# attempt to detect that game is being run inside VS Code
DEV_MODE = "debugpy" in sys.modules


def get_one_key_input() -> str:
    r"""Get one key input from the console.

    The check for a second character is necessary as in VS Code's console the direction
    keys register as '\x00{c}' where `c` is some capital letter.
    """
    char1 = getch().decode()
    char2 = getch().decode() if char1 == "\x00" else ""
    return char1 + char2


def hide_cursor() -> None:
    """Hide the terminal's cursor using ANSI codes."""
    print("\033[?25l", end="")


def show_cursor() -> None:
    """Show the terminal's cursor using ANSI codes."""
    print("\033[?25h", end="")


def reset_cursor() -> None:
    """Move the cursor up by the number of lines displayed. Next print occurs there.

    This is used instead of `os.system('cls')` which creates an 'flickering' effect.
    """
    print(f"\033[{MAIN_DISPLAY_SIZE.rows}A\033[2K", end="")

def get_shell_name() -> str:
    # get parent's parent as if in venv parent is python
    return Process(os.getpid()).parent().name()


def main() -> None:
    """Entry point to begin the game.

    The game state is updated and re-printed after each keystroke.
    """
    init()
    os.system("cls")
    hide_cursor()


    if DEV_MODE:
        config = VSC_CONFIG
    else:
        shell = get_shell_name()
        if shell == "cmd.exe":
            config = CMD_CONFIG
        elif shell == "powershell.exe":
            config = PS_CONFIG
        else:
            config = VSC_CONFIG
            warn(f"Shell {shell} not supported/recognized. Defaulting to VSC_CONFIG")

    game = GameState(config)
    while not game.quitting:
        reset_cursor()
        hide_cursor()
        print(game)
        key = get_one_key_input()
        game.process_input_key(key)
    show_cursor()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        os.system("cls")
        raise
