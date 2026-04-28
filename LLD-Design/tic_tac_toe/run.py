from system import TicTacToeSystem
from constants import Symbol
from models import Player

def main():
    system = TicTacToeSystem.get_instance()

    alice = Player("Alice", Symbol.X)
    bob = Player("Bob", Symbol.O)

    # Game 1: Alice wins
    print("========== GAME 1 ==========")
    system.create_game(alice, bob)

    system.make_move(alice, 0, 0)  # X at (0,0)
    system.make_move(bob, 1, 0)    # O at (1,0)
    system.make_move(alice, 0, 1)  # X at (0,1)
    system.make_move(bob, 1, 1)    # O at (1,1)
    system.make_move(alice, 0, 2)  # X at (0,2) - Alice wins!

    print(f"Game 1 Result: {system.game_status}")

    # Game 2: Bob wins
    print("\n========== GAME 2 ==========")
    system.create_game(alice, bob)

    system.make_move(alice, 0, 0)  # X at (0,0)
    system.make_move(bob, 1, 1)    # O at (1,1) - center
    system.make_move(alice, 0, 1)  # X at (0,1)
    system.make_move(bob, 0, 2)    # O at (0,2)
    system.make_move(alice, 2, 0)  # X at (2,0)
    system.make_move(bob, 2, 2)    # O at (2,2) - Bob wins diagonal!

    print(f"Game 2 Result: {system.game_status}")

    # Game 3: Draw
    print("\n========== GAME 3 ==========")
    system.create_game(alice, bob)

    system.make_move(alice, 0, 0)  # X
    system.make_move(bob, 0, 1)    # O
    system.make_move(alice, 0, 2)  # X
    system.make_move(bob, 1, 1)    # O
    system.make_move(alice, 1, 0)  # X
    system.make_move(bob, 1, 2)    # O
    system.make_move(alice, 2, 1)  # X
    system.make_move(bob, 2, 0)    # O
    system.make_move(alice, 2, 2)  # X - Draw!

    print(f"Game 3 Result: {system.game_status}")

    # Final scoreboard
    system.print_scoreboard()


if __name__ == "__main__":
    main()