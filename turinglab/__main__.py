import os
import sys
from argparse import ArgumentParser
from turinglab.image import get_image
from turinglab.input import from_file
from turinglab.emulator import Emulator
from turinglab.output import to_docx


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("input_file", type=str, help="Path to file with program",)
    parser.add_argument("output_dir", type=str, help="Output dir")
    parser.add_argument('-t','--tests', nargs='+', type=str, help='List of input strings for tests')
    parser.add_argument('-e','--empty-character', type=str, help='Empty character')
    parser.add_argument('-f','--force', default=False, action='store_true', help='Force rewrite output dir')
    return parser

def main():
    parser = get_parser()

    args = parser.parse_args()

    program = from_file(args.input_file)
    
    if args.force == False and os.path.exists(args.output_dir):
        print('Directory already exists!')
        return -1

    os.makedirs(args.output_dir, exist_ok=True)

    test_data = []

    for test in args.tests:
        test = test.replace(args.empty_character, 'λ')

        tm = Emulator(program, test)

        data = [tm.info()]

        while not tm.stopped:
            tm.step()
            data.append(tm.info())

        test_data.append(data)

    to_docx(os.path.join(args.output_dir, 'report.docx'), program, test_data)
    get_image(os.path.join(args.output_dir, 'graph'), program)

        
if __name__ == '__main__':
    main()