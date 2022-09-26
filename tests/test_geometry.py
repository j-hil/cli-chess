from unittest import TestCase
from jchess.geometry import Vector


class TestVector(TestCase):

    def test_init(self):
        u = Vector(4, 2)
        self.assertEqual(u.x, 4)
        self.assertEqual(u.y, 2)

    def test_add(self):
        self.assertEqual(Vector(1, 2) + Vector(5, 6), Vector(6, 8))
        self.assertEqual(Vector(-1, 11) + (1, 4), Vector(0, 15))

    def test_sub(self):
        self.assertEqual(Vector(1, 2) - Vector(5, 6), Vector(-4, -4))
        self.assertEqual(Vector(-1, 11) - (1, 4), Vector(-2, 7))



