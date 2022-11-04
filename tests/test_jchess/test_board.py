from pathlib import Path
from unittest import TestCase

from jchess.board import Board
from jchess.geometry import V
from jchess.pieces import Piece, Player, Role
from jchess.testutils import board_from_ssv

TEST_DATA_PATH = Path(__file__).parent / "data"


class TestBoard(TestCase):
    def test_init(self) -> None:
        board = Board()
        self.assertEqual(len(board), 64)

    def test_queen(self) -> None:
        queen_csv = TEST_DATA_PATH / "queen.ssv"
        board, expected_targets = board_from_ssv(queen_csv)
        coord = V(3, 3)
        self.assertEqual(board[coord], Piece(Role.QUEEN, Player.TWO, moved=True))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_bishop(self) -> None:
        bishop_ssv = TEST_DATA_PATH / "bishop.ssv"
        board, expected_targets = board_from_ssv(bishop_ssv)
        coord = V(3, 3)
        self.assertEqual(board[coord], Piece(Role.BISHOP, Player.ONE, moved=True))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_rook(self) -> None:
        rook_ssv = TEST_DATA_PATH / "rook.ssv"
        board, expected_targets = board_from_ssv(rook_ssv)
        coord = V(1, 2)
        self.assertEqual(board[coord], Piece(Role.ROOK, Player.ONE, moved=True))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_knight(self) -> None:
        knight_ssv = TEST_DATA_PATH / "knight.ssv"
        board, expected_targets = board_from_ssv(knight_ssv)
        coord = V(3, 3)
        self.assertEqual(board[coord], Piece(Role.KNIGHT, Player.ONE, moved=True))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_king(self) -> None:
        knight_ssv = TEST_DATA_PATH / "king.ssv"
        board, expected_targets = board_from_ssv(knight_ssv)
        coord = V(3, 3)
        self.assertEqual(board[coord], Piece(Role.KING, Player.ONE, moved=True))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_pawn(self) -> None:
        knight_ssv = TEST_DATA_PATH / "pawn.ssv"
        board, expected_targets = board_from_ssv(knight_ssv)
        coord = V(3, 6)
        self.assertEqual(board[coord], Piece(Role.PAWN, Player.ONE, moved=False))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))

    def test_castling(self) -> None:
        knight_ssv = TEST_DATA_PATH / "castling.ssv"
        board, expected_targets = board_from_ssv(knight_ssv)
        coord = V(4, 7)
        self.assertEqual(board[coord], Piece(Role.KING, Player.ONE, moved=False))
        self.assertEqual(set(expected_targets), set(board.targets[coord]))
