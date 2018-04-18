import numpy as np
from pylatex import Document, Section, Subsection, Command, Math, Package
from pylatex.base_classes import Environment
from pylatex.utils import italic, NoEscape
import os

task_number = ''


class Problem(Environment):

    def __init__(self, number=''):
        super(Problem, self).__init__()
        self.arguments = [number]


class Solution(Environment):

    def __init__(self, number=''):
        super(Solution, self).__init__()
        self.arguments = [number]


def fill_document(doc: Document):
    """
    Fill document with solution
    @param doc: Document to be filled
    @return:
    """
    pass


def fill_preambula(doc: Document):
    """
    Заполняет преамбулу. ОБЯЗАТЕЛЬНО ВЫЗВАТЬ!
    @param doc: Документ, в котором заполнить
    @return:
    """
    doc.packages = set()
    doc.preamble = []
    doc.documentclass = Command('documentclass', options=['12pt'], arguments=['book'])
    doc.preamble.append(NoEscape(r'\input{%s/preambula}' % os.path.abspath(os.path.join(os.getcwd(), os.pardir))))


if __name__ == '__main__':
    doc = Document('basic')
    fill_document(doc)
    fill_preambula(doc)
    doc.generate_pdf(task_number, clean_tex=False)
