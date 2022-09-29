"""Creates a class containing the bulk of the logic and complexity of the game."""

from jchess.geometry import Vector
from jchess.squares import Square, Player, Role
from jchess.configs import Config, VSC_CONFIG
from jchess.game.logic import defending_coords_
from jchess.game.engine import Mode, EMPTY_SQUARE, UNSELECTED_COORD, evolve_state_
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
            configs available in jchess.config. Defaults to VSC_CONFIG
        """
        self.board = [
            [Square(role, Player.TWO) for role in [R, N, B, Q, K, B, N, R]],
            [Square(P, Player.TWO) for _ in range(8)],
            *[[EMPTY_SQUARE for _ in range(8)] for _ in range(4)],
            [Square(P, Player.ONE) for _ in range(8)],
            [Square(role, Player.ONE) for role in [R, N, B, Q, K, B, N, R]],
        ]
        self.config = config
        self.mode = Mode.ONE

        # start cursor at player one's King
        self.cursor_coord = Vector(4, 7)
        self.selected_coord = UNSELECTED_COORD

        self.en_passant_victim_coord: Vector = UNSELECTED_COORD
        # self.can_left_castle = {Player.ONE: True, Player.TWO: True}

        self.turn = 0
        self.taken_pieces: dict[Player, list[Role]] = {Player.ONE: [], Player.TWO: []}


    @property
    def selected(self) -> Square:
        """Square currently selected by the active player, if any."""
        return self[self.selected_coord]

    @selected.setter
    def selected(self, value: Square) -> None:
        self[self.selected_coord] = value

    @property
    def cursor(self) -> Square:
        """Square which the game cursor is currently highlighting."""
        return self[self.cursor_coord]

    @cursor.setter
    def cursor(self, value: Square) -> None:
        self[self.cursor_coord] = value

    def score(self, player: Player) -> int:
        return sum(x.val for x in self.taken_pieces[player])

    def active_player(self) -> Player:
        return list(Player)[self.turn % 2]

    def inactive_player(self) -> Player:
        return list(Player)[(self.turn + 1) % 2]

    def defending_coords(self, attacker_coord: Vector) -> list[Vector]:
        """All coordinates defending `attacker_coord`."""
        return defending_coords_(self, attacker_coord)

    def evolve_state(self) -> None:
        """Wait for an input form the user and then act accordingly."""
        return evolve_state_(self)

    def __getitem__(self, key: Vector) -> Square:
        return self.board[key.y][key.x]

    def __setitem__(self, key: Vector, value: Square) -> None:
        self.board[key.y][key.x] = value

    def __str__(self) -> str:
        return str(generate_main_display(self))
