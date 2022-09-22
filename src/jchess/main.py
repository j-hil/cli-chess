"""Initial drafting file."""
from msvcrt import getch
from jchess.state import GameState
import os
from copy import deepcopy
from colorama import init


def get_one_key_input():
    char1 = getch().decode()
    char2 = getch().decode() if char1 == "\x00" else ""
    return char1 + char2

def hide_cursor():
    print('\033[?25l', end="")

def show_cursor():
    print('\033[?25h', end="")

def clear_screen():
    # os.system("cls")
    # print("\n" * 10)
    print('\033[20A\033[2K', end='')


def main():
    """Enter the main game-play loop."""

    init()
    os.system("cls")
    hide_cursor()

    game = GameState()

    while True:

        clear_screen()

        print(game)

        key = get_one_key_input()
        x, y = game.cursor

        if key == " " and game.can_select_attacker():
            game.selected = deepcopy(game.cursor)

        elif key == " " and game.cursor in game.defending_coords(game.selected):
            game.make_move()

        elif key == "\x00H" and y - 1 >= 0:
            game.cursor = (x, y - 1)
        elif key == "\x00P" and y + 1 <= 7:
            game.cursor = (x, y + 1)
        elif key == "\x00K" and x - 1 >= 0:
            game.cursor = (x - 1, y)
        elif key == "\x00M" and x + 1 <= 7:
            game.cursor = (x + 1, y)
        elif key in ["\x1b", "q", "Q"]:
            show_cursor()
            break


if __name__ == "__main__":
    main()
