from subprocess import run
import sys
from unittest import TestCase
from importlib.metadata import metadata


class CodeQuality(TestCase):
    def test_mypy(self) -> None:
        p = run(f"{sys.executable} -m mypy .".split(), capture_output=True)
        if p.returncode:
            raise RuntimeError(f"[>>] mypy output:\n{p.stdout.decode()}")

    def test_pylint(self) -> None:
        args = f"{sys.executable} -m pylint .\\src\\jchess --disable=fixme".split()
        p = run(args, capture_output=True)
        if p.returncode:
            raise RuntimeError(f"[>>] pylint output:\n{p.stdout.decode()}")

    def test_pydocstyle(self) -> None:
        p = run(f"{sys.executable} -m pydocstyle .".split(), capture_output=True)
        if p.returncode:
            raise RuntimeError(f"[>>] pydocstyle output:\n{p.stderr.decode()}")
