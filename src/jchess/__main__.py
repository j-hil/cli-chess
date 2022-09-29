"""Program entry point.

Can be run as `python -m jchess`.
"""
import os
import sys
from colorama import init
from psutil import Process

from jchess.game.state import GameState
from jchess.game.visuals import MAIN_DISPLAY_ROWS
from jchess.configs import CONFIG, VSC_CONFIG

# attempt to detect that game is being run inside VS Code
DEV_MODE = "debugpy" in sys.modules


def main() -> None:
    """Entry point to begin game. Game state updated & re-printed with each input."""
    # enable colors, clear the screen, and hide the cursor
    init()
    os.system("cls")
    print("\033[?25l", end="")

    if DEV_MODE:
        config = VSC_CONFIG
    else:
        # TODO: need psutil for this one line. would be nice to remove that dependency
        shell = Process(os.getpid()).parent().name()
        config = CONFIG.get(shell, VSC_CONFIG)

    game = GameState(config)
    while True:
        print(f"\033[{MAIN_DISPLAY_ROWS}A\033[2K", end="")  # reset cursor position
        print(game)
        game.evolve_state()


if __name__ == "__main__":
    try:
        main()
    finally:
        os.system("cls")
        print("\033[?25h", end="")  # show cursor
