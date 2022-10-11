"""Suite of terminal manipulation functions."""
import os
import sys

if os.name == "nt":
    from msvcrt import getch
else:
    import tty
    from termios import tcsetattr, tcgetattr, TCSADRAIN

ESC = "\x1b"
CSI = ESC + "["
OSC = ESC + "]"


def clear():
    print(CSI + "2J")


def show_cursor():
    print(CSI + "?25h")


def hide_cursor():
    print(CSI + "?25l")


def reset_cursor():
    # print(f"\033[{MAIN_DISPLAY_ROWS}A\033[2K", end="")
    print(CSI + "H" )


if os.name == "nt":

    def get_char() -> str:
        """Get a single character string from the user. Windows-compatible version."""
        return getch().decode()

else:

    def get_char() -> str:
        """Get a single character string from the user. Linux-compatible version.

        Based on https://stackoverflow.com/questions/71548267/. Somewhat magic to me.
        """
        sys.stdout.flush()
        ch = ""
        fd = sys.stdin.fileno()
        old_settings = tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            tcsetattr(fd, TCSADRAIN, old_settings)
        return ch
