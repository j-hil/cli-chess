import sys
from subprocess import run

import jchess

jchess_path, *_ = jchess.__path__


def test_mypy() -> None:
    args = f"{sys.executable} -m mypy .".split()
    p = run(args, capture_output=True, check=False)
    if p.returncode:
        raise RuntimeError(f"[>>] mypy output:\n{p.stdout.decode()}")


def test_pylint() -> None:
    args = f"{sys.executable} -m pylint {jchess_path} --disable=fixme".split()
    p = run(args, capture_output=True, check=False)
    if p.returncode:
        raise RuntimeError(f"[>>] pylint output:\n{p.stdout.decode()}")


def test_pydocstyle() -> None:
    args = f"{sys.executable} -m pydocstyle .".split()
    p = run(args, capture_output=True, check=False)
    if p.returncode:
        raise RuntimeError(f"[>>] pydocstyle output:\n{p.stderr.decode()}")


def test_black() -> None:
    args = f"{sys.executable} -m black --check .".split()
    p = run(args, capture_output=True, check=False)
    if p.returncode:
        raise RuntimeError(f"[>>] black output:\n{p.stderr.decode()}")


def test_isort() -> None:
    args = f"{sys.executable} -m isort --check .".split()
    p = run(args, capture_output=True, check=False)
    if p.returncode:
        raise RuntimeError(f"[>>] black output:\n{p.stderr.decode()}")
