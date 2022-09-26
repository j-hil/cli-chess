"""Display all possible fore, back and style combinations.

In particular this is useful to view which combinations of fores, backs and styles are
appropriate for each console, since it varies.

Original taken from https://github.com/tartley/colorama/blob/master/demos/demo01.py
"""
from colorama import init, Fore, Back, Style

BASE_COLORS = ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE"]
LIGHT_COLORS = [f"LIGHT{color}_EX" for color in BASE_COLORS]

FORES = [getattr(Fore, color) for color in BASE_COLORS + LIGHT_COLORS]
BACKS = [getattr(Back, color) for color in BASE_COLORS + LIGHT_COLORS]
STYLES = [Style.DIM, Style.NORMAL, Style.BRIGHT]

NAMES = {
    **{getattr(Fore, color): color for color in BASE_COLORS},
    **{getattr(Fore, f"LIGHT{color}_EX"): f"L-{color}" for color in BASE_COLORS},
    **{getattr(Back, color): color for color in BASE_COLORS},
    **{getattr(Back, f"LIGHT{color}_EX"): f"L-{color}" for color in BASE_COLORS},
}

def _generate_pallet():
    headers = " || ".join(f"{NAMES[fore]: ^9}" for fore in FORES)
    output = " v-BACK \\ FORE->" + " || " + headers + "\n"
    for back in BACKS:
        row = Fore.WHITE + Style.BRIGHT + f"{NAMES[back]: <16}" + Style.RESET_ALL + " || "
        for fore in FORES:
            styles = " ".join(style + "X" for style in STYLES)
            row += back + fore + "  " + styles + "  " + Style.RESET_ALL + " || "
        output += row + "\n"
    return output

if __name__ == "__main__":
    init()
    print(_generate_pallet())

