from pathlib import Path
from unittest import TestCase

from jchess.board import Board
from jchess.geometry import V
from jchess.pieces import Piece, Player, Role
from jchess.testutils import board_from_ssv

DATA = Path(__file__).parent / "data"


class TestBoard(TestCase):
    def test_init(self) -> None:
        board = Board()
        self.assertEqual(len(board), 64)

    def test_queen(self) -> None:
        board, expected_targets = board_from_ssv(DATA / "queen.ssv")
        coord = V(3, 3)
        self.assertEqual(board[coord], Piece(Role.QUEEN, Player.TWO, moved=True))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_bishop(self) -> None:
        board, expected_targets = board_from_ssv(DATA / "bishop.ssv")
        coord = V(3, 3)
        self.assertEqual(board[coord], Piece(Role.BISHOP, Player.ONE, moved=True))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_rook(self) -> None:
        board, expected_targets = board_from_ssv(DATA / "rook.ssv")
        coord = V(1, 2)
        self.assertEqual(board[coord], Piece(Role.ROOK, Player.ONE, moved=True))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_knight(self) -> None:
        board, expected_targets = board_from_ssv(DATA / "knight.ssv")
        coord = V(3, 3)
        self.assertEqual(board[coord], Piece(Role.KNIGHT, Player.ONE, moved=True))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_king(self) -> None:
        board, expected_targets = board_from_ssv(DATA / "king.ssv")
        coord = V(3, 3)
        self.assertEqual(board[coord], Piece(Role.KING, Player.ONE, moved=True))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_king2(self) -> None:
        board, expected_targets = board_from_ssv(DATA / "king2.ssv")
        coord = V(3, 1)
        self.assertEqual(board[coord], Piece(Role.KING, Player.TWO, moved=True))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_pawn(self) -> None:
        board, expected_targets = board_from_ssv(DATA / "pawn.ssv")
        coord = V(3, 6)
        self.assertEqual(board[coord], Piece(Role.PAWN, Player.ONE, moved=False))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_castling(self) -> None:
        board, expected_targets = board_from_ssv(DATA / "castling.ssv")
        coord = V(4, 7)
        self.assertEqual(board[coord], Piece(Role.KING, Player.ONE, moved=False))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_check_prevention(self) -> None:
        board, expected_targets = board_from_ssv(DATA / "check_prevention.ssv")
        coord = V(4, 3)
        self.assertEqual(board[coord], Piece(Role.QUEEN, Player.TWO, moved=True))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))
