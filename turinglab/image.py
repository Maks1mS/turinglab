import pydot
import requests
import shutil

def get_image(filename, program):
    g = pydot.Dot('my_graph', nodesep=0.5)
    g.set_node_defaults(
        width='1.5',
        fontsize='18',
        shape='circle'
    )

    rows = 0
    cols = len(program.keys())

    for x in program.keys():
        if len(list(program[x].keys())) == 0: 
            continue
        rows = max(list(program[x].keys())[-1] + 1, rows)

    program_table = [None] * rows

    for i in range(rows):
        program_table[i] = [None] * cols

    symbols = [None] * cols

    for j, (symbol, value) in enumerate(program.items()):
        symbols[j] = symbol
        for i, (state, action) in enumerate(value.items()):
            program_table[state][j] = action

    g.add_node(pydot.Node(f'gz', label='<g<SUB>z</SUB>>', shape='circle'))

    for i in range(rows):
        g.add_node(pydot.Node(f'g{i}', label=f'<g<SUB>{i}</SUB>>', shape='circle'))
        for j in range(cols):
            action = program_table[i][j]
            if action is None: continue

            symbol, direction, state = action
            label = symbols[j] + '/' + symbol + '/' + ('R' if direction == '>' else 'L')
            src = f'g{i}'
            dst = f'g{"z" if state == -1 else state}'
            if src == dst:
                src = src + ':ne'
                dst = dst + ':se'
            g.add_edge(pydot.Edge(src, dst, label = label))


    g.write_raw(f'{filename}.dot', encoding='utf-8')

    try:
        g.write_svg(f'{filename}.svg', encoding='utf-8')
    except Exception:
        output_raw_dot = g.to_string()
        img_data = requests.get("https://quickchart.io/graphviz?graph=" + output_raw_dot).content
        with open(f'{filename}_quickchart.svg', 'wb') as handler:
            handler.write(img_data)
    