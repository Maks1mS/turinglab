from turinglab.image import get_image
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Inches
from docx.enum.text import WD_LINE_SPACING
from docx.enum.text import WD_ALIGN_PARAGRAPH 

def add_state(p, state):
    p.add_run('q')
    index_text = p.add_run(str('z' if state == -1 else state))
    index_text.font.subscript = True

def create_paragraph(document):
    p = document.add_paragraph()
    style_paragraph(p)
    return p

def style_paragraph(p):
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE

def to_docx(filename, program, data):
    document = Document()
    
    style = document.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(14)

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
        
    for i in range(rows):
        for j in range(cols):
            action = program_table[i][j]
            if action is None: continue

            p = create_paragraph(document)
            add_state(p, i)

            symbol, direction, state = action

            p.add_run(symbols[j] + ' → ')
            add_state(p, state)
            p.add_run(symbol + ('R' if direction == '>' else 'L'))


    p = create_paragraph(document)

    table = document.add_table(rows + 1, cols + 1)
    table.style = 'Table Grid'
    table.autofit = True
    table.allow_autofit = True
    
    for i in range(0, rows):
        p = table.rows[i + 1].cells[0].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        style_paragraph(p)
        add_state(p, i)
    
    for i, x in enumerate(program.keys()):
        p = table.rows[0].cells[i + 1].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        style_paragraph(p)
        p.add_run(x)

    for i in range(rows):
        for j in range(cols):
            action = program_table[i][j]
            if action is None: continue

            p = table.rows[i + 1].cells[j + 1].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            style_paragraph(p)

            symbol, direction, state = action
            add_state(p, state)
            p.add_run(symbol)
            p.add_run('R' if direction == '>' else 'L')

    p = create_paragraph(document)

    for i, test in enumerate(data):
        p = create_paragraph(document)
        p.add_run(f'Test {i + 1}:')

        for j, data in enumerate(test):
            p = create_paragraph(document)
            p.add_run('K')

            index_text = p.add_run(str(j))
            index_text.font.subscript = True

            p.add_run(': ')

            head, state, tape = data
            offset = list(tape.keys())[0]
            head -= offset
            tape_str = ''.join(tape.values())

            p.add_run(tape_str[:head].lstrip('λ') + 'q')

            index_text = p.add_run(str('z' if state == -1 else state))
            index_text.font.subscript = True

            p.add_run(tape_str[head] + tape_str[head + 1:].rstrip('λ'))
        
    document.save(filename)