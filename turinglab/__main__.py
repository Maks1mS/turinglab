import sys
from turinglab.input import from_tur
from turinglab.emulator import Emulator
from turinglab.output import to_docx
    

def main():
    tur, input_string, docx = sys.argv[1:]

    [program,_,_] = from_tur(tur)

    tm = Emulator(program, input_string)

    data = [tm.info()]

    while not tm.stopped:
        tm.step()
        data.append(tm.info())

    to_docx(docx, data)
        
if __name__ == '__main__':
    main()