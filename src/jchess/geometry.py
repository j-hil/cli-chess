"""Simple Vector class to facilitate easy coordinate translation.

Designed to be interchangeable with tuple wherever possible.
"""
from typing import Callable

# Conveniences for typing
VectorLike = tuple[int, int]
Vectors = list["Vector"]


class Vector(tuple[int, int]):
    """Represents 2D mathematical vector with integer components."""

    def __new__(cls: type["Vector"], x: int, y: int) -> "Vector":
        return super().__new__(cls, (x, y))  # type: ignore[arg-type]

    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = x, y
        super().__init__()

    def __add__(self, other: VectorLike) -> "Vector":  # type: ignore[override]
        return Vector(self[0] + other[0], self[1] + other[1])

    __radd__ = __add__

    def __sub__(self, other: VectorLike) -> "Vector":
        return Vector(self[0] - other[0], self[1] - other[1])

    def __rsub__(self, other: VectorLike) -> "Vector":
        return Vector(other[0] - self[0], other[1] - self[1])

    def __mul__(self, other: int) -> "Vector":  #  type: ignore[override]
        return Vector(other * self.x, other * self.y)

    __rmul__: Callable[["Vector", int], "Vector"] = __mul__

    def __mod__(self, modulus: int) -> "Vector":
        return Vector(self.x % modulus, self.y % modulus)

    def __repr__(self) -> str:
        return "V" + super().__repr__()
