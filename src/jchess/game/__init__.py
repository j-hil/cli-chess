"""Sub-package contains the core class of the game `GameState`.

`state` contains `GameState` while `display`, `engine` and `logic` contain functionality
to support `GameState`.

Basically it's included if it has the snippet, with the obvious addition of `state`.
>>> from typing import TYPE_CHECKING
... if TYPE_CHECKING:
...     from jchess.game.state import GameState
"""
