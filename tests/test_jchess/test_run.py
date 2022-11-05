from unittest import TestCase
from unittest.mock import DEFAULT, Mock, patch

import jchess.run
from jchess.action import Action
from jchess.run import run


class TestMain(TestCase):
    """Smoke test for main script."""

    @patch.multiple(jchess.run.Game, get_action=DEFAULT)  # type: ignore
    @patch.multiple(jchess.run, os=DEFAULT, terminal=DEFAULT, print=DEFAULT)
    def test_run(self, get_action: Mock, print: Mock, terminal: Mock, os: Mock) -> None:
        get_action.side_effect = list(Action)  # relies on order of Action
        with self.assertRaises(SystemExit):
            run()

        self.assertEqual(get_action.call_count, len(Action))
        self.assertEqual(print.call_count, len(Action))
