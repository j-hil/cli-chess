"""Creates a class containing the bulk of the logic and complexity of the game."""

from copy import deepcopy

from jchess.geometry import Vector, VectorLike
from jchess.squares import NULL_SQUARE, Square, Role, Player
from jchess.configs import Config, VS_CODE_CONFIG
from jchess.constants import (
    PIECE_VALUE,
    STANDARD_CHESS_BOARD,
    DELTAS,
    LINES,
    INPUT_DELTAS,
)
from jchess.display import generate_main_display


# TODO: this class could do with cleaning & reducing
class GameState:
    """Represents the state of the game, and controls the game logic."""

    def __init__(self, config: Config = VS_CODE_CONFIG):
        """Initialise a `GameState`.

        :param config: Controls settings such as color, symbols etc. Several pre-made
            configs available in jchess.config. Defaults to VS_CODE_CONFIG
        """
        self.board = STANDARD_CHESS_BOARD
        self.config = config

        self.highlighted_coord = Vector(0, 4)
        self.selected_coord: Vector | None = None
        self.active = Player.ONE
        self.inactive = Player.TWO
        self.quitting = False

        self.taken_pieces: dict[Player, list[Square]] = {Player.ONE: [], Player.TWO: []}
        self.score = {Player.ONE: 0, Player.TWO: 0}

    @property
    def selected(self) -> Square | None:
        """Square currently selected by the active player, if any."""
        if self.selected_coord is None:
            return None
        return self[self.selected_coord]

    @selected.setter
    def selected(self, value: Square | None) -> None:
        if value is None:
            self.selected_coord = None
            return

        if self.selected_coord is None:
            raise RuntimeError("`selected` can't be a Square as selected_coord=None.")

        self[self.selected_coord] = value

    @property
    def highlighted(self) -> Square:
        """Square which the game cursor is currently highlighting."""
        piece = self[self.highlighted_coord]
        if piece is None:
            raise RuntimeError("`_cursor_coord` should always be in bounds.")
        return piece

    @highlighted.setter
    def highlighted(self, value: Square) -> None:
        self[self.highlighted_coord] = value

    def is_defending(self, coord: VectorLike) -> bool:
        """Check if the square at the input coord is defending against the attacker."""
        if isinstance(coord, tuple):
            coord = Vector(*coord)
        return coord in self.defending_coords(self.selected_coord)

    def defending_coords(self, attacker_coord: Vector | None) -> list[Vector]:
        """All coordinates defending against the current attacker."""
        attacker = self[attacker_coord]
        if attacker is None or attacker_coord is None:
            return []

        result = []
        if attacker.role in [Role.BISHOP, Role.ROOK, Role.QUEEN]:
            for line in LINES[attacker.role]:
                for delta in line:
                    defender_coord = attacker_coord + delta
                    defender = self[defender_coord]
                    if defender is not None:
                        if defender.player is self.inactive:
                            result.append(defender_coord)
                            break
                        if defender.player is self.active:
                            break
                        result.append(defender_coord)

        if attacker.role in [Role.KING, Role.KNIGHT]:
            for delta in DELTAS[attacker.role]:
                defender_coord = attacker_coord + delta
                defender = self[defender_coord]
                if defender is not None and defender.player != self.active:
                    result.append(defender_coord)

        if attacker.role is Role.PAWN:
            if attacker.player is Player.ONE:
                direction = 1
                x_start = 1
            else:  # player is TWO
                direction = -1
                x_start = 6

            defender_coord = attacker_coord + (direction, 0)
            defender = self[defender_coord]
            if defender is not None and defender.role is Role.NULL:
                result.append(defender_coord)

            for dy in [1, -1]:
                defender_coord = attacker_coord + (direction, dy)
                defender = self[defender_coord]
                if defender is not None and defender.player == self.inactive:
                    result.append(defender_coord)

            defender_coord = attacker_coord + (2 * direction, 0)
            if attacker_coord.x == x_start:
                result.append(defender_coord)

        return result

    def make_move(self) -> None:
        """Execute a move of the attacker to the current highlighted square."""
        if self.selected is None:
            raise ValueError("Cannot make a move when no Square is selected.")

        if self.highlighted is not NULL_SQUARE:
            self.taken_pieces[self.active].append(self.highlighted)
            self.score[self.active] += PIECE_VALUE[self.highlighted.role]

        self.highlighted = self.selected
        self.selected = NULL_SQUARE
        self.active, self.inactive = self.inactive, self.active
        self.selected_coord = None

    def __getitem__(self, key: Vector | None) -> Square | None:
        if key is None or not key.in_bounds():
            return None
        return self.board[key.y][key.x]

    def __setitem__(self, key: Vector, value: Square) -> None:
        self.board[key.y][key.x] = value

    def __repr__(self) -> str:
        symbol = self.config.role_symbol
        return f"\n{'-' * 31}\n".join(
            " " + " | ".join(symbol[square.role] for square in row) + " "
            for row in self.board
        )

    def __str__(self) -> str:
        return str(generate_main_display(self))

    def process_input_key(self, key: str) -> None:
        """Take a read key and evolve the game state as appropriate."""
        can_use_highlighted = (
            self.selected is None
            and self.highlighted.role is not Role.NULL
            and self.highlighted.player is self.active
            and len(self.defending_coords(self.highlighted_coord)) > 0
        )

        if key == " " and can_use_highlighted:
            self.selected_coord = deepcopy(self.highlighted_coord)
        elif key == " " and self.is_defending(self.highlighted_coord):
            self.make_move()
        elif key in ["\x1b", "q", "Q"]:
            self.quitting = True
        else:
            new_cursor_coord = self.highlighted_coord + INPUT_DELTAS.get(key, (0, 0))
            if new_cursor_coord.in_bounds():
                self.highlighted_coord = new_cursor_coord


if __name__ == "__main__":
    game = GameState()
    from jchess.display import generate_player_column

    x = generate_player_column(game, Player.ONE)
    print(x)
