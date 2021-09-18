import os
import sys
from argparse import ArgumentParser
from turinglab.image import get_image
from turinglab.input import from_file
from turinglab.emulator import Emulator
from turinglab.output import to_docx

def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("input_file", type=str, help="Path to file with program")
    parser.add_argument("input_string", type=str, help="Input symbols")
    parser.add_argument("output_dir", type=str, help="Output dir")

    return parser

def main():
    parser = get_parser()

    args = parser.parse_args()

    program = from_file(args.input_file)

    if os.path.exists(args.output_dir):
        print('Directory already exists!')
        return -1

    os.makedirs(args.output_dir)
        

    tm = Emulator(program, args.input_string)

    data = [tm.info()]

    while not tm.stopped:
        tm.step()
        data.append(tm.info())

    to_docx(os.path.join(args.output_dir, 'report.docx'), program, data)

    get_image(os.path.join(args.output_dir, 'graph'), program)

        
if __name__ == '__main__':
    main()