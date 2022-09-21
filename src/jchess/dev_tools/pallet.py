"""Display all possible fore, back and style combinations.

In particular this is useful to view which combinations of fores, backs and styles are
appropriate for each console, since it varies.
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

output = (
    # column labels
    " " * 11
    + "".join(fore + f"{NAMES[fore]:11s}" for fore in FORES)
    + "\n"
    # remaining rows
    + "".join(
        (
            back
            + f"{NAMES[back]:11s}"
            + Back.RESET
            + back
            + "".join(
                (
                    fore
                    + "".join(style + " X" for style in STYLES) + " "
                    + Style.RESET_ALL
                    + " || "
                    + back
                )
                for fore in FORES
            )
            + Style.RESET_ALL
            + "\n"
        )
        for back in BACKS
    )
)

# BLACK AND WHITE ON BLACK AND MAGENTA seems to be only good combo
init()
print(output)



