import sys
from turinglab.input import from_file
from turinglab.emulator import Emulator
from turinglab.output import to_docx
    

def main():
    program_file, input_string, docx = sys.argv[1:]

    program = from_file(program_file)

    tm = Emulator(program, input_string)

    data = [tm.info()]

    while not tm.stopped:
        tm.step()
        data.append(tm.info())

    to_docx(docx, data)
        
if __name__ == '__main__':
    main()