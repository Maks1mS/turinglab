from collections import defaultdict

DIRECTIONS = {
    '>': 1,
    '<': -1,
    '.': 0
}


class Emulator():
    '''
    A class used to emulate an Turing machine
    '''

    def __init__(self, instructions, input_string: str = '', blank_symbol: chr = 'λ'):
        self.head = 0
        self.current_state = 0

        self.blank_symbol = blank_symbol
        self.instructions = instructions

        self.stopped = False

        self.tape = defaultdict(lambda: self.blank_symbol, dict(enumerate(input_string)))

    def step(self):
        if self.stopped == True:
            raise RuntimeError('Turing machine is stopped!')

        symbol = self.tape[self.head]

        try:
            symbol, direction, state = self.instructions[symbol][self.current_state]
            self.tape[self.head] = symbol

            self.current_state = state
            self.head += DIRECTIONS[direction]
            
            self.tape[self.head] = self.tape[self.head]
            
            if self.head < 0:
                self.tape = defaultdict(lambda: self.blank_symbol, (sorted(self.tape.items())))

            if self.current_state == -1:
                self.stopped = True

        except:
            self.stopped = True

    def info(self):
        return [self.head, self.current_state, defaultdict(lambda: self.blank_symbol, self.tape)]

        

