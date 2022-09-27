"""Tests for `squares.py`."""

from unittest import TestCase
from jchess.squares import Role

VALUE = {
    Role.KING: ("KING", 104),
    Role.QUEEN: ("QUEEN", 9),
    Role.ROOK: ("ROOK", 5),
    Role.BISHOP: ("BISHOP", 3),
    Role.KNIGHT: ("KNIGHT", 3),
    Role.PAWN: ("PAWN", 1),
    Role.NULL: ("NULL", 0),
}


class TestRole(TestCase):
    # tests also serve as a sort of regression test

    def test_value(self) -> None:
        for role in Role:
            self.assertEqual(role.val, VALUE[role][1])

    def test_str(self) -> None:
        for role in Role:
            self.assertEqual(str(role), VALUE[role][0])
