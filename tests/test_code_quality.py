import sys
from subprocess import run
from unittest import TestCase

import jchess

jchess_path, *_ = jchess.__path__


class CodeQuality(TestCase):
    def test_mypy(self) -> None:
        args = f"{sys.executable} -m mypy .".split()
        p = run(args, capture_output=True, check=False)
        if p.returncode:
            raise RuntimeError(f"[>>] mypy output:\n{p.stdout.decode()}")

    def test_pylint(self) -> None:
        args = f"{sys.executable} -m pylint {jchess_path} --disable=fixme".split()
        p = run(args, capture_output=True, check=False)
        if p.returncode:
            raise RuntimeError(f"[>>] pylint output:\n{p.stdout.decode()}")

    def test_pydocstyle(self) -> None:
        args = f"{sys.executable} -m pydocstyle .".split()
        p = run(args, capture_output=True, check=False)
        if p.returncode:
            raise RuntimeError(f"[>>] pydocstyle output:\n{p.stderr.decode()}")

    def test_black(self) -> None:
        args = f"{sys.executable} -m black --check .".split()
        p = run(args, capture_output=True, check=False)
        if p.returncode:
            raise RuntimeError(f"[>>] black output:\n{p.stderr.decode()}")

    def test_isort(self) -> None:
        args = f"{sys.executable} -m isort --check .".split()
        p = run(args, capture_output=True, check=False)
        if p.returncode:
            raise RuntimeError(f"[>>] black output:\n{p.stderr.decode()}")
