from collections import defaultdict
from sortedcontainers import SortedDict
from copy import copy, deepcopy
from enum import IntEnum


class Movemement(IntEnum):
    R = 1
    L = -1
    E = 0


class Action:
    def __init__(
        self,
        state,
        symbol: chr,
        movement: Movemement
    ) -> None:
        self.state = state
        self.symbol = symbol
        self.movement = movement


class Program:
    data = dict()

    state_count = 0
    symbol_count = 0
    symbol_dict = dict()

    blank_symbol = 'λ'

    def __init__(self, blank_symbol: chr = 'λ') -> None:
        self.blank_symbol = blank_symbol

    def is_blank(self, symbol) -> bool:
        return symbol == self.blank_symbol

    def set(self, state, symbol, action) -> None:
        if state not in self.data:
            self.data[state] = dict()
            self.state_count += 1

        self.symbol_dict[symbol] = None
        self.data[state][symbol] = action

    def get(self, state, symbol) -> Action or None:
        if symbol not in self.data[state]:
            return None

        return self.data[state][symbol]

    def get_symbols(self):
        return list(self.symbol_dict.keys())


class Emulator():
    """
    A class used to emulate an Turing machine
    """

    class Tape:

        l_index = 0
        r_index = 0

        def __init__(self, input_string: str, blank_symbol: str) -> None:
            self.tape = SortedDict(dict(enumerate(input_string)))
            self.blank_symbol = blank_symbol

            r_index = len(input_string)
            pass

        def __deepcopy__(self, memo):
            id_self = id(self)
            _copy = memo.get(id_self)
            if _copy is None:
                _copy = type(self)('', self.blank_symbol)

                _copy.tape = deepcopy(self.tape)
                _copy.blank_symbol = self.blank_symbol
                _copy.l_index = self.l_index
                _copy.r_index = self.r_index

                memo[id_self] = _copy
            return _copy

        def __setitem__(self, key, value):
            self.tape[key] = value
            self.l_index = min(self.l_index, key)
            self.r_index = max(self.r_index, key)

        def __getitem__(self, key):
            if key not in self.tape:
                return self.blank_symbol

            return self.tape[key]

        def values(self):
            return self.tape.values()

    def __init__(self, program: Program, input_string: str = ''):
        self.head = 0
        self.state = 0
        self.stopped = False

        self.program = program
        self.tape = Emulator.Tape(input_string, program.blank_symbol)

    def step(self):
        if self.stopped is True:
            raise RuntimeError('Turing machine is stopped!')

        try:
            action = self.program.get(self.state, self.tape[self.head])

            self.tape[self.head] = action.symbol
            self.state = action.state
            self.head += int(action.movement)
            self.tape[self.head] = self.tape[self.head]

            if self.state == -1:
                self.stopped = True

        except Exception as err:
            self.stopped = True
            print('Error', err)

    def info(self):
        return [
            self.head,
            self.state,
            deepcopy(self.tape),
        ]
