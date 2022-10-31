import os

import jchess.run
import jchess.display
import jchess.state
from jchess.run import run
from jchess.action import Action, get_action_rhs
from jchess.configs import UTF8_SYMBOLS, VSC_PALLET
from jchess.state import GameState

inputs: list[str] = []

# attempt to detect that game is being run inside VS Code
DEV_MODE = os.environ.get("TERM_PROGRAM") == "vscode"


def hack_get_action(self: GameState) -> Action:

    action = get_action_rhs()
    global inputs
    inputs.append(action.value)

    return action


def main() -> None:
    if not DEV_MODE:
        print("Warning: running `jchess` this way is intended only for development.")
        input("Press any key to continue.")
    else:
        jchess.run.DEFAULT_PALLET = VSC_PALLET  # type: ignore
        jchess.run.DEFAULT_SYMBOLS = UTF8_SYMBOLS  # type: ignore

    jchess.display.ROW_LABELS = "   ".join(list("01234567"))
    jchess.display.COL_LABELS = "\n \n".join(list("01234567"))
    jchess.state.GameState.get_action = hack_get_action

    try:
        run()
    finally:
        print("Actions were:")
        output = " ".join(inputs)
        n = 76
        for i in range(len(output) // n):
            print(f'"{output[n * i : n * (i + 1)]}"')


if __name__ == "__main__":
    main()
