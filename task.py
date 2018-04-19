import numpy as np
from pylatex import Document, Section, Subsection, Command, Math, Package
from pylatex import Matrix as TexMatrix
from pylatex.base_classes import Environment
from pylatex.utils import italic, NoEscape
from sympy import *
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


# Не очень сильная вещь. Позволяет разбивать выражения, но не делает этого автоматическ
class Multline(Environment):

    _escape = False
    content_separator = ''

    def __init__(self, data=''):
        super(Multline, self).__init__()
        self.data = data


# СИЛЬНАЯ ВЕЩЬ. Позволяет автоматически разбивать длинные выражения
class Dmath(Environment):

    _escape = False
    content_separator = ''

    def __init__(self, data=''):
        super(Dmath, self).__init__()
        self.data = data
        self.packages = [Package(name='breqn')]

def fill_document(doc: Document):
    """
    Fill document with solution
    @param doc: Document to be filled
    @return:
    """
    # Условие задачи
    with doc.create(Problem(task_number)):
        pass

    # Решение задачи
    with doc.create(Solution(task_number)):
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
