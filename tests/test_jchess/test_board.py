from pathlib import Path

from jchess.board import Board
from jchess.geometry import V
from jchess.pieces import Piece, Player, Role
from jchess.testutils import board_from_ssv

DATA = Path(__file__).parent / "data"


def test_init() -> None:
    board = Board()
    assert len(board) == 64


def test_queen() -> None:
    board, expected_targets = board_from_ssv(DATA / "queen.ssv")
    coord = V(3, 3)
    assert board[coord] == Piece(Role.QUEEN, Player.TWO, moved=True)
    assert expected_targets == board.targets_of[coord]


def test_bishop() -> None:
    board, expected_targets = board_from_ssv(DATA / "bishop.ssv")
    coord = V(3, 3)
    assert board[coord] == Piece(Role.BISHOP, Player.ONE, moved=True)
    assert expected_targets == board.targets_of[coord]


def test_rook() -> None:
    board, expected_targets = board_from_ssv(DATA / "rook.ssv")
    coord = V(1, 2)
    assert board[coord] == Piece(Role.ROOK, Player.ONE, moved=True)
    assert expected_targets == board.targets_of[coord]


def test_knight() -> None:
    board, expected_targets = board_from_ssv(DATA / "knight.ssv")
    coord = V(3, 3)
    assert board[coord] == Piece(Role.KNIGHT, Player.ONE, moved=True)
    assert expected_targets == board.targets_of[coord]


def test_king() -> None:
    board, expected_targets = board_from_ssv(DATA / "king.ssv")
    coord = V(3, 3)
    assert board[coord] == Piece(Role.KING, Player.ONE, moved=True)
    assert expected_targets == board.targets_of[coord]


def test_king2() -> None:
    board, expected_targets = board_from_ssv(DATA / "king2.ssv")
    coord = V(3, 1)
    assert board[coord] == Piece(Role.KING, Player.TWO, moved=True)
    assert expected_targets == board.targets_of[coord]


def test_pawn() -> None:
    board, expected_targets = board_from_ssv(DATA / "pawn.ssv")
    coord = V(3, 6)
    assert board[coord] == Piece(Role.PAWN, Player.ONE, moved=False)
    assert expected_targets == board.targets_of[coord]


def test_castling() -> None:
    board, expected_targets = board_from_ssv(DATA / "castling.ssv")
    coord = V(4, 7)
    assert board[coord] == Piece(Role.KING, Player.ONE, moved=False)
    assert expected_targets == board.targets_of[coord]


def test_check_prevention() -> None:
    board, expected_targets = board_from_ssv(DATA / "check_prevention.ssv")
    coord = V(4, 3)
    assert board[coord] == Piece(Role.QUEEN, Player.TWO, moved=True)
    assert expected_targets == board.targets_of[coord]
