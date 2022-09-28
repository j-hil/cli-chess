"""Creates a class containing the bulk of the logic and complexity of the game."""
# TODO: remove as many tooling 'ignores' as possible

from typing_extensions import Self
from jchess.game.logic import defending_coords_
from jchess.geometry import Vector
from jchess.squares import Square, Player, Role
from jchess.configs import Config, VSC_CONFIG
from jchess.game.engine import Mode, NULL_SQUARE, NOT_SELECTED_SQUARE, NOT_SELECTED_COORD, evolve_state_
from jchess.game.visuals import generate_main_display

K, Q, R, B, N, P, _ = Role  # type: ignore  # pylint: disable=invalid-name


class GameState:
    """Represents the state of the game, and controls the game logic."""

    @staticmethod
    def has_coord(coord: Vector) -> bool:
        return coord.x in range(8) and coord.y in range(8)

    def __init__(self, config: Config = VSC_CONFIG):
        """Initialise a `GameState`.

        :param config: Controls settings such as color, symbols etc. Several pre-made
            configs available in jchess.config. Defaults to VS_CODE_CONFIG
        """
        self.board: list[list[Square]] = [
            [Square(role, Player.TWO) for role in [R, N, B, Q, K, B, N, R]],  # type: ignore  # pylint: disable=line-too-long
            [Square(P, Player.TWO) for _ in range(8)],  # type: ignore
            *[[NULL_SQUARE for _ in range(8)] for _ in range(4)],
            [Square(P, Player.ONE) for _ in range(8)],  # type: ignore
            [Square(role, Player.ONE) for role in [R, N, B, Q, K, B, N, R]],  # type: ignore  # pylint: disable=line-too-long
        ]
        self.config: Config = config

        self.highlighted_coord: Vector = Vector(4, 7)
        self.selected_coord: Vector = NOT_SELECTED_COORD

        self.player: Player = Player.ONE

        self.taken_pieces: dict[Player, list[Role]] = {Player.ONE: [], Player.TWO: []}
        self.mode: Mode = Mode.ONE

    @property
    def selected(self) -> Square:
        """Square currently selected by the active player, if any."""
        if self.selected_coord is NOT_SELECTED_COORD:
            return NOT_SELECTED_SQUARE
        return self[self.selected_coord]

    @selected.setter
    def selected(self, value: Square) -> None:
        if value is NOT_SELECTED_SQUARE:
            self.selected_coord = NOT_SELECTED_COORD
        else:
            self[self.selected_coord] = value

    @property
    def highlighted(self) -> Square:
        """Square which the game cursor is currently highlighting."""
        piece = self[self.highlighted_coord]
        if piece is None:
            raise RuntimeError(f"{self.highlighted_coord=} should always be in bounds.")
        return piece

    @highlighted.setter
    def highlighted(self, value: Square) -> None:
        self[self.highlighted_coord] = value

    def score(self, player: Player) -> int:
        return sum(x.val for x in self.taken_pieces[player])

    def is_defending(self, coord: Vector, against: Vector) -> bool:
        """Check if the square at the input coord is defending against the attacker."""
        return coord in self.defending_coords(against)

    def defending_coords(self, attacker_coord: Vector) -> list[Vector]:
        """All coordinates defending `attacker_coord`."""
        return defending_coords_(self, attacker_coord)

    def evolve_state(self) -> None:
        """Wait for an input form the user and then act accordingly."""
        return evolve_state_(self)

    def __getitem__(self, key: Vector) -> Square:
        if not self.has_coord(key):
            raise IndexError("Index vector not within board bounds.")
        return self.board[key.y][key.x]

    def __setitem__(self, key: Vector, value: Square) -> None:
        self.board[key.y][key.x] = value

    def __str__(self) -> str:
        return str(generate_main_display(self))
