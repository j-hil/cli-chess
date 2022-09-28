"""Provide versioning constant for `setuptools`.

Chosen convention is `year.month.commits` which has the following desired properties:
* generates a strictly increasing sequence of version numbers
* completely automatic version number generation
* naturally approximates the major.minor.patch convention
* pep 440 compliant
* provides useful information at a glance

The version is also tagged as dirty if there are uncommitted changes."""

from datetime import date
from subprocess import run


def _get_stdout(cmd: str) -> str:
    return run(cmd.split(), capture_output=True).stdout.decode()

def _get_version():
    today = date.today()
    # this probably only works with a linear commit history
    commits = _get_stdout("git rev-list --all --count").strip()
    dirty = _get_stdout("git status --porcelain") and "+dirty"
    return f"{today.year % 100}.{today.month}.{commits}{dirty}"

VERSION = _get_version()

