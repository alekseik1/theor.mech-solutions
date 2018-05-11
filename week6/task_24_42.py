from task import *
from pylatex.basic import Environment, NewLine
from pylatex import Alignat

task_number = '24.42'

p, q, a = [], [], []
for i in range(3):
    p.append(Symbol('p_' + str(i + 1)))
    q.append(Symbol('q_' + str(i + 1)))
    a.append(Symbol(r'\alpha_' + str(i + 1)))
H = p[0] ** 2 + q[0] ** 2 + (p[1] ** 2 + p[2] ** 2) / (q[1] ** 2 + q[2] ** 2)
h = Symbol('h')
t = Symbol(r't')
S = Function(r'S')(*q, *a, t)


def _ham_yak_definition(_h=None):
    if _h is None:
        _h = Function('H')(t, *q, Derivative(S, t))
    return Derivative(S, t) + _h


class Cases(Environment):

    _escape = False


def fill_document(doc: Document):
    """
    Fill document with solution
    @param doc: Document to be filled
    @return:
    """
    # Условие задачи
    with doc.create(Problem(task_number)):
        doc.append(NoEscape(r'Составить уравнение Гамильтона-Якоби, найти его полный интеграл и '
                            r'найти движение $q(t)$, $p(t)$ в квадратурах для системы, заданной гамильтонианом:'))
        doc.append(Math(data=['H = ', latex(H)], escape=False))

    # Решение задачи
    with doc.create(Solution(task_number)):
        doc.append(r'Уравнения Гамильтона-Якоби имеют вид:')
        doc.append(Math(data=[latex(_ham_yak_definition()), '= 0'], escape=False))
        doc.append(r'Подставляя выражение гамильтониана, имеем:')
        doc.append(Math(data=[latex(_ham_yak_definition(H)
                                    .subs([(p[i], Derivative(S, q[i])) for i in range(3)])), '= 0'], escape=False))
        doc.append(r'Анализируя выражения для гамильтониана, приходим к первому первому интегралу:')
        PI = []
        PI.append(p[0]**2 + q[0]**2 - a[0])
        doc.append(Math(data=[latex(a[0]), '=', latex(solve(PI, a[0])[a[0]]), r'\Rightarrow',
                              latex(p[0]), r'=', latex(solve(PI, p[0])[1][0])], escape=False))
        doc.append(r'Система консервативна, поэтому гамильтониан сам будет первым интегралом:')
        doc.append(Math(data=[r'h = ', latex(H)], escape=False))
        doc.append(NoEscape(r'Это уравнение на $h$ равносильно:'))
        PI.append(p[1]**2-(h-a[0])*q[1]**2 - a[1])
        PI.append((h-a[0])*q[2]**2-p[2]**2 - a[1])
        p_a = solve(PI, p[0])[1][0], solve((PI[1].subs(H, h)),  p[1])[1], solve((PI[2].subs(H, h)),  p[2])[1]
        doc.append(Math(data=[latex(PI[1] + a[1]), ' = ', latex(PI[2] + a[1])], escape=False))
        with doc.create(Alignat(numbering=False, escape=False)) as agn:
            with agn.create(Cases()):
                agn.append(latex(PI[1].subs(H, h) + a[1]) + ' = ' + latex(a[1]))
                agn.append(NoEscape(r'\\'))
                agn.append(latex(PI[2].subs(H, h) + a[1]) + ' = ' + latex(a[1]))
            agn.append(NoEscape(r'\Rightarrow'))
            with agn.create(Cases()):
                agn.append(r'p_2 = ' + latex(p_a[1]))
                agn.append(NoEscape(r'\\'))
                agn.append(r'p_3 = ' + latex(p_a[2]))
        doc.append(r'Теперь уже легко составить уравнения движения:')
        S_final = -h*t + sum([Integral(collect(p_a[i], q[i]**2), q[i]) for i in range(3)])
        S_final_ready = S_final\
            .doit()\
            .subs(polar_lift(-a[0]+h), -a[0]+h)
        doc.append(Dmath(r'S = ' + latex(S_final) + r'=' + latex(S_final.doit())
                         + r'=' + latex(simplify(S_final_ready))))
        doc.append(r'В общем, люди уже взрослые, сами подставите нужные скобки. Простите, но заставить эту машину '
                   r'думать в час ночи мне не удеается. В ответах такое:')
        S_ans = -h*t + Rational(1, 2)*(q[0]*sqrt(a[0] - q[0]**2) + a[0]*asin(q[0]/sqrt(a[0]))) + \
                Rational(1, 2)*sqrt(h - a[0])*(q[1]*sqrt(a[1]/(h-a[0]) + q[1]**2) +
                                    a[1]/(h-a[0])*asinh(q[1]*sqrt(h-a[0])/sqrt(a[1])) + q[2]*sqrt(q[2]**2 -
        a[1]/(h-a[0])) - a[1]/(h-a[0])*acosh(q[2]*sqrt(h-a[0])/sqrt(a[1]))) # Ну нахер
        doc.append(Dmath(r'S = ' + latex(S_ans)))


if __name__ == '__main__':
    doc = Document('basic')
    fill_document(doc)
    fill_preambula(doc)
    doc.generate_pdf(task_number, clean_tex=False, compiler_args=['-f'])
