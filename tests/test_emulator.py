from turinglab.emulator import Emulator
from turinglab.output import to_docx

def test_emulator():

    blank_symbol = '_'

    instructions = {
        '0': [['1', '>', 0], ['0', '<', 1]],
        '1': [['0', '>', 0], ['1', '<', 1]],
        blank_symbol: [[blank_symbol, '<', 1], [blank_symbol, '>', -1]]
    }

    input_string = '010'

    tm = Emulator(instructions, input_string, blank_symbol)

    while not tm.stopped:
        tm.step()

    head, _, tape = tm.info()
    output_string = "".join(tape.values()).strip(blank_symbol)

    assert output_string == '101'
    assert head == 0

