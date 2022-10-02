"""Tests for `geometry.py`."""

from unittest import TestCase
from jchess.geometry import Vector


class TestVector(TestCase):
    def test_init(self) -> None:
        u = Vector(4, 2)
        self.assertEqual(u.x, 4)
        self.assertEqual(u.y, 2)

    def test_add(self) -> None:
        self.assertEqual(Vector(1, 2) + Vector(5, 6), Vector(6, 8))
        self.assertEqual(Vector(-1, 11) + (1, 4), Vector(0, 15))

    def test_sub(self) -> None:
        self.assertEqual(Vector(1, 2) - Vector(5, 6), Vector(-4, -4))
        self.assertEqual(Vector(-1, 11) - (1, 4), Vector(-2, 7))

    def test_unpacking(self) -> None:
        self.assertEqual(Vector(*Vector(1,2)), Vector(1,2))
        self.assertEqual(Vector(*(1,2)), Vector(1,2))

    def test_equality(self) -> None:
        self.assertEqual(Vector(1, 2), (1, 2))
        self.assertTrue(Vector(1, 2) in [(1, 2), (3, 4)])
        self.assertTrue((1, 2) in [Vector(1, 2), Vector(3, 4)])
