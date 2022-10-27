import functools
from typing import Callable
from unittest.mock import patch

from jchess.action import Action
from jchess.state import GameState

ACTION_LOOKUP = {action.value: action for action in Action}


def patch_inputs(cmdstr: str):
    actions = [ACTION_LOOKUP[c] for c in cmdstr.split()]

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        @patch("jchess.state.GameState.get_action")
        def wrapper(self, mock_get_action):
            mock_get_action.side_effect = actions
            game = GameState()
            for _ in actions:
                game.evolve_state()
            return func(self, game)

        return wrapper

    return decorator
