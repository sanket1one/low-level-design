from constants import Symbol
from models import Cell
from exceptions import InvalidMoveException
class Board:
    def __init__(self, size: int):
        self._size = size
        self._grid: list[list[Cell]] = []
        self._initialize_board()
    
    def _initialize_board(self) -> None:
        self._grid = [[Cell() for _ in range(self._size)] for _ in range(self._size)]
    
    def place_symbol(self, row: int, col: int, symbol: Symbol)-> None:
        self._validate_position(row, col)
        self._grid[row][col].symbol = symbol
    

    def is_cell_empty(self, row: int, col: int) -> bool:
        self._validate_position(row, col)
        return self._grid[row][col].is_empty
    
    def is_full(self) -> bool:
        for row in self._grid:
            for cell in row:
                if cell.is_empty:
                    return False
        return True

    def get_cell(self, row:int, col: int) -> Cell:
        self._validate_position(row, col)
        return self._grid[row][col]

    def print_board(self) -> None:
        print()
        for i, row in enumerate(self._grid):
            row_str = " | ".join(f" {cell.symbol.display_char} " for cell in row)
            print(row_str)
            if i < self._size -1:
                print("-" * (self._size * 5 - 1))
        print()
    
    @property
    def size(self)-> int:
        return self._size
    
    def _validate_position(self, row:int , col:int) -> None:
         if row < 0 or row >= self._size or col < 0 or col >= self._size:
            raise InvalidMoveException(f"Position ({row}, {col}) is out of bounds")
    



