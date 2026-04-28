from constants import Symbol

class Player:
    def __init__(self, name: str, symbol: Symbol):
        if symbol == Symbol.EMPTY:
            raise ValueError("Player cannot have Empty symbol")
        self._name = name
        self._symbol = symbol
    
    @property
    def name(self) -> str:
        return self._name 

    @property
    def symbol(self) -> Symbol:
        return self._symbol
    
    def __str__(self) -> str:
        return f"{self._name} ({self._symbol.display_char})"


class Cell:
    def __init__(self):
        self._symbol = Symbol.EMPTY
    
    @property
    def symbol(self) -> Symbol:
        return self._symbol

    @symbol.setter
    def symbol(self, value: Symbol) -> None:
        self._symbol = value

    @property
    def is_empty(self) -> bool:
        return self._symbol == Symbol.EMPTY
