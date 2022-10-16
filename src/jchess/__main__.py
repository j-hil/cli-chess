"""Program entry point; run as `python -m jchess`."""
import os
import colorama

from jchess import terminal
from jchess.terminal import get_user_action, Action
from jchess.configs import DEFAULT_CONFIG, VSC_CONFIG
from jchess.state import GameState

# attempt to detect that game is being run inside VS Code
DEV_MODE = os.environ.get("TERM_PROGRAM") == "vscode"


def main() -> None:
    """Entry point to begin game. Game state updated & re-printed with each input."""
    colorama.init()
    terminal.clear()
    terminal.resize(25, 87)
    terminal.reset_cursor()
    terminal.hide_cursor()

    game = GameState(DEFAULT_CONFIG if not DEV_MODE else VSC_CONFIG)
    print(game.ctrlseq)
    game.evolve_state(Action.IGNORE)
    print(game.ctrlseq)

    action = get_user_action()
    while action != Action.QUIT:
        game.evolve_state(action)
        print(game.ctrlseq)
        action = get_user_action()


if __name__ == "__main__":
    try:
        main()
    finally:
        terminal.clear()
        terminal.show_cursor()
