"""Program entry point.

Can be run as `python -m jchess`.
"""
import os
import colorama
from psutil import Process

from jchess.configs import CONFIG, DEFAULT_CONFIG, VSC_CONFIG
from jchess import terminal
from jchess.state import GameState

# attempt to detect that game is being run inside VS Code
DEV_MODE = os.environ.get("TERM_PROGRAM") == "vscode"


def main() -> None:
    """Entry point to begin game. Game state updated & re-printed with each input."""
    colorama.init()
    terminal.clear()
    terminal.resize(26, 88)
    terminal.reset_cursor()
    terminal.hide_cursor()

    if DEV_MODE:
        config = VSC_CONFIG
    else:
        # TODO: need psutil for this one line. would be nice to remove that dependency
        shell = Process(os.getppid()).name()
        config = CONFIG.get(shell, DEFAULT_CONFIG)

    game = GameState(config)
    while True:
        print(game, end="")
        game.evolve_state()
        terminal.reset_cursor()


if __name__ == "__main__":
    try:
        main()
    finally:
        terminal.clear()
        terminal.show_cursor()
