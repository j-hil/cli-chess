"""Minimal `setup.py` for editable installs."""

from setuptools import setup

try:
    from jchess.dev_tools.version import VERSION
    setup(version=VERSION)
except ImportError:
    setup()