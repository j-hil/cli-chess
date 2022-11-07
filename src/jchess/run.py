"""Program entry point; run `jchess` in the command line."""

import os

import colorama

from jchess import terminal
from jchess.display import DEFAULT_PALLET, DEFAULT_SYMBOLS, Display
from jchess.game import Game


def run() -> None:
    """Entry point to begin game. Game state then visuals updated with each input."""

    original_size = os.get_terminal_size()
    try:
        colorama.init()
        terminal.clear()
        terminal.resize(87, 25)
        terminal.reset_cursor()
        terminal.hide_cursor()

        display = Display(DEFAULT_PALLET, DEFAULT_SYMBOLS)
        game = Game()
        while True:
            print(display.ctrlseq(game))
            game.evolve_state()

    finally:
        terminal.clear()
        terminal.show_cursor()
        terminal.resize(*original_size)
