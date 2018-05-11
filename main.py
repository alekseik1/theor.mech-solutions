import importlib
from task import *

all_tasks = [['19.8', '19.26'],
             ['20.17'],
             [],
             [],
             ['23.24'],
             ['24.33']]

debug = False


if __name__ == '__main__':
    doc = Document('basic')
    for week, tasks in enumerate(all_tasks):
        for task in tasks:
            mod = importlib.import_module(('week%s.task_{}_{}' % (week+1)).format(*task.split('.')))
            fill_document = getattr(mod, 'fill_document')
            fill_document(doc)

    fill_preambula(doc)
    doc.generate_pdf('all', clean_tex=not debug)
