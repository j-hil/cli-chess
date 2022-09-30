from unittest import TestCase
from colorama import Fore, Back, Style
from jchess.display import PrintableChar


class TestPrintableChar(TestCase):
    def test_init(self):
        # basic use case
        PrintableChar("a")

        # check fails for multi-char strings
        with self.assertRaises(ValueError):
            PrintableChar("ab")

        # check fails for non-displayable chars
        with self.assertRaises(ValueError):
            PrintableChar("a\r")
        with self.assertRaises(ValueError):
            PrintableChar("a" + Fore.BLACK)

    def test_color(self):

        # basic use case
        c = PrintableChar("c", Fore.BLACK, "", Style.BRIGHT)
        c.back = Back.BLUE

        # check color must be from colorama
        d = PrintableChar("d")
        with self.assertRaises(ValueError):
            d.fore = "BLACK"
        with self.assertRaises(ValueError):
            d.back = "BLACK"
        with self.assertRaises(ValueError):
            d.style = "BRIGHT"

    def test_str(self):

        c = PrintableChar("c", Fore.BLACK, "", Style.BRIGHT)
        self.assertEqual(str(c), Fore.BLACK + Style.BRIGHT + "c" + Style.RESET_ALL)

        c.back = Back.BLUE
        self.assertEqual(
            str(c), Fore.BLACK + Back.BLUE + Style.BRIGHT + "c" + Style.RESET_ALL
        )

    def test_repr(self):

        c = PrintableChar("c", Fore.BLACK, "", Style.BRIGHT)
        self.assertEqual(repr(c), f"[char='c', color=BLACK;NONE;BRIGHT]")
