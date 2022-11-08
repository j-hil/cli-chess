"""Program entry point; run `jchess` in the command line."""

from jchess.display import DEFAULT_PALLET, DEFAULT_SYMBOLS, Display
from jchess.game import Game


def run() -> None:
    """Entry point to begin game. Game state then visuals updated with each input."""

    game = Game()
    with Display(game, DEFAULT_PALLET, DEFAULT_SYMBOLS) as display:
        while True:
            display.refresh()
            game.evolve_state()
