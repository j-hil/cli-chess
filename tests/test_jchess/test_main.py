from unittest import TestCase
from unittest.mock import DEFAULT, patch

import jchess
from jchess.action import Action


class TestMain(TestCase):
    """Smoke test for main script."""

    # mocked to simulate player
    @patch("jchess.GameState.get_action")
    # mocked to prevent writing to stdout
    @patch.multiple("jchess", os=DEFAULT, terminal=DEFAULT, print=DEFAULT)
    def test_main(self, get_action, print, terminal, os):
        get_action.side_effect = list(Action)  # relies on order of Action
        with self.assertRaises(SystemExit):
            jchess.run()

        self.assertEqual(get_action.call_count, len(Action))
        self.assertEqual(print.call_count, len(Action))
