from typing import TYPE_CHECKING

from jchess.pieces import Role
from jchess.terminal import ctrlseq

if TYPE_CHECKING:
    from jchess.state._state import GameState


def clear() -> str:
    return ctrlseq(PROMOTION_CLEAR, at=(3, 12))


def init(self: "GameState") -> str:
    role = OPTIONS[self.cursor_p]
    color = self.config.cursor_color
    return ctrlseq(PROMOTION_TEMPLATE, at=(3, 12)) + ctrlseq(
        f"({role.symbol}) {role}", color=color, at=(3, 14 + self.cursor_p)
    )


def update(self: "GameState", old_cursor_p: int) -> str:
    role0 = OPTIONS[old_cursor_p]
    role1 = OPTIONS[self.cursor_p]
    color = self.config.cursor_color
    return ctrlseq(
        f"({role0.symbol}) {role0: <6}", at=(3, 14 + old_cursor_p)
    ) + ctrlseq(f"({role1.symbol}) {role1}", color=color, at=(3, 14 + self.cursor_p))


OPTIONS = (Role.QUEEN, Role.KNIGHT, Role.ROOK, Role.BISHOP)
PROMOTION_TEMPLATE = "Promote to:\n===========\n" + "\n".join(
    f"({role.symbol}) {role}" for role in OPTIONS
)
PROMOTION_CLEAR = "".join(" " if c != "\n" else "\n" for c in PROMOTION_TEMPLATE)
