"""Tests for `geometry.py`."""
from unittest import TestCase

from jchess.geometry import V


class TestVector(TestCase):
    def test_init(self) -> None:
        u = V(4, 2)
        self.assertEqual(u.x, 4)
        self.assertEqual(u.y, 2)

    def test_getitem(self) -> None:
        u = V(2, 7)
        self.assertEqual(u[0], 2)
        self.assertEqual(u[1], 7)
        with self.assertRaises(IndexError):
            u[2]

    def test_add(self) -> None:
        self.assertEqual(V(1, 2) + V(5, 6), V(6, 8))
        self.assertEqual(V(-1, 11) + V(1, 4), V(0, 15))

    def test_sub(self) -> None:
        self.assertEqual(V(1, 2) - V(5, 6), V(-4, -4))
        self.assertEqual(V(-1, 11) - V(1, 4), V(-2, 7))

    def test_mul(self) -> None:
        self.assertEqual(2 * V(1, 2), V(2, 4))
        self.assertEqual(V(1, 2) * -3, V(-3, -6))

    def test_unpacking(self) -> None:
        self.assertEqual(V(*V(1, 2)), V(1, 2))
        x, y = V(1, 2)
        self.assertEqual((x, y), (1, 2))
