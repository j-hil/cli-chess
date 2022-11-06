"""Simple Vector class to facilitate easy coordinate translation.

Designed to be interchangeable with tuple wherever possible.
"""

from dataclasses import dataclass
from typing import Iterator, TypeAlias


@dataclass(slots=True, frozen=True)
class V:
    """Simple 2D vector with integer components."""

    x: int
    y: int

    def __add__(self, other: "V") -> "V":
        return V(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "V") -> "V":
        return V(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int) -> "V":
        return V(self.x * other, self.y * other)

    # typing doesn't seem to like the simpler `__rmul__ = __mul__`
    def __rmul__(self, other: int) -> "V":
        return V(other * self.x, other * self.y)

    def __mod__(self, other: int) -> "V":
        return V(self.x % other, self.y % other)

    def __getitem__(self, index: int) -> int:
        return (self.x, self.y)[index]

    def __iter__(self) -> Iterator[int]:
        return iter((self.x, self.y))

    def __repr__(self) -> str:
        return V.__name__ + f"({self.x}, {self.y})"


# Conveniences for typing
Vector: TypeAlias = "V"
VectorSet = set[V]
