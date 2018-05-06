from task import *

task_number = '19.8'


def fill_document(doc: Document):
    """
    Fill document with solution
    @param doc: Document to be filled
    @return:
    """
    # Условие задачи
    with doc.create(Problem(task_number)):
        doc.append(r'Найти гамильтониан и составить канонические уравениния движения:')

        t = Symbol('t')
        q1, q2, q3, q4 = Function('q1')(t), Function('q2')(t), Function('q3')(t), Function('q4')(t)
        L = Rational(1, 2)*(diff(q1, t)**2 + diff(q2, t)**2) + Rational(1, 4)*(diff(q1, t) + diff(q3, t))**2 + \
            Rational(1, 4)*(diff(q2, t) + diff(q4, t))**2 - 2*(q1**2 + q2**2 - q1*q2) - Rational(1, 4)*(q3**2 + q4**2)

        doc.append(Dmath(Math(data=['L=', latex(L)], escape=False)))


    # Решение задачи
    with doc.create(Solution(task_number)):
        p1, p2, p3, p4 = Function('p_1')(t), Function('p_2')(t), Function('p_3')(t), Function('p_4')(t)

        q1_dot = diff(q1, t)
        q2_dot = diff(q2, t)
        q3_dot = diff(q3, t)
        q4_dot = diff(q4, t)

        q1_dot_func = Function(r'\dot{q_1}')(t)
        q2_dot_func = Function(r'\dot{q_2}')(t)
        q3_dot_func = Function(r'\dot{q_3}')(t)
        q4_dot_func = Function(r'\dot{q_4}')(t)

        def _make_sub(d: Function):
            return d.subs(q1_dot, q1_dot_func).subs(q2_dot, q2_dot_func).subs(q3_dot, q3_dot_func).subs(q4_dot, q4_dot_func)

        d1 = _make_sub(diff(L, q1_dot))
        d2 = _make_sub(diff(L, q2_dot))
        d3 = _make_sub(diff(L, q3_dot))
        d4 = _make_sub(diff(L, q4_dot))

        doc.append(Math(data=['\cfrac{\partial L}{\partial \dot{q_1}} = ', latex(d1)], escape=False))
        doc.append(Math(data=['\cfrac{\partial L}{\partial \dot{q_2}} = ', latex(d2)], escape=False))
        doc.append(Math(data=['\cfrac{\partial L}{\partial \dot{q_3}} = ', latex(d3)], escape=False))
        doc.append(Math(data=['\cfrac{\partial L}{\partial \dot{q_4}} = ', latex(d4)], escape=False))

        doc.append(r'Решая систему, получим:')
        q_dot = Matrix(solve_poly_system([d1 - p1, d2 - p2, d3 - p3, d4 - p4],
                          q1_dot_func, q2_dot_func, q3_dot_func, q4_dot_func)[0]).T

        def _make_sub(d: Function):
            return d.subs(q1_dot, q_dot[0]).subs(q2_dot, q_dot[1]).subs(q3_dot, q_dot[2]).subs(q4_dot, q_dot[3])

        p = Matrix([p1, p2, p3, p4])
        # Очень опасная строка
        doc.append(Multline(Math(data=
                        [r'\\q_' + str(pair[0]+1) + ' = ' + latex(pair[1]) + r'\\'
                         for pair in enumerate(solve_poly_system([d1 - p1, d2 - p2, d3 - p3, d4 - p4],
                                                                 q1_dot_func, q2_dot_func, q3_dot_func, q4_dot_func)[0])],
                        escape=False, inline=True)))
        doc.append(r'Теперь можно выписать гамильтониан')
        doc.append(Dmath(Math(data=['H = ', latex((q_dot*p)[0]), '-', latex(_make_sub(L)), '=',
                                    latex((q_dot*p)[0].simplify()), '-', latex(_make_sub(L).simplify()), '=',
                                    latex(((q_dot*p)[0] - _make_sub(L)).simplify())], escape=False)))
        doc.append(r'Это совпадает с ответами. Я реально заебался, когда это писал.')


if __name__ == '__main__':
    doc = Document('basic')
    fill_document(doc)
    fill_preambula(doc)
    doc.generate_pdf(task_number, clean_tex=False)
