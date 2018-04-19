import week2.task_20_17
import task
from pylatex import Document, Command, NoEscape
import os
import importlib

all_tasks = [['19.8', '19.26'],
         ['20.17']]

debug = False

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
    for week, tasks in enumerate(all_tasks):
        for task in tasks:
            mod = importlib.import_module(('week%s.task_{}_{}' % (week+1)).format(*task.split('.')))
            fill_document = getattr(mod, 'fill_document')
            fill_document(doc)

    #week2.task_20_17.fill_document(doc)
    fill_preambula(doc)
    doc.generate_pdf('all', clean_tex=not debug)
