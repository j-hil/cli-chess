from unittest import TestCase
from unittest.mock import DEFAULT, patch

from jchess.__main__ import main as jchess_main
from jchess.terminal import Action


class TestMain(TestCase):
    @patch.multiple(
        "jchess.__main__",
        get_user_action=DEFAULT,  # mocked to simulate player
        os=DEFAULT,  # this and bellow are mocked to prevent writing to stdout
        terminal=DEFAULT,
        print=DEFAULT,
    )
    def test_main(self, print, terminal, os, get_user_action):
        get_user_action.side_effect = [Action.IGNORE, Action.QUIT]
        jchess_main()

        self.assertEqual(get_user_action.call_count, 2)
        self.assertEqual(print.call_count, 3)
