import os

from pylatex import Document, Command, Math, LineBreak, Subsection, NewLine
from pylatex import Matrix as TexMatrix
from pylatex.base_classes import Environment
from pylatex.utils import NoEscape, italic
from sympy import *
task_number = '20.17'


class Problem(Environment):

    def __init__(self, number=''):
        super(Problem, self).__init__()
        self.arguments = [number]


class Solution(Environment):

    def __init__(self, number=''):
        super(Solution, self).__init__()
        self.arguments = [number]


# Определение матрицы Якоби
def _jac_definition():
    _p1, _p2, _q1, _q2 = symbols('p1 p2 q1 q2')
    _phi1, _phi2, _phi3 = Function('phi1')(_p1, _p2, _q1, _q2), Function('phi2')(_p1, _p2, _q1, _q2), Function('phi3')(_p1, _p2, _q1, _q2)
    return Matrix([[diff(_phi1, _p1), diff(_phi1, _p2), diff(_phi1, _q1), diff(_phi1, _q2)],
                  [diff(_phi2, _p1), diff(_phi2, _p2), diff(_phi2, _q1), diff(_phi2, _q2)],
                  [diff(_phi3, _p1), diff(_phi3, _p2), diff(_phi3, _q1), diff(_phi3, _q2)]])


def fill_document(doc: Document):
    """
    Fill document with solution
    @param doc: Document to be filled
    @return:
    """

    with doc.create(Problem(task_number)):
        doc.append(r'Проверить, являются ли функции ')

        p1, p2, q1, q2 = symbols('p1 p2 q1 q2')
        H = p1*p2 + q1*q2
        phi1 = p1**2 + q2**2
        phi2 = p2**2 + q1**2

        doc.append(Math(data=['\phi_1 = ', latex(phi1)], escape=False, inline=True))
        doc.append(NoEscape('~и~'))
        doc.append(Math(data=['\phi_2 = ', latex(phi2)], escape=False, inline=True))
        doc.append(NoEscape(r'~первыми интегралами.'))

    with doc.create(Solution(task_number)):
        doc.append('Для проверки воспользуемся скобками Пуассона:\n')
        # phi1
        doc.append(NoEscape(r'\underline{$\phi_1$}:'))
        m1 = Matrix([diff(phi1, q1), diff(phi1, q2)]).T
        m2 = Matrix([diff(H, p1), diff(H, p2)])
        m3 = Matrix([diff(phi1, p1), diff(phi1, p2)]).T
        m4 = Matrix([diff(H, q1), diff(H, q2)])
        doc.append(Math(data=['(\phi_1, H) = ',
                              latex(m1), latex(m2), '-',
                              latex(m3), latex(m4), '=',
                              latex((m1*m2)[0]), '-', latex((m3*m4)[0]), '=', latex((m1*m2 - m3*m4)[0])], escape=False))
        doc.append(NoEscape(r'$\Rightarrow \phi_1$ \underline{является} первым интегралом \\'))
        # phi2
        #doc.append(LatexObject())
        doc.append(NoEscape(r'\underline{$\phi_2$}:'))
        m1 = Matrix([diff(phi2, q1), diff(phi2, q2)]).T
        m2 = Matrix([diff(H, p1), diff(H, p2)])
        m3 = Matrix([diff(phi2, p1), diff(phi2, p2)]).T
        m4 = Matrix([diff(H, q1), diff(H, q2)])
        doc.append(Math(data=['(\phi_2, H) = ',
                              latex(m1), latex(m2), '-',
                              latex(m3), latex(m4), '=',
                              latex((m1*m2)[0]), '-', latex((m3*m4)[0]), '=', latex((m1*m2 - m3*m4)[0])], escape=False))
        doc.append(NoEscape(r'$\Rightarrow \phi_2$ \underline{является} первым интегралом \\'))

        # phi3
        doc.append(NoEscape(r'Найдем $\phi_3$:'))
        m1 = Matrix([diff(phi1, q1), diff(phi1, q2)]).T
        m2 = Matrix([diff(phi2, p1), diff(phi2, p2)])
        m3 = Matrix([diff(phi1, p1), diff(phi1, p2)]).T
        m4 = Matrix([diff(phi2, q1), diff(phi2, q2)])
        phi3 = (m1*m2 - m3*m4)[0]
        doc.append(Math(data=['\phi_3 = (\phi_1, \phi_2) = ',
                              latex(m1), latex(m2), '-',
                              latex(m3), latex(m4), '=',
                              latex((m1*m2)[0]), '-', latex((m3*m4)[0]), '=', latex((m1*m2 - m3*m4)[0]), '= \phi_3'], escape=False))
        doc.append(NoEscape(r'\textit{Вообще, мы могли бы сразу сказать, что $\phi_3$ '
                            r'является первым интегралом по т. Пуассона. Но мы это и проверим!} \\'))

        # phi2
        doc.append(NoEscape(r'\underline{$\phi_3$}:'))
        m1 = Matrix([diff(phi3, q1), diff(phi3, q2)]).T
        m2 = Matrix([diff(H, p1), diff(H, p2)])
        m3 = Matrix([diff(phi3, p1), diff(phi3, p2)]).T
        m4 = Matrix([diff(H, q1), diff(H, q2)])
        doc.append(Math(data=['(\phi_3, H) = ',
                              latex(m1), latex(m2), '-',
                              latex(m3), latex(m4), '=',
                              latex((m1 * m2)[0]), '-', latex((m3 * m4)[0]), '=', latex((m1 * m2 - m3 * m4)[0])],
                        escape=False))
        doc.append(NoEscape(r'$\Rightarrow \phi_3$ \underline{является} первым интегралом \\'))
        doc.append(LineBreak())

        # Независимость.
        doc.append(r'Проверим независимость ')
        doc.append(Math(data=['\phi_1,~', '\phi_2,~', '\phi_3:'], escape=False, inline=True))
        doc.append(NewLine())
        J = Matrix([[diff(phi1, p1), diff(phi1, p2), diff(phi1, q1), diff(phi1, q2)],
                    [diff(phi2, p1), diff(phi2, p2), diff(phi2, q1), diff(phi2, q2)],
                    [diff(phi3, p1), diff(phi3, p2), diff(phi3, q1), diff(phi3, q2)]])
        doc.append(Math(data=['J = ', latex(_jac_definition())], escape=False))
        doc.append(Math(data=['=', latex(J)], escape=False))
        doc.append(r'Чтобы первые интегралы были независимы, необходимо и достаточно, чтобы ранг матрицы равнялся'
                   r' максимально возможному, т.е. 3. Для проверки этого используются миноры (погуглите, как)'
                   r'Подсчитаем, например, минор, состоящий из первых трех столбцов:')
        J.col_del(3)
        doc.append(Math(data=['\Delta_1 = ', latex(det(J)), '=', latex(det(J).simplify()), '\\neq 0'], escape=False))
        doc.append(NoEscape(r'Отсюда заключаем, что первые интегралы \underline{независимы}.'))


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
