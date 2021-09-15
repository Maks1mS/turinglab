import csv
import pprint

def from_tur(filename):
    f = open(filename, "rb")
    raw = []
    byte = f.read(1)
    while byte:
        raw.append(byte)
        byte = f.read(1)
    indx = [0]
    empty = [b'\x00', b'\x00', b'\x00']
    for i in range(len(raw) - 2):
        if raw[i:i+3] == empty:
            indx.append(i)
            indx.append(i+3)
        
    data = []
    for i in range(1, len(indx)):
        packet = raw[indx[i - 1]:indx[i]]
        if packet != empty:
            data.append(packet)
    
    task = b''.join(data[1]).decode('cp1251')
    description = b''.join(data[4]).decode('cp1251')
    solution = b''.join(data[3][:-2]).decode('cp1251')
    solution = list(csv.reader(solution.split('\r\n'), delimiter='\t'))

    header = solution[:1][0][1:]

    solution_dict = [dict() for x in range(len(header))]

    for x in solution[1:]:
        symbol = x[0] if x[0] != ' ' else 'λ'

        for (i, action) in enumerate(x[1:]):
            action = list(action)
            if len(action) == 0:
                continue
            
            if action[0] == '_':
                action[0] = 'λ'

            action[2] = int(action[2]) - 1


            solution_dict[i][symbol] = action

    return solution_dict, task, description