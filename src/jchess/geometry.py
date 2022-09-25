"""Simple Vector class to facilitate easy coordinate translation."""

from typing import Union
from dataclasses import dataclass

VectorLike = Union["Vector", tuple[int, int]]


@dataclass
class Vector:
    """Represents 2D mathematical vector with integer components."""

    x: int
    y: int

    def __add__(self, other: VectorLike) -> "Vector":
        if isinstance(other, tuple):
            return Vector(self.x + other[0], self.y + other[1])
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: VectorLike) -> "Vector":
        if isinstance(other, tuple):
            return Vector(self.x - other[0], self.y - other[1])
        return Vector(self.x - other.x, self.y - other.y)
