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


def _get_width_height_vec(s: str) -> tuple[int, int]:
    parts = s.split("\n")
    w, h = len(parts[0]), len(parts)
    return w, h


# Main 25 x 87 display constants ----------------------------------------------------- #
MAIN_DISPLAY_TEMPLATE = """\
+-------------------------------------------------------------------------------------+
| Welcome to J-Chess! Controls: arrows to navigate, space to select, and 'q' to quit. |
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
def _make_start_menu() -> tuple[str, V]:
    mode_strs = [f"(+) {m.value}" for m in Mode]
    initial_w = max(len(s) for s in mode_strs)

    main_lines = [f"{'Pick a game mode:': ^{initial_w}}", "=" * initial_w, *mode_strs]
    template = "".join(
        ["+-", "-" * initial_w, "-+\n"]
        + [f"| {s: <{initial_w}} |\n" for s in main_lines]
        + ["+-", "-" * initial_w, "-+"]
    )

    w, h = _get_width_height_vec(template)
    return template, (V(MAIN_W, MAIN_H) - V(w, h)) // 2 + V(-1, 0)


START_MENU_TEMPLATE, START_MENU_ANCHOR = _make_start_menu()
START_MENU_CLEAR = "".join(" " if c != "\n" else "\n" for c in START_MENU_TEMPLATE)


# Other constants --------------------------------------------------------------- #
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

ROW_LABELS = "8   7   6   5   4   3   2   1"
COL_LABELS = "a\n \nb\n \nc\n \nd\n \ne\n \nf\n \ng\n \nh"
