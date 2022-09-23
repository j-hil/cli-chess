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


def hide_terminal_cursor():
    print("\033[?25l", end="")


def show_terminal_cursor():
    print("\033[?25h", end="")


def clear_screen():
    print("\033[20A\033[2K", end="")


def main():

    init()
    os.system("cls")
    hide_terminal_cursor()
    game = GameState()
    while True:

        clear_screen()
        hide_terminal_cursor()
        print(game)

        key = get_one_key_input()
        x, y = game.cursor_coord.x, game.cursor_coord.y

        if key == " " and game.can_select_attacker():
            game.attacker_coord = deepcopy(game.cursor_coord)
        elif key == " " and game.is_defending(game.cursor_coord):
            game.make_move()
        elif key == "\x00H" and y - 1 >= 0:
            game.cursor_coord += (0, -1)
        elif key == "\x00P" and y + 1 <= 7:
            game.cursor_coord += (0, +1)
        elif key == "\x00K" and x - 1 >= 0:
            game.cursor_coord += (-1, 0)
        elif key == "\x00M" and x + 1 <= 7:
            game.cursor_coord += (+1, 0)
        elif key in ["\x1b", "q", "Q"]:
            show_terminal_cursor()
            break


if __name__ == "__main__":
    main()
