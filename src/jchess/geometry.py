"""Simple Vector class to facilitate easy coordinate translation.

Cleaner code examples:

>>> delta in [Vector(1, 2), Vector(3, 4)]
becomes
>>> delta in [(1, 2), (3, 4)]

>>> delta = Vector(1, 2) - Vector(3, 4)
becomes
>>> delta = piece.coord

>>> x = array[Vector(1, 2)]
becomes (if facilitated by the type(array))
>>> x = array[1, 2]
"""

from typing import Any, Iterator, Union

# Vector is designed to be interchangeable with a tuple where possible.
VectorLike = Union["Vector", tuple[int, int]]


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

    def __add__(self, other: VectorLike) -> "Vector":
        return Vector(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other: VectorLike) -> "Vector":
        return Vector(self[0] - other[0], self[1] - other[1])

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, (Vector, tuple)):
            return NotImplemented
        return self[0] == other[0] and self[1] == other[1] and len(self) == len(other)

    def __iter__(self) -> Iterator[int]:
        return (z for z in [self.x, self.y])

    def __str__(self) -> str:
        return f"V({self.x}, {self.y})"

    def __len__(self) -> int:
        return 2
