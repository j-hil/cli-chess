"""Compute the constants for use in `jchess.display._class`."""
# At any given snapshot these could just be constants but I compute them dynamically
# (and inefficiently) instead so that I have to fiddle around with them less often.
#
# Since everything is computed once when the module is first imported, there shouldn't
# be any significant additional overhead.
#
# This is honestly such an ugly way to do things and it should be replaced by a better
# system. See github issues?

from enum import IntEnum
from textwrap import wrap
from typing import Literal

from jchess.game import PROMOTION_OPTIONS, Mode
from jchess.geometry import V
from jchess.pieces import Player

# Consts determining location of elements on the terminal screen --------------------- #


class H(IntEnum):
    MAIN = 23
    SIDE_SMALL = 3
    SIDE_LARGE = MAIN - 2 * SIDE_SMALL - 6
    README = 11
    START = 7
    PROMOTION = SIDE_LARGE


class W(IntEnum):
    MAIN = 85
    SIDE = 11
    CENTER = MAIN - 2 * (SIDE + 1)
    TILE = 3
    START = 24
    GUTTER = 61
    PROMOTION = SIDE


Y1, Y2, Y3, Y4, Y5, Y6, Y7 = 2, 4, 8, 12, 16, 20, 24
X1, X2, X3 = 2, W.SIDE + 3, 2 + W.MAIN - W.SIDE


class Loc:
    # really should be Loc(V, Enum) but it just doesn't work... see github issues?
    HEADLINE = V(X1, Y1)
    BOARD = V(29, 6)

    LH_README = V(X1, Y2)
    LH_SCORE = V(X1, Y5)
    LH_TAKEN = V(X1, Y6)
    LH_PROMOTION = LH_README

    RH_SCORE = V(X3, Y2)
    RH_TAKEN = V(X3, Y3)
    RH_README = V(X3, Y4)
    RH_PROMOTION = RH_README

    VERSION = V(X1, Y7)
    AUTHOR = V(X3, Y7)
    GUTTER = V(X2, Y7)

    START = (V(W.MAIN, H.MAIN) - V(W.START, H.START)) // 2 + V(1, 1)


def _make_readme(flag: Literal["rhs", "lhs", "bot"]) -> str:
    if flag in ["rhs", "lhs"]:
        msg_parts = [
            "Arrow keys" if flag == "rhs" else "WASD keys",
            "(movement)",
            "Enter" if flag == "rhs" else "Space",
            "(selection)",
            "F12" if flag == "rhs" else "F1 ",
            "(forfeit)",
        ]
    else:  # flag is bot
        text = "This player is a 'dumb bot': it randomly selects each next move."
        msg_parts = wrap(text, W.SIDE)
    msg_parts = ["README:", "=" * W.SIDE, *msg_parts]
    missing_rows = H.SIDE_LARGE - len(msg_parts)
    msg_parts = (
        (missing_rows // 2) * [""]
        + msg_parts
        + (missing_rows - missing_rows // 2) * [""]
    )
    return "\n".join(l.center(W.SIDE) for l in msg_parts)


def _make_promotion() -> str:
    msg_parts = [
        "Promote to:",
        "=" * W.SIDE,
        *[f"({r.symbol}) {r}".ljust(W.SIDE) for r in PROMOTION_OPTIONS],
    ]
    missing_rows = H.SIDE_LARGE - len(msg_parts)
    msg_parts = (
        (missing_rows // 2) * [""]
        + msg_parts
        + (missing_rows - missing_rows // 2) * [""]
    )
    return "\n".join(l.center(W.SIDE) for l in msg_parts)


def _make_start_menu() -> str:
    lines = [
        "Pick a game mode:",
        "=" * W.START,
        *[f"{m.value}" for m in Mode],
        "=" * W.START,
        "[esc: quit, space: pick]",
    ]
    return "\n".join(l.center(W.START) for l in lines)


INFO_TEMPLATE = """\
Player {}:
===========
SCORE = {:0>3}\
"""
START_TEMPLATE = _make_start_menu()
PROMOTION_TEMPLATE = _make_promotion()
README_TEMPLATES = {
    Player.ONE: {
        Mode.TDB: _make_readme("bot"),
        Mode.VDB: _make_readme("rhs"),
        Mode.LTP: _make_readme("lhs"),
    },
    Player.TWO: {
        Mode.TDB: _make_readme("bot"),
        Mode.VDB: _make_readme("bot"),
        Mode.LTP: _make_readme("rhs"),
    },
}
MODE_STRINGS = [f"{m.value: ^{W.START}}" for m in Mode]
