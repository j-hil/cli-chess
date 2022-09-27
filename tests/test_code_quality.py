from subprocess import run
import sys
from unittest import TestCase
from importlib.metadata import metadata


class CodeQuality(TestCase):
    def test_mypy(self) -> None:
        args = [sys.executable, "-m", "mypy", "."]
        p = run(args, capture_output=True)
        if p.returncode:
            raise RuntimeError(f"[>>] mypy output:\n{p.stdout.decode()}")

    def test_pylint(self) -> None:
        args = [sys.executable, "-m", "pylint", r".\src\jchess", "--disable=fixme"]
        p = run(args, capture_output=True)
        if p.returncode:
            raise RuntimeError(f"[>>] pylint output:\n{p.stdout.decode()}")

    def test_pydocstyle(self) -> None:
        args = [sys.executable, "-m", "pydocstyle", "."]
        p = run(args, capture_output=True)
        if p.returncode:
            raise RuntimeError(f"[>>] pydocstyle output:\n{p.stderr.decode()}")
