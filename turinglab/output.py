from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING
from docx.enum.text import WD_ALIGN_PARAGRAPH 

def add_state(p, state):
    p.add_run('q')
    index_text = p.add_run(str('z' if state == -1 else state))
    index_text.font.subscript = True

def to_docx(filename, program, data):
    document = Document()
    
    style = document.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(14)

    rows = 0
    cols = len(program.keys())

    for x in program.keys():
        rows = max(list(program[x].keys())[-1] + 1, rows)

    table = document.add_table(rows + 1, cols + 1)
    table.style = 'Table Grid'
    table.autofit = True
    table.allow_autofit = True
    
    for i in range(1, rows + 1):
        p = table.rows[i].cells[0].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        add_state(p, i)
    
    for i, x in enumerate(program.keys()):
        p = table.rows[0].cells[i + 1].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        p.add_run(x)

    for j, (value) in enumerate(program.values()):
        for i, (state, action) in enumerate(value.items()):
            p = table.rows[state + 1].cells[j + 1].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE

            symbol, direction, state = action
            add_state(p, state)
            p.add_run(symbol)
            p.add_run('R' if direction == '>' else 'L')

    p = document.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE

    for i in range(len(data)):
        p = document.add_paragraph('K')

        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE

        index_text = p.add_run(str(i))
        index_text.font.subscript = True

        p.add_run(': ')

        head, state, tape = data[i]
        offset = list(tape.keys())[0]
        head -= offset
        tape_str = ''.join(tape.values())

        p.add_run(tape_str[:head].lstrip('λ') + 'q')

        index_text = p.add_run(str('z' if state == -1 else state))
        index_text.font.subscript = True

        p.add_run(tape_str[head] + tape_str[head + 1:].rstrip('λ'))
        
    document.save(filename)