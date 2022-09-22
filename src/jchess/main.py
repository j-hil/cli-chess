"""Initial drafting file."""
from msvcrt import getch
from jchess.state import GameState
import os
from copy import deepcopy


def get_one_key_input():
    char1 = getch().decode()
    char2 = getch().decode() if char1 == "\x00" else ""
    return char1 + char2


def main(game: GameState):
    """Enter the main game-play loop."""

    while True:

        os.system("cls")
        print(game)

        key = get_one_key_input()
        x, y = game.cursor

        if key == " " and game.selected is None and game.valid_selection():
            game.selected = deepcopy(game.cursor)
            continue

        if key == " " and game.selected is not None and game.valid_move():
            x0, y0 = game.selected

            piece0 = game.board[y0][x0]
            piece1 = game.board[y][x]

            # TODO: decided what the convention for 'taken' pieces (eg send to -1, -1)
            piece0.coord = x, y

            if piece1 is not None:
                piece1.coord = (-1, -1)

            game.selected = None
            game.swap_player()
            continue

        if key == "\x00H" and y - 1 >= 0:
            game.cursor = (x, y - 1)
        elif key == "\x00P" and y + 1 <= 7:
            game.cursor = (x, y + 1)
        elif key == "\x00K" and x - 1 >= 0:
            game.cursor = (x - 1, y)
        elif key == "\x00M" and x + 1 <= 7:
            game.cursor = (x + 1, y)
        elif key in ["\x1b", "q", "Q"]:
            break


if __name__ == "__main__":

    # TODO: implement different colors/styles for different consoles
    from colorama import init

    init()
    game = GameState()
    main(game)
