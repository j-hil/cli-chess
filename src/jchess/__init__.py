"""Package metadata."""

from importlib.metadata import metadata


__package__ = "jchess"
__version__ = metadata(__package__)["version"]
__author__ = "j-hil"
