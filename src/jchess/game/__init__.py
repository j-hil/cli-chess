"""Sub-package contains the core class of the game `GameState`.

File `state.py` contains `GameState` itself,,  while `display.py`, `engine.py` and
`logic.py` contain functionality to support `GameState`.

Rule of thumb: a file should be in here if it includes the following snippet:
>>> from typing import TYPE_CHECKING
... if TYPE_CHECKING:
...     from jchess.game.state import GameState
"""
