"""Initial drafting file."""
from msvcrt import getch
from state import GameState
from pieces import Piece
import os
from copy import deepcopy


def get_one_key_input():
    char1 = getch().decode()
    char2 = getch().decode() if char1 == "\x00" else ""
    return char1 + char2


def main(game: GameState):
    """Enter the main game-play loop."""

    keys = []
    while True:
        os.system("cls")
        print(game)
        x = get_one_key_input()

        if x == " " and game.selected is None and game.valid_selection():
            game.selected = deepcopy(game.cursor)
            continue

        if x == " " and game.selected is not None and game.valid_move():
            x0, y0 = game.selected.x, game.selected.y
            x1, y1 = game.cursor.x, game.cursor.y

            piece0: Piece | None = game.board[y0][x0]
            piece1: Piece | None = game.board[y1][x1]

            # TODO: decided what the convention for 'taken' pieces (eg send to -1, -1)
            piece0.coord = x1, y1

            if piece1 is not None:
                piece1.coord = (-1, -1)

            game.selected = None
            game.cursor.x, game.cursor.y = 0, 0
            continue

        if x == "\x00H" and game.cursor.y - 1 >= 0:
            keys.append("↑")
            game.cursor.y -= 1
        elif x == "\x00P" and game.cursor.y + 1 <= 7:
            keys.append("↓")
            game.cursor.y += 1
        elif x == "\x00K" and game.cursor.x - 1 >= 0:
            keys.append("←")
            game.cursor.x -= 1
        elif x == "\x00M" and game.cursor.x + 1 <= 7:
            keys.append("→")
            game.cursor.x += 1
        elif x in ["\x1b", "q", "Q"]:
            print(keys)
            break
        else:
            keys.append(x)


if __name__ == "__main__":

    # TODO: implement different colors/styles for different consoles
    from colorama import init, Style

    init()
    print(Style.BRIGHT)
    game = GameState()
    main(game)
