"""Tests for `geometry.py`."""
from pytest import raises

from jchess.geometry import V


def test_init() -> None:
    u = V(4, 2)
    assert (u.x, u.y) == (4, 2)


def test_getitem() -> None:
    u = V(2, 7)
    assert u[0] == 2
    assert u[1] == 7
    with raises(IndexError):
        u[2]


def test_add() -> None:
    assert V(1, 2) + V(5, 6) == V(6, 8)
    assert V(-1, 11) + V(1, 4) == V(0, 15)


def test_sub() -> None:
    assert V(1, 2) - V(5, 6) == V(-4, -4)
    assert V(-1, 11) - V(1, 4) == V(-2, 7)


def test_mul() -> None:
    assert 2 * V(1, 2) == V(2, 4)
    assert V(1, 2) * -3 == V(-3, -6)


def test_unpacking() -> None:
    assert V(*V(1, 2)) == V(1, 2)
    x, y = V(1, 2)
    assert (x, y) == (1, 2)
