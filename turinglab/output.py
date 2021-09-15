from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING

def to_docx(filename, data):
    document = Document()
    section = document.sections[0]

    sectPr = section._sectPr
    cols = sectPr.xpath('./w:cols')[0]
    cols.set(qn('w:num'),'2')
    
    style = document.styles['Normal']
    
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(14)

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