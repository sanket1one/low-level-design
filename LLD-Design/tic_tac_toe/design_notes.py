"""
Tic Tac Toe

"""

# Requirements
"""
1. Functional Requirements
- Game is played on 3*3 grid
- player-player game alternate turns, 'X' and 'O'
- detect annoucement of winner
- declare a draw if all cell are filled and no player won.
- reject invalid move
- maintain the score board.
- moves should be hardcode in a drive/demo class to simulate gameplay.


2. Non Functional Requirement
- oops principle
- modular and extensible
- testable and easy to maintain
- clear console output

3. Identify the core entity
- focus on noun
    1. game play 3x3 grid
        -> Board: entity
    2. board is made up of cell contain symbol or empty.
        -> Cell: Entity
    3. players alternate turn  identified by 'x' or 'o'
        -> player: Entity: name assigned symbol
    ENUM Symbol 'x' or 'o' and 'empty'

4.Game play
 - accept moves, validate them, check for wins, switch turns,  
 - Orchestrator: Game entity
 - Game State: Enum IN_PROGRESS, WINNER_X, WINNER_O, and DRAW

 5. Scoreboard
 - Scoreboard: how many times each player has won
 - TicTacToeSystem: Central controller that create game and maintain the score board.
"""

"""
Enttity Oveview

core  classes
TicTacToe System

1. interfaces

winningStrategy
-> Check whether someone won.

GameObserver
-> udpate the game

2. Core classes

Board
-> grid, size || Board(size) placeSymbol(row, col, symbol) isCellEmpty(row, col) isFull() printBoard()


Cell:
-> Symbol || isEmpty()


3. Game [Orchestrator]

-> Board board, Players[] player,int currentPlayerIndex,GameStatus status, List<WinningStrategies> winningStrategies, List<Observer> observers
||
-> GamePlay
-> makeMove
-> addObserver
-> notifyObserver

4. ScoreBoard

[interface] GameObserver || update(Game game) 
[class] ScoreBoard || map scores || Scoreboard() recordWin() printScoreboard() udpate()
[class] Player || name



5. Tick Tac Toe system

- TTC instance , ScoreBoard scoreBoard, Game currentGame || getInstane(), createGame(), makeMove(), printScoreBoard()

"""

# KEY Design Pattern

"""

[Startegy Design Pattern] (Win Detection)
 -> Testability
 -> Extensiblity
 -> Single responsiblity

    Game -> WinningStrategy[interface]

    [RowWinningStrategy, ColumnWinningStrategy, DiagonalWinningStrategy] -> implements [WinningStrategy]



[Observer Pattern] [Score Board Update]

-> adding new listener trivial(analytics, logging, replays)
-> keeps the game focused on game logic, not notification logistics.

    subject -notifies--> GameObserver[interface]

    [Implemented by]
    -> ScoreBoard , AnalyticsObserver future, ReplayRecordder future.

[Singelton] (TicTacToe System)

"""


