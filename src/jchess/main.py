"""
Initial drafting file.


##  ##  ##  ##
  ##  ##  ##  ##
##  ##  ##  ##         CLI CHESS :) - coming soon, maybe
  ##  ##  ##  ##
##  ##  ##  ##
  ##  ##  ##  ##
##  ##  ##  ##
  ##  ##  ##  ##
"""

from msvcrt import getch

def get_one_key_input():
    char1 = getch().decode()
    char2 = getch().decode() if char1 == "\x00" else ""
    return char1 + char2



def main():
    """Enter the main game-play loop."""

    keys = []
    while True:
        x = get_one_key_input()

        if x == "\x00H":
            keys.append("↑")
        elif x == "\x00P":
            keys.append("↓")
        elif x == "\x00K":
            keys.append("←")
        elif x == "\x00M":
            keys.append("→")
        elif x == "q":
            break
        else:
            keys.append(x)

    print(" ".join(keys))


if __name__ == "__main__":
    main()
