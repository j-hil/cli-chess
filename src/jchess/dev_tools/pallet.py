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

NAME: dict[str, str]= {
    **{getattr(Fore, color): color for color in BASE_COLORS},
    **{getattr(Fore, f"LIGHT{color}_EX"): f"L-{color}" for color in BASE_COLORS},
    **{getattr(Back, color): color for color in BASE_COLORS},
    **{getattr(Back, f"LIGHT{color}_EX"): f"L-{color}" for color in BASE_COLORS},
    **{getattr(Style, style): style for style in ["DIM", "NORMAL", "BRIGHT"]},
}


def _generate_pallet() -> str:
    sep = " || "
    headers = sep.join(f"{NAME[fore]: ^9}" for fore in FORES)
    output = " v-BACK \\ FORE->" + sep + headers + "\n"
    for back in BACKS:
        row = Fore.WHITE + Style.BRIGHT + f"{NAME[back]: <16}" + Style.RESET_ALL + sep
        for fore in FORES:
            styles = " ".join(style + "X" for style in STYLES)
            row += back + fore + "  " + styles + "  " + Style.RESET_ALL + sep
        output += row + "\n"
    return output


if __name__ == "__main__":
    init()
    print(_generate_pallet())
