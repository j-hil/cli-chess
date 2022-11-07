"""Expose the public aspects of `jchess.display.*`."""

from ._class import Display
from ._configs import (
    DARK_UTF8_SYMBOLS,
    DEFAULT_PALLET,
    DEFAULT_SYMBOLS,
    LIGHT_UTF8_SYMBOLS,
    STANDARD_SYMBOLS,
    VSC_PALLET,
)

__all__ = [
    "Display",
    "DARK_UTF8_SYMBOLS",
    "DEFAULT_PALLET",
    "DEFAULT_SYMBOLS",
    "STANDARD_SYMBOLS",
    "LIGHT_UTF8_SYMBOLS",
    "VSC_PALLET",
]
