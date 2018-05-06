from pylatex import NewLine
from task import *

task_number = '23.24'


def fill_document(doc: Document):
    """
    Fill document with solution
    @param doc: Document to be filled
    @return:
    """
    xi, eta, phi = symbols('xi eta phi')
    x1, x2, x3 = Function('x1')(xi, eta, phi), Function('x2')(xi, eta, phi), Function('x3')(xi, eta, phi)
    p_xi, p_eta, p_phi = symbols(r'p_\xi p_\eta p_\phi')
    px1, px2, px3 = symbols(r'p_{x_1} p_{x_2} p_{x_3}')
    # Условие задачи
    with doc.create(Problem(task_number)):
        doc.append(NoEscape(r'Приведенные ниже выражения $x_i = x_i (q_1, q_2, q_3, t) ~(i = 1, 2, 3)$ определяют '
                            r'переход от декартовых координат к обобщенным координатам в механической системе '
                            r'с лагранжианом $L(x_i, \dot{x_i}, t)$. Найти соответствующие формулы преобразования '
                            r'обобщенных импульсов $p_{x_i} = p_{x_i} (q_1, q_2, q_3, p_1, p_2, p_3, t)$. Установить '
                            r'каноничность преобразования $x_i = x_i (q_1, q_2, q_3, t), ~~p_{x_i} = '
                            r'p_{x_i} (q_1, q_2, q_3, p_1, p_2, p_3, t) ~(i = 1, 2, 3)$'))

    # Решение задачи
    with doc.create(Solution(task_number)):
        doc.append(r'В одномерном случае импульс после преобразования будет задаваться формулой:')
        doc.append(Math(data=[latex(p_xi), '=', latex(px1*diff(x1, xi) + px2*diff(x2, xi) + px3*diff(x3, xi))], escape=False))
        doc.append(r'Для многомерного случая (всех трех обобщенных координат) имеем матрицу:')
        Jac = Matrix([[diff(x1, xi), diff(x2, xi), diff(x3, xi)],
                      [diff(x1, eta), diff(x2, eta), diff(x3, eta)],
                      [diff(x1, phi), diff(x2, phi), diff(x3, phi)]])
        p_new = Matrix([p_xi, p_eta, p_phi])
        p_old = Matrix([px1, px2, px3])
        doc.append(Math(data=[latex(p_new), '=', latex(Jac), latex(p_old)], escape=False))
        doc.append(r'Отсюда можно выразить ')
        doc.append(Math(data=[latex(px1), ',', latex(px2), ',', latex(px3)], escape=False, inline=True))
        doc.append(r':')
        doc.append(Math(data=[latex(p_old), '=', latex(Jac) + '^{-1}', latex(p_new)], escape=False))
        doc.append(r'Теперь зададим само преобразование:')
        sigma = Symbol('sigma')
        x1 = sigma*sqrt((xi**2 - 1)*(1 - eta**2))*cos(phi)
        x2 = sigma*sqrt((xi**2 - 1)*(1 - eta**2))*sin(phi)
        x3 = sigma*xi*eta
        doc.append(Math(data=['x_1 = ', latex(x1)], escape=False))
        doc.append(Math(data=[r'x_2 = ', latex(x2)], escape=False))
        doc.append(Math(data=[r'x_3 = ', latex(x3)], escape=False))
        doc.append(r'Считать производные, а потом и обратную матрицу -- дело явно нелюдское. '
                   r'Поэтому я и сделал все в Питоне!')
        doc.append(NewLine())
        doc.append(r'Подставляя функции, имеем:')
        Jac = Matrix([[diff(x1, xi), diff(x2, xi), diff(x3, xi)],
                      [diff(x1, eta), diff(x2, eta), diff(x3, eta)],
                      [diff(x1, phi), diff(x2, phi), diff(x3, phi)]])
        tmp = (Jac**-1)
        tmp.simplify()
        res = tmp*p_new
        doc.append(Dmath(''.join([latex(p_old), '=', latex(Jac) + '^{-1}', latex(p_new),
                                  '=', latex(tmp), latex(p_new),
                                  '=', latex(simplify(tmp*p_new))])))
        doc.append(Dmath(r'p_{x_1} = ' + latex(collect(res[0], phi))))
        doc.append(NewLine())
        doc.append(Dmath(r'p_{x_2} = ' + latex(collect(res[1], phi))))
        doc.append(NewLine())
        doc.append(Dmath(r'p_{x_3} = ' + latex(simplify(res[2]))))
        # Грязный хак. Сверяемся с ответами
        ans_1, ans_2, ans_3 = sqrt((xi**2 - 1)*(1 - eta**2))/sigma/(xi**2 - eta**2)*(xi*p_xi - eta*p_eta)*cos(phi) \
                              - p_phi*sin(phi)/sigma/sqrt((xi**2-1)*(1-eta**2)), \
                              sqrt((xi**2 - 1)*(1 - eta**2))/sigma/(xi**2 - eta**2)*(xi*p_xi - eta*p_eta)*sin(phi) \
                              + p_phi*cos(phi)/sigma/sqrt((xi**2-1)*(1-eta**2)), eta/sigma*(xi**2 - 1)/(xi**2 - eta**2)\
                              + xi*(1-eta**2)/(xi**2 - eta**2)
        doc.append(r'Последняя строка не сходится с ответом. Честно говоря, Питону я доверяю больше, чем Ханукаеву. '
                   r'Скатайте с ответов, если что)')


if __name__ == '__main__':
    doc = Document('basic')
    fill_document(doc)
    fill_preambula(doc)
    doc.generate_pdf(task_number, clean_tex=False)
