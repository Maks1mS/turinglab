import re
from turinglab.emulator import Program, Movemement, Action


def from_file(filename: str):

    f = open(filename, "r")

    program = Program(blank_symbol="_")

    # program = dict()

    for line in f:
        symbol, *actions = line.replace("\n", "").split('\t')

        if symbol == " ":
            symbol = "_"

        for i, action in enumerate(actions):
            if not action:
                continue

            new_symbol, direction, *new_state = action
            new_state = int(''.join(new_state)) - 1

            movement = {
                '>': Movemement.R,
                '.': Movemement.E,
                '<': Movemement.L
            }[direction]

            program.set(i, symbol, Action(new_state, new_symbol, movement))

    f.close()

    return program
