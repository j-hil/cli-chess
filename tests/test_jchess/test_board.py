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
        queen = board[V(3, 3)]
        self.assertEqual(queen, Piece(Role.QUEEN, Player.TWO, V(3, 3)))
        assert queen
        self.assertEqual(set(expected_targets), set(queen.targets))

    def test_bishop(self) -> None:
        bishop_ssv = TEST_DATA_PATH / "bishop.ssv"
        board, expected_targets = board_from_ssv(bishop_ssv)
        bishop = board[V(3, 3)]
        self.assertEqual(bishop, Piece(Role.BISHOP, Player.ONE, V(3, 3)))
        assert bishop
        self.assertEqual(set(expected_targets), set(bishop.targets))

    def test_rook(self) -> None:
        rook_ssv = TEST_DATA_PATH / "rook.ssv"
        board, expected_targets = board_from_ssv(rook_ssv)
        rook = board[V(1, 2)]
        self.assertEqual(rook, Piece(Role.ROOK, Player.ONE, V(1, 2)))
        assert rook
        self.assertEqual(set(expected_targets), set(rook.targets))

    def test_knight(self) -> None:
        knight_ssv = TEST_DATA_PATH / "knight.ssv"
        board, expected_targets = board_from_ssv(knight_ssv)
        knight = board[V(3, 3)]
        self.assertEqual(knight, Piece(Role.KNIGHT, Player.ONE, V(3, 3)))
        assert knight
        self.assertEqual(set(expected_targets), set(knight.targets))

    def test_king(self) -> None:
        knight_ssv = TEST_DATA_PATH / "king.ssv"
        board, expected_targets = board_from_ssv(knight_ssv)
        king = board[V(3, 3)]
        self.assertEqual(king, Piece(Role.KING, Player.ONE, V(3, 3)))
        assert king
        self.assertEqual(set(expected_targets), set(king.targets))

    def test_pawn(self) -> None:
        knight_ssv = TEST_DATA_PATH / "pawn.ssv"
        board, expected_targets = board_from_ssv(knight_ssv)
        pawn = board[V(3, 6)]
        self.assertEqual(pawn, Piece(Role.PAWN, Player.ONE, V(3, 6)))
        assert pawn
        self.assertEqual(set(expected_targets), set(pawn.targets))

    def test_castling(self) -> None:
        knight_ssv = TEST_DATA_PATH / "castling.ssv"
        board, expected_targets = board_from_ssv(knight_ssv)
        coord = V(4, 7)
        king = board[coord]
        self.assertEqual(king, Piece(Role.KING, Player.ONE, coord))
        assert king
        self.assertEqual(set(expected_targets), set(king.targets))
