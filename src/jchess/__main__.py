"""Program entry point.

Can be run as `python -m jchess`.
"""
import os
import colorama

from jchess.configs import DEFAULT_CONFIG, VSC_CONFIG
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

    game = GameState(DEFAULT_CONFIG if not DEV_MODE else VSC_CONFIG)
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
