import os
from typing import Self, no_type_check

import jchess.display
import jchess.run
from jchess.action import Action, get_action_rhs
from jchess.configs import UTF8_SYMBOLS, VSC_PALLET
from jchess.game import Game
from jchess.run import run
from jchess.testutils import board_to_ssv

# attempt to detect that game is being run inside VS Code
DEV_MODE = os.environ.get("TERM_PROGRAM") == "vscode"


class HackedGame(Game):

    singleton = None
    inputs: list[str] = []

    def __new__(cls: type["HackedGame"]) -> "HackedGame":
        if cls.singleton is None:
            cls.singleton = super().__new__(cls)
        return cls.singleton

    def get_action(self) -> Action:
        action = get_action_rhs()
        self.inputs.append(action.value)
        return action


hacked_game = HackedGame()


@no_type_check
def hack() -> None:
    if not DEV_MODE:
        print("Warning: running `jchess` this way is intended only for development.")
        input("Press any key to continue.")
    else:
        jchess.run.DEFAULT_PALLET = VSC_PALLET
        jchess.run.DEFAULT_SYMBOLS = UTF8_SYMBOLS

    jchess.display.ROW_LABELS = "0   1   2   3   4   5   6   7"
    jchess.display.COL_LABELS = "0\n \n1\n \n2\n \n3\n \n4\n \n5\n \n6\n \n7"
    jchess.run.Game = HackedGame


def main() -> None:
    try:
        hack()
        run()
    finally:
        print("Actions were:")
        output = " ".join(hacked_game.inputs)
        n = 76
        for i in range(len(output) // n + 1):
            print(f"{output[n * i : n * (i + 1)]}")
        print()

        print("Final State")
        board = hacked_game.board
        targets = board.targets[hacked_game.bcursor]
        print(board_to_ssv(board, targets))
        print()


if __name__ == "__main__":
    main()
