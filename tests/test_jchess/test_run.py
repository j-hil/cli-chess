from unittest.mock import DEFAULT, Mock, patch

import jchess.display._class
import jchess.game
import jchess.run
from jchess.action import Action
from jchess.run import run


@patch.multiple(jchess.display._class, os=DEFAULT, terminal=DEFAULT, print=DEFAULT)
@patch.multiple(jchess.run.Game, get_action=DEFAULT)  # type: ignore
def _test_run(get_action: Mock, print: Mock, terminal: Mock, os: Mock) -> None:
    get_action.side_effect = list(Action) + [Action.IGNORE]
    run()

    assert get_action.call_count == len(Action) + 1
    assert print.call_count == len(Action) + 1


def test_run() -> None:
    # I don't know why, but it is necessary to wrap the patched function
    _test_run()
