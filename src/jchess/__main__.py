"""Program entry point.

Can be run as `python -m jchess`.
"""
import os
import sys
import colorama
from psutil import Process

from jchess.configs import CONFIG, VSC_CONFIG
from jchess import terminal
from jchess.game.state import GameState

# attempt to detect that game is being run inside VS Code
DEV_MODE = "debugpy" in sys.modules


def main() -> None:
    """Entry point to begin game. Game state updated & re-printed with each input."""
    colorama.init()
    terminal.clear()
    terminal.hide_cursor()

    if DEV_MODE:
        config = VSC_CONFIG
    else:
        # TODO: need psutil for this one line. would be nice to remove that dependency
        shell = Process(os.getpid()).parent().name()
        config = CONFIG.get(shell, VSC_CONFIG)

    game = GameState(config)
    while True:
        terminal.reset_cursor()
        print(game)
        game.evolve_state()


if __name__ == "__main__":
    try:
        main()
    finally:
        terminal.clear()
        terminal.show_cursor()
