from copy import deepcopy

from jchess.state import GameState


def process_input_key(self: GameState, key: str) -> None:
    """Take a read key and evolve the game state as appropriate."""
    can_use_highlighted = (
        self.selected is None
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
        if GameState.in_bounds(new_cursor_coord):
            self.highlighted_coord = new_cursor_coord


INPUT_DELTAS: dict[str, tuple[int, int]] = {
    "\x00H": (0, -1),
    "\x00P": (0, +1),
    "\x00K": (-1, 0),
    "\x00M": (+1, 0),
}
