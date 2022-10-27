"""Program entry point; run `jchess` in the command line."""
import os

import colorama

from jchess import terminal
from jchess.configs import DEFAULT_PALLET, DEFAULT_SYMBOLS
from jchess.display import Display
from jchess.state import GameState


def run() -> None:
    """Entry point to begin game. Game state updated & re-printed with each input."""

    original_size = os.get_terminal_size()
    try:
        colorama.init()
        terminal.clear()
        terminal.resize(87, 25)
        terminal.reset_cursor()
        terminal.hide_cursor()

        display = Display(DEFAULT_PALLET, DEFAULT_SYMBOLS)
        game = GameState()
        while True:
            print(display.ctrlseq(game))
            game.evolve_state()

    finally:
        terminal.clear()
        terminal.show_cursor()
        terminal.resize(*original_size)
