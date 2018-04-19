import numpy as np
from pylatex import Document, Section, Subsection, Command, Math, Package
from pylatex import Matrix as TexMatrix
from pylatex.base_classes import Environment
from pylatex.utils import italic, NoEscape
from sympy import *
import os

task_number = '19.26'


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


def _hamiltoinian_definition():
    return NoEscape(r'H = \sum_{i=1}^n p_i \dot{q_i} - L \bigg\rvert_{\dot{q_i} = f_i (p, q)}')


def fill_document(doc: Document):
    """
    Fill document with solution
    @param doc: Document to be filled
    @return:
    """
    # Условие задачи
    with doc.create(Problem(task_number)):
        doc.append(NoEscape(r'Две материальные точки массами $m_1$ и $m_2$ связаны между собой упругим '
                            r'стержнем жесткости $c$ и помещены на гладкую горизонтальную плоскость; стержень не'
                            r'работает на изгиб и на кручение и в нерастянутом состоянии имеет длину $l_0$; массой'
                            r'стержня можно пренебречь. Составить канонические уравнения движения системы.'))

    # Решение задачи
    with doc.create(Solution(task_number)):
        doc.append(r'Запишем выражение для кинетической и потенциальной энергии:')
        m1, m2, c, l0, t= symbols('m1 m2 c l0 t')
        x, y, r, phi, x_dot, y_dot, r_dot, phi_dot = Function('x')(t), Function('y')(t), \
                                                     Function('r')(t), Function('phi')(t), \
                                                     Function('\dot{x}')(t), Function('\dot{y}')(t), \
                                                     Function('\dot{r}')(t), Function('\dot{\phi}')(t)
        mu = m1*m2/(m1+m2)
        T = Rational(1, 2)*(m1+m2)*(x_dot**2 + y_dot**2) + Rational(1, 2)*mu*(r_dot**2 + r**2*phi_dot**2)
        P = Rational(1, 2)*c*(r - l0)**2
        L = T - P
        doc.append(Math(data=[r'T = ', latex(T)], escape=False))
        doc.append(Math(data=[r'\text{П} = ', latex(P)], escape=False))
        doc.append(r'Остюда найдем лагранжиан, а потом гамильтониан:')
        doc.append(Math(data=[r'L = T - \text{П} = ', latex(L)], escape=False))
        # Это - функции от остальных
        p_x = diff(L, x_dot)
        p_y = diff(L, y_dot)
        p_r = diff(L, r_dot)
        p_phi = diff(L, phi_dot)
        # А это - просто символы
        px, py, pr, pphi = symbols(r'p_x p_y p_r p_\phi')
        #px, py, pr, pphi = Function('p_x')(t), Function('p_y')(t), Function('p_r')(t), Function('p_\phi')(t)

        doc.append(Math(data=[r'p_x = \cfrac{\partial L}{\partial \dot{x}} =', latex(p_x)], escape=False))
        doc.append(Math(data=[r'p_y = \cfrac{\partial L}{\partial \dot{y}} =', latex(p_y)], escape=False))
        doc.append(Math(data=[r'p_r = \cfrac{\partial L}{\partial \dot{r}} =', latex(p_r)], escape=False))
        doc.append(Math(data=[r'p_\phi = \cfrac{\partial L}{\partial \dot{\phi}} =', latex(p_phi)], escape=False))

        doc.append(r'Решая систему, находим:')
        sols = solve_poly_system([p_x - px, p_y - py, p_r - pr, p_phi - pphi], x_dot, y_dot, r_dot, phi_dot)[0]
        doc.append(Math(data=[r'\dot{x} = ', latex(sols[0])], escape=False))
        doc.append(Math(data=[r'\dot{y} = ', latex(sols[1])], escape=False))
        doc.append(Math(data=[r'\dot{r} = ', latex(sols[2])], escape=False))
        doc.append(Math(data=[r'\dot{\phi} = ', latex(sols[3])], escape=False))

        doc.append(r'Теперь выпишем гамильтониан:')
        H_old = p_x*sols[0] + p_y*sols[1] + p_r*sols[2] + p_phi*sols[3] - L
        # Подставим все в гамильтониан
        H = H_old.subs(x_dot, sols[0]).subs(y_dot, sols[1]).subs(r_dot, sols[2]).subs(phi_dot, sols[3])
        doc.append(Dmath(Math(data=[_hamiltoinian_definition(), '=', latex(H_old),
                                    r'\bigg\rvert_{\dot{q_i} = f_i (p, q)} =', latex(H)], escape=False)))
        doc.append(r'Отсюда легко найти канонические уравнения движения:')
        doc.append(Math(data=[r'\dot{p_x} = -\cfrac{\partial H}{\partial x} =', latex(diff(H, x))], escape=False))
        doc.append(Math(data=[r'\dot{p_y} = -\cfrac{\partial H}{\partial y} =', latex(diff(H, y))], escape=False))
        doc.append(Math(data=[r'\dot{p_r} = -\cfrac{\partial H}{\partial r} =', latex(diff(H, r))], escape=False))
        doc.append(Math(data=[r'\dot{p_\phi} = -\cfrac{\partial H}{\partial \phi} =', latex(diff(H, phi))], escape=False))


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
