import sys
from argparse import ArgumentParser
from turinglab.input import from_file
from turinglab.emulator import Emulator
from turinglab.output import to_docx

def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("input_file", type=str, help="Path to file with program")
    parser.add_argument("input_string", type=str, help="Input symbols")
    parser.add_argument("output_file", type=str, help="Output file")

    return parser

def main():
    parser = get_parser()

    args = parser.parse_args()


    program = from_file(args.input_file)

    tm = Emulator(program, args.input_string)

    data = [tm.info()]

    while not tm.stopped:
        tm.step()
        data.append(tm.info())

    to_docx(args.output_file, data)
        
if __name__ == '__main__':
    main()