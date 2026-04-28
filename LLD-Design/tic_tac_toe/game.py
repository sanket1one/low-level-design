import threading
from board import Board
from base_classes import WinningStrategy, GameObserver
from strategies import RowWinningStrategy, ColumnWinningStrategy, DiagonalWinningStrategy
from exceptions import InvalidMoveException
from constants import GameStatus, Symbol
from typing import Optional
from models import Player

class Game:
    def __init__(self, player1: Player, player2: Player, board_size: int):
        self._board = Board(board_size)
        self._players = [player1, player2]
        self._current_player_index = 0
        self._status = GameStatus.IN_PROGRESS
        self._winning_strategies = self._initialize_strategies()
        self._observer: list[GameObserver] = []
        self._lock = threading.Lock()
    

    def _initialize_strategies(self) -> list[WinningStrategy]:
        return [
            RowWinningStrategy(),
            ColumnWinningStrategy(),
            DiagonalWinningStrategy()
        ]

    def make_move(self, row:int, col: int) -> None:
        with self._lock:
            # Check if game is already over
            if self._status != GameStatus.IN_PROGRESS:
                raise InvalidMoveException("Game is already over!")

            # Validate the move
            if not self._board.is_cell_empty(row, col):
                raise InvalidMoveException(f"Cell ({row}, {col}) is already occupied")
            
            # place the symbol
            current_player = self._players[self._current_player_index]
            self._board.place_symbol(row, col, current_player.symbol)

            # check for win
            if self._check_win(row, col, current_player.symbol):
                self._status = (GameStatus.WINNER_X if current_player.symbol == Symbol.X
                               else GameStatus.WINNER_O)
                self.notify_observers()
                return
            

            # check for draw
            if self._board.is_full():
                self._status = GameStatus.DRAW
                self.notify_observers()
                return
            
            self._current_player_index = (self._current_player_index + 1) % 2

    def _check_win(self, row: int, col: int, symbol: Symbol) -> bool:
        for strategy in self._winning_strategies:
            if strategy.check_win(self._board, row, col, symbol):
                return True
        return False
    
    def add_observer(self, observer: GameObserver) -> None:
        self._observer.append(observer)

    def notify_observers(self) -> None:
        for observer in self._observer:
            observer.update(self)
    
    @property
    def board(self)-> Board:
        return self._board

    @property
    def current_player(self) -> Player:
        return self._players[self._current_player_index]
    
    @property
    def status(self) -> GameStatus:
        return self._status
    
    @property
    def winner(self) -> Optional[Player]:
        if self._status == GameStatus.WINNER_X:
            return next(p for p in self._players if p.symbol == Symbol.X)
        elif self._status == GameStatus.WINNER_O:
            return next(p for p in self._players if p.symbol == Symbol.O)
        else:
            return None
    
    def print_board(self) -> None:
        self._board.print_board()


