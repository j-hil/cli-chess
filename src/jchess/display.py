"""Class for manipulating 2D arrays of displayable characters.

Provides the following extra features over a usual array of strings:
* Each element is a *displayable* character (rather than potentially a character of
zero length like a color.
* Basic formatting which is agnostic to rows and columns (see `merge_in`)
* Compatible with `geometry.Vector`.
"""
# TODO: Introduce a printable-char class
from itertools import product
from jchess.geometry import Vector, VectorLike


class DisplayArray:
    """An array of arrays of displayable characters."""

    def __init__(self, string: str):
        """Initialize a `DisplayArray`.

        :param string: Each line becomes a row, and each character in a line becomes an
            element of it's corresponding row.
        :raises ValueError: Each line must be of equal length.
        """
        row_len = string.find("\n")
        row_len = row_len if row_len > 0 else len(string)
        rows = []
        for i, row in enumerate(string.split("\n")):
            if len(row) != row_len:
                raise ValueError(INVALID_INPUT_MSG.format(i, row, row_len, len(row)))
            rows.append(list(row))
        self.rows = rows

    @property
    def n_rows(self) -> int:
        return len(self.rows)

    @property
    def n_cols(self) -> int:
        return len(self.rows[0])

    def __getitem__(self, position: VectorLike) -> str:
        if isinstance(position, tuple):
            return self.rows[position[1]][position[0]]
        return self.rows[position.y][position.x]

    def __setitem__(self, position: VectorLike, value: str) -> None:
        if isinstance(position, tuple):
            self.rows[position[1]][position[0]] = value
        else:
            self.rows[position.y][position.x] = value

    def __str__(self) -> str:
        return "\n".join("".join(c for c in row) for row in self.rows)

    def merge_in(self, other: "DisplayArray", *, anchor: str) -> None:
        """Merge another `DisplayArray` into this one.

        :param other: Display to merge into the current one
        :param anchor: Merge occurs at first occurrence of `anchor`(top-left corner)
        :raises ValueError: If `other` display doesn't fit inside `self` from `at`
        """
        n_cols, n_rows = self.n_cols, self.n_rows
        for i, j in product(range(n_rows), range(n_cols)):
            index = Vector(j, i)
            if self[index] == anchor:
                break
        else:
            raise IndexError(f"{anchor=} not found.")

        w, h = n_cols - index.x, n_rows - index.y
        if w < other.n_cols or h < other.n_rows:
            raise ValueError("The consumed display must fit in the allocated space")

        for i, j in product(range(other.n_rows), range(other.n_cols)):
            old_position = Vector(j, i)
            new_position = old_position + index
            self[new_position] = other[old_position]


INVALID_INPUT_MSG = """\
Each line in `string` must be of equal length.
    Problem in row {}: {}.
    Expected len(row)={}, got {}.
"""
