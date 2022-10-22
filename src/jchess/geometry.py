"""Simple Vector class to facilitate easy coordinate translation.

Designed to be interchangeable with tuple wherever possible.
"""

from typing import Any, Iterator, Union


class Vector:
    """Represents 2D mathematical vector with integer components."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError(f"{index=} should be 0 or 1.")

    def __add__(self, other: "VectorLike") -> "Vector":
        return Vector(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other: "VectorLike") -> "Vector":
        return Vector(self.x - other[0], self.y - other[1])

    def __mul__(self, other: int) -> "Vector":
        return Vector(other * self.x, other * self.y)

    __rmul__ = __mul__

    def __mod__(self, modulus: int) -> "Vector":
        return Vector(self.x % modulus, self.y % modulus)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, (Vector, tuple)):
            return NotImplemented
        return self[0] == other[0] and self[1] == other[1] and len(self) == len(other)

    def __iter__(self) -> Iterator[int]:
        return (z for z in [self.x, self.y])

    def __repr__(self) -> str:
        return f"V({self.x}, {self.y})"

    def __len__(self) -> int:
        return 2


# Conveniences for typing
VectorLike = Union[Vector, tuple[int, int]]
Vectors = list[Vector]
