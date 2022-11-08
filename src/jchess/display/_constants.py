"""Compute the constants for use in `jchess.display._class`."""
# At any given snapshot these could just be constants but I compute them dynamically
# (and inefficiently) instead so that I have to fiddle around with them less often.
#
# Since everything is computed once when the module is first imported, there shouldn't
# be any significant additional overhead.
#
# More should be moved from _class into here, but I'll only do so if it becomes useful.

from jchess.game import PROMOTION_OPTIONS, Mode
from jchess.geometry import V
from jchess.pieces import Player


def _get_width_height_vec(s: str) -> tuple[int, int]:
    parts = s.split("\n")
    w, h = len(parts[0]), len(parts)
    return w, h


# Main 25 x 87 display constants ----------------------------------------------------- #
MAIN_DISPLAY_TEMPLATE = """\
+-------------------------------------------------------------------------------------+
|                   Welcome to J-Chess! To quit hit the escape key.                   |
+-------------+---------------------------------------------------------+-------------+
|             |                                                         |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
+-------------+            +---+---+---+---+---+---+---+---+            +-------------+
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
+-------------+            +---+---+---+---+---+---+---+---+            +-------------+
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |            |   |   |   |   |   |   |   |   |            |             |
|             |            +---+---+---+---+---+---+---+---+            |             |
|             |                                                         |             |
+-------------+---------------------------------------------------------+-------------+
|             |                                                         |             |
+-------------------------------------------------------------------------------------+\
"""
MAIN_W, MAIN_H = _get_width_height_vec(MAIN_DISPLAY_TEMPLATE)

# Start menu constants --------------------------------------------------------------- #
INITIAL_W = len("[esc: quit, space: pick]")


def _make_start_menu() -> tuple[str, V]:
    main_lines = [
        "Pick a game mode:",
        "=" * INITIAL_W,
        *[f"{m.value}" for m in Mode],
        "=" * INITIAL_W,
        "[esc: quit, space: pick]",
    ]
    template = "".join(
        ["+-", "-" * INITIAL_W, "-+\n"]
        + [f"| {s: ^{INITIAL_W}} |\n" for s in main_lines]
        + ["+-", "-" * INITIAL_W, "-+"]
    )

    w, h = _get_width_height_vec(template)
    return template, (V(MAIN_W, MAIN_H) - V(w, h)) // 2 + V(-1, 0)


MODE_STRINGS = [f"{m.value: ^{INITIAL_W}}" for m in Mode]
START_MENU_TEMPLATE, START_MENU_ANCHOR = _make_start_menu()
START_MENU_CLEAR = "".join(" " if c != "\n" else "\n" for c in START_MENU_TEMPLATE)


# Player column constants ------------------------------------------------------------ #
HELP_RHS = """\
 CONTROLS
===========
Arrow keys
 (to move)
   Enter
(to select)
    F12
 (forfeit)
"""

HELP_LHS = """\
 CONTROLS
===========
 WASD keys
 (to move)
   Space
(to select)
    F1
 (forfeit)
"""

HELP_BOT = """\
    BOT
===========
Player {}
 randomly
selects its
 next move
 It is a
'dumb bot'.
"""

HELP_TEMPLATES = {
    Player.ONE: {
        Mode.TDB: HELP_BOT.format(Player.ONE),
        Mode.VDB: HELP_RHS,
        Mode.LTP: HELP_LHS,
    },
    Player.TWO: {
        Mode.TDB: HELP_BOT.format(Player.TWO),
        Mode.VDB: HELP_BOT.format(Player.TWO),
        Mode.LTP: HELP_RHS,
    },
}

INFO_TEMPLATE = """\
Player {}:
===========
SCORE = 000\
"""

PROMOTION_TEMPLATE = """\
Promote to:
===========
""" + "\n".join(
    f"({r.symbol}) {r}" for r in PROMOTION_OPTIONS
)
PROMOTION_CLEAR = "".join(" " if c != "\n" else "\n" for c in PROMOTION_TEMPLATE)

INFO_W = len(PROMOTION_TEMPLATE.split("\n", maxsplit=1)[0])
for t in [HELP_LHS, INFO_TEMPLATE, PROMOTION_TEMPLATE, PROMOTION_CLEAR]:
    assert INFO_W == len(t.split("\n", maxsplit=2)[1])


# Other constants -------------------------------------------------------------------- #
ROW_LABELS = "8   7   6   5   4   3   2   1"
COL_LABELS = "a\n \nb\n \nc\n \nd\n \ne\n \nf\n \ng\n \nh"
