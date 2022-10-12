from subprocess import run
import sys
from unittest import TestCase

import jchess

jchess_path = jchess.__path__[0]  # type: ignore


class CodeQuality(TestCase):
    def test_mypy(self) -> None:
        p = run(f"{sys.executable} -m mypy .".split(), capture_output=True)
        if p.returncode:
            raise RuntimeError(f"[>>] mypy output:\n{p.stdout.decode()}")

    def test_pylint(self) -> None:
        args = f"{sys.executable} -m pylint {jchess_path} --disable=fixme".split()
        p = run(args, capture_output=True)
        if p.returncode:
            raise RuntimeError(f"[>>] pylint output:\n{p.stdout.decode()}")

    def test_pydocstyle(self) -> None:
        p = run(f"{sys.executable} -m pydocstyle .".split(), capture_output=True)
        if p.returncode:
            raise RuntimeError(f"[>>] pydocstyle output:\n{p.stderr.decode()}")
