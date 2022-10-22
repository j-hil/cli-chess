"""Tests for `geometry.py`."""
from unittest import TestCase

from jchess.geometry import Vector


class TestVector(TestCase):
    def test_init(self) -> None:
        u = Vector(4, 2)
        self.assertEqual(u.x, 4)
        self.assertEqual(u.y, 2)

    def test_getitem(self) -> None:
        u = Vector(2, 7)
        self.assertEqual(u[0], 2)
        self.assertEqual(u[1], 7)
        with self.assertRaises(IndexError):
            u[-1]
        with self.assertRaises(IndexError):
            u[2]

    def test_add(self) -> None:
        self.assertEqual(Vector(1, 2) + Vector(5, 6), Vector(6, 8))
        self.assertEqual(Vector(-1, 11) + (1, 4), Vector(0, 15))

    def test_sub(self) -> None:
        self.assertEqual(Vector(1, 2) - Vector(5, 6), Vector(-4, -4))
        self.assertEqual(Vector(-1, 11) - (1, 4), Vector(-2, 7))

    def test_mul(self) -> None:
        self.assertEqual(2 * Vector(1, 2), Vector(2, 4))
        self.assertEqual(-3 * Vector(1, 2), Vector(-3, -6))

    def test_unpacking(self) -> None:
        self.assertEqual(Vector(*Vector(1, 2)), Vector(1, 2))
        self.assertEqual(Vector(*(1, 2)), Vector(1, 2))

    def test_equality(self) -> None:
        self.assertEqual(Vector(1, 2), (1, 2))
        self.assertIn(Vector(1, 2), [(1, 2), (3, 4)])
        self.assertIn((1, 2), [Vector(1, 2), Vector(3, 4)])
        self.assertFalse(Vector(1, 2) == object())

    def test_list_removal(self) -> None:

        array = [Vector(x, y) for x, y in ((1, 2), (3, 4), (5, 6), (7, 8))]
        for coord in array.copy():
            if coord.x == 3:
                array.remove(coord)
        self.assertEqual(array, [Vector(x, y) for x, y in ((1, 2), (5, 6), (7, 8))])

    def test_repr(self) -> None:
        self.assertEqual(repr(Vector(1, 2)), "V(1, 2)")
