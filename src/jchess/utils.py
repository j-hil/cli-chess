import os
import sys

if os.name == "nt":
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import tty
    import termios

    def getch() -> str:
        sys.stdout.flush()
        ch = ""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try :
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally :
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

if __name__ == "__main__":
    x = ""
    while x not in ["q", b"q"]:
        x = getch()
        print(f"{x=}")