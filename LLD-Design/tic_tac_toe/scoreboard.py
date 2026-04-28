from collections import defaultdict
import threading
from game import Game
from models import Player
from base_classes import GameObserver

class Scoreboard(GameObserver):
    def __init__(self):
        self._scores: dict[str, int] = defaultdict(int)
        self._lock = threading.Lock()
    
    def update(self, game: Game) -> None:
        winner = game.winner
        if winner is not None:
            self.record_win(winner)
            print(f"Scoreboard updated: {winner.name} wins!")
        
    def record_win(self, player: Player) -> None:
        with self._lock:
            self._scores[player.name] += 1
    
    def get_score(self, player_name: str) -> str:
        return self._scores.get(player_name, 0)
    
    def print_scoreboard(self) -> None:
        print("\n===== SCOREBOARD =====")
        if not self._scores:
            print("No games played yet.")
        else:
            for name, score in self._scores.items():
                print(f"{name}: {score} wins")
        print("======================\n")
 
