from abc import ABC, abstractmethod
from constants import Symbol
from game import Game
from board import Board

class WinningStrategy(ABC):
    @abstractmethod
    def check_win(self, board: Board, row: int, col: int, symbol: Symbol) -> bool:
        pass

class GameObserver(ABC):
    @abstractmethod
    def update(self, game: 'Game') -> None:
        pass