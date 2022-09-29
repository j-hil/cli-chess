"""Creates a class containing the bulk of the logic and complexity of the game."""

from jchess.game.logic import defending_coords_
from jchess.geometry import Vector
from jchess.squares import Square, Player, Role
from jchess.configs import Config, VSC_CONFIG
from jchess.game.engine import (
    Mode,
    EMPTY_SQUARE,
    UNSELECTED_SQUARE,
    UNSELECTED_COORD,
    evolve_state_,
)
from jchess.game.visuals import generate_main_display

K, Q, R, B, N, P, _ = list(Role)


class GameState:
    """Represents the state of the game, and controls the game logic."""

    @staticmethod
    def has(coord: Vector) -> bool:
        """Check if a valid chess coord."""
        return coord.x in range(8) and coord.y in range(8)

    def __init__(self, config: Config = VSC_CONFIG):
        """Initialise a `GameState`.

        :param config: Controls settings such as color, symbols etc. Several pre-made
            configs available in jchess.config. Defaults to VS_CODE_CONFIG
        """
        self.board: list[list[Square]] = [
            [Square(role, Player.TWO) for role in [R, N, B, Q, K, B, N, R]],
            [Square(P, Player.TWO) for _ in range(8)],
            *[[EMPTY_SQUARE for _ in range(8)] for _ in range(4)],
            [Square(P, Player.ONE) for _ in range(8)],
            [Square(role, Player.ONE) for role in [R, N, B, Q, K, B, N, R]],
        ]
        self.config = config

        self.highlighted_coord = Vector(4, 7)
        self.selected_coord = UNSELECTED_COORD

        self.turn = 0
        self.taken_pieces: dict[Player, list[Role]] = {Player.ONE: [], Player.TWO: []}
        self.mode = Mode.ONE

    @property
    def selected(self) -> Square:
        """Square currently selected by the active player, if any."""
        if self.selected_coord is UNSELECTED_COORD:
            return UNSELECTED_SQUARE
        return self[self.selected_coord]

    @selected.setter
    def selected(self, value: Square) -> None:
        if value is UNSELECTED_SQUARE:
            self.selected_coord = UNSELECTED_COORD
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

    def active_player(self) -> Player:
        return list(Player)[self.turn % 2]

    def inactive_player(self) -> Player:
        return list(Player)[(self.turn + 1) % 2]

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
        if not self.has(key):
            raise IndexError("Index vector not within board bounds.")
        return self.board[key.y][key.x]

    def __setitem__(self, key: Vector, value: Square) -> None:
        self.board[key.y][key.x] = value

    def __str__(self) -> str:
        return str(generate_main_display(self))
