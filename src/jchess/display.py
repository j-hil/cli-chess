"""Printing `GameState` information.

Contains helper functions to:
* process `GameState` information into readable & pretty strings. In principle these
could be methods but it's convenient to have them here.
* combine said strings according to desired relative positions

I think a lot of the manipulations of the display could probably be simplified with the
built in `curses` module which I was unaware of when I begin this project.

DisplayArray is used (rather than using an array of strings) as colorization
characters (eg Fore.BLACK) become difficult to place.
"""
from dataclasses import dataclass
from jchess.geometry import Vector, VectorLike


class DisplayArray:
    """An array of arrays of strings, but the strings should be a single printable char.

    Designed to work with `Vector` and have mutable elements. Length of strings not
    enforced.
    """

    def __init__(self, string: str):
        """Initialize a `DisplayArray`.

        :param string: Each line becomes a row, and each character in a line becomes an
            element of it's corresponding row.
        :raises ValueError: Each line must be of equal length.
        """
        row_len = string.find("\n")
        row_len = row_len if row_len > 0 else len(string)
        rows = []
        for row in string.split("\n"):
            if len(row) != row_len:
                raise ValueError("Each line in `string` must be of equal length.")
            rows.append(list(row))
        self.rows = rows

    @property
    def n_rows(self):
        return len(self.rows)

    @property
    def n_cols(self):
        return len(self.rows[0])

    def __getitem__(self, position: VectorLike) -> str:
        if isinstance(position, tuple):
            return self.rows[position[1]][position[0]]
        return self.rows[position.y][position.x]

    def __setitem__(self, position: Vector, value: str) -> None:
        self.rows[position.y][position.x] = value

    def __str__(self) -> str:
        return "\n".join("".join(c for c in row) for row in self.rows)

    def merge_in(self, other: "DisplayArray", *, at: VectorLike) -> None:
        """Merge another `DisplayArray` into this one.

        :param other: Display to merge into the current one
        :param at: Coordinate to start the merge at (top-left corner)
        :raises ValueError: If `other` display doesn't fit inside `self` from `at`
        """
        translation = Vector(*at) if isinstance(at, tuple) else at

        w, h = self.n_cols - translation.x, self.n_rows - translation.y
        if w < other.n_cols or h < other.n_rows:
            raise ValueError("The incoming display must fit in the allocated space")

        for i in range(other.n_rows):
            for j in range(other.n_cols):
                old_position = Vector(j, i)
                new_position = old_position + translation
                self[new_position] = other[old_position]
