import week2.task_20_17
import task
from pylatex import Document, Command, NoEscape
import os

def fill_preambula(doc: Document):
    """
    Заполняет преамбулу. ОБЯЗАТЕЛЬНО ВЫЗВАТЬ!
    @param doc: Документ, в котором заполнить
    @return:
    """
    doc.packages = set()
    doc.preamble = []
    doc.documentclass = Command('documentclass', options=['12pt'], arguments=['book'])
    doc.preamble.append(NoEscape(r'\input{%s/preambula}' % os.getcwd()))


if __name__ == '__main__':
    doc = Document('basic')
    week2.task_20_17.fill_document(doc)
    fill_preambula(doc)
    doc.generate_pdf('all', clean_tex=False)
