from typing import Optional
import threading
from scoreboard import Scoreboard
from game import Game
from models import Player
from constants import GameStatus

class TicTacToeSystem:
    _instance: Optional['TicTacToeSystem'] = None
    _lock = threading.Lock()

    def __init__(self):
        if TicTacToeSystem._instance is not None:
            raise RuntimeError("Use get_instance() to access TicTacToeSystem")
        self._scoreboard = Scoreboard()
        self._current_game:Optional['Game'] = None

    @classmethod
    def get_instance(cls) -> 'TicTacToeSystem':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
    

    def create_game(self, player1: Player, player2: Player, board_size: int = 3) -> Game:
        self._current_game = Game(player1, player2, board_size)
        self._current_game.add_observer(self._scoreboard)
        print(f"New game started: {player1.name} vs {player2.name}")
        return self._current_game

    def make_move(self, player: Player, row: int, col: int) -> None:
        if self._current_game is None:
            raise RuntimeError("No active game. Call create_game first.")
        self._current_game.make_move(row, col)
        self._current_game.print_board()

    @property
    def game_status(self) -> GameStatus:
        if self._current_game is None:
            raise RuntimeError("No active game.")
        return self._current_game.status

    def print_scoreboard(self) -> None:
        self._scoreboard.print_scoreboard()
    
    @classmethod
    def reset_instance(cls) -> None:
        with cls._lock:
            cls._instance = None

