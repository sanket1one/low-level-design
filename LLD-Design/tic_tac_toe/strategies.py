
from constants import Symbol
from board import Board
from base_classes import WinningStrategy

class RowWinningStrategy(WinningStrategy):
    def check_win(self, board: Board, row: int, col: int, symbol: Symbol):
        size = board.size
        for c in range(size):
            if board.get_cell(row, c).symbol != symbol:
                return False
        return True

class ColumnWinningStrategy(WinningStrategy):
    def check_win(self, board: Board, row: int, col: int, symbol: Symbol) -> bool:
        size = board.size
        for r in range(size):
            if board.get_cell(r, col).symbol != symbol:
                return False
        return True

class DiagonalWinningStrategy(WinningStrategy):
    def check_win(self, board: Board, row: int, col: int, symbol: Symbol) -> bool:
        size = board.size

        # Check main diagonal (top-left to bottom-right)
        main_diagonal_win = True
        for i in range(size):
            if board.get_cell(i, i).symbol != symbol:
                main_diagonal_win = False
                break

        if main_diagonal_win:
            return True

        # Check anti-diagonal (top-right to bottom-left)
        for i in range(size):
            if board.get_cell(i, size - 1 - i).symbol != symbol:
                return False
        return True