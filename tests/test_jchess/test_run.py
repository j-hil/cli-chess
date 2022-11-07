from unittest.mock import DEFAULT, Mock, patch

from pytest import raises

import jchess.game
import jchess.run
from jchess.action import Action
from jchess.run import run


@patch.multiple(jchess.run, os=DEFAULT, terminal=DEFAULT, print=DEFAULT)
@patch.multiple(jchess.game, input=DEFAULT)
@patch.multiple(jchess.run.Game, get_action=DEFAULT)  # type: ignore
def _test_run(
    get_action: Mock, input: Mock, print: Mock, terminal: Mock, os: Mock
) -> None:
    get_action.side_effect = list(Action)  # relies on order of Action
    with raises(SystemExit):
        run()

    assert get_action.call_count == len(Action)
    assert print.call_count == len(Action) + 1


def test_run() -> None:
    # I don't know why, but it is necessary to wrap the patched function
    _test_run()
