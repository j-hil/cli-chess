"""Initial drafting file."""
from msvcrt import getch
from state import GameState
import os


def get_one_key_input():
    char1 = getch().decode()
    char2 = getch().decode() if char1 == "\x00" else ""
    return char1 + char2


def main(game: GameState):
    """Enter the main game-play loop."""

    keys = []
    while True:
        x = get_one_key_input()

        if x == "\x00H":
            keys.append("↑")
            game.cursor.y -= 1
        elif x == "\x00P":
            keys.append("↓")
            game.cursor.y += 1
        elif x == "\x00K":
            keys.append("←")
            game.cursor.x -= 1
        elif x == "\x00M":
            keys.append("→")
            game.cursor.x += 1
        elif x.lower() == "q":
            break
        else:
            keys.append(x)
        os.system("cls")
        print(game)


if __name__ == "__main__":

    # TODO: implement different colors/styles for different consoles
    from colorama import init, Style

    init()
    print(Style.BRIGHT)
    game = GameState()
    print(game)

    main(game)