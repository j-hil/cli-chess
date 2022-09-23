"""Simple Vector class to facilitate easy coordinate translation."""

from typing import Union
from dataclasses import dataclass

VectorLike = Union["Vector", tuple[int, int]]


@dataclass
class Vector:
    """Represents 2D mathematical vector."""

    x: int
    y: int

    def __add__(self, other: VectorLike) -> "Vector":
        if isinstance(other, tuple):
            return Vector(self.x + other[0], self.y + other[1])
        return Vector(self.x + other.x, self.y + other.y)

    def in_bounds(self) -> bool:
        """Check if instance is on the chess board."""
        return self.x in range(8) and self.y in range(8)
