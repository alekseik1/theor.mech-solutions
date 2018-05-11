from task import *
from pylatex.basic import Environment, NewLine
from pylatex import Alignat

task_number = '24.33'


class Cases(Environment):

    _escape = False


def fill_document(doc: Document):
    """
    Fill document with solution
    @param doc: Document to be filled
    @return:
    """
    p = [0]*3
    q = [0]*3
    p[1], p[2], q[1], q[2] = symbols(r'p_1 p_2 q_1 q_2')
    H = p[1]*q[2]+p[2]*q[1]
    # Условие задачи
    with doc.create(Problem(task_number)):
        doc.append(NoEscape(r'В задачах 24.32-24.35 система задается своим гамильтонианом $H(\vec{q}, \vec{p}, t)$. '
                            r'Подвергнуть систему такому каноническому преобразованию, '
                            r'чтобы в новых переменных полный интеграл соответствующего уравнения Гамильтона-Якоби '
                            r'можно было найти методом разделения переменных. Найти этот полный интеграл и закон '
                            r'движения $q(t)$, $p(t)$ в исходных переменных.'))
        doc.append(Math(data=['H = ', latex(H)], escape=False))

    # Решение задачи
    with doc.create(Solution(task_number)):
        p_ = [0]*3
        q_ = [0]*3
        for i in range(1, 3):
            p_[i] = Symbol(r'\widetilde{p_%s}' % i)
            q_[i] = Symbol(r'\widetilde{q_%s}' % i)
        Z = [Rational(1, 2)*(p[1]+q[2]) - p_[1], Rational(1, 2)*(p[1] - q[2]) - p_[2],
                                 Rational(1, 2)*(q[1] - p[2]) - q_[1], Rational(1, 2)*(p[2]+q[1]) - q_[2]]
        doc.append(r'В качестве преобразования возьмем (да-да, я взял это с ответов; вообще, похожее объяснял Жестков '
                   r'еще во 2 семестре):')
        doc.append(NewLine())
        with doc.create(Alignat(numbering=False, escape=False)) as agn:
            with agn.create(Cases()):
                for i in range(1, 3):
                    agn.append(Math(data=[latex(p_[i]), '=', latex(solve(Z, p_[i])[p_[i]]), r'\\',
                                          latex(q_[i]), '=', latex(solve(Z, q_[i])[q_[i]]), r'\\'], escape=False, inline=True))
        doc.append(r'Поищем валентность и производящую функцию:')
        doc.append(Math(data=[r'\sum_{i=1}^2\left(', r'\widetilde p_i', r'\delta \widetilde q_i', '-',
                              r'c~p_i \delta q_i', r'\right) = ', r'-\delta F'], escape=False))
        c = Rational(1, 2)
        F = Rational(1, 2)*p[2]*q[2]
        a = (0, *symbols(r'\alpha_1 \alpha_2'))
        t = Symbol('t')
        S = Function('S')(*q_[1:], *a, t)
        H_ = Rational(1, 2)*(p_[1]**2 - p_[2]**2 + q_[2]**2 - q_[1]**2)
        doc.append(NoEscape(r'Подставляя и преобразуя, имеем:'))
        with doc.create(Alignat(numbering=False, escape=False)) as agn:
            agn.append(Math(data=[r'c = ' + latex(c), r',~~F = ', latex(F), r',~~S = F'], escape=False))
        doc.append(NoEscape(r'Здесь $S$ -- полный интеграл. При этом гамильтониан находим по формуле:'))
        doc.append(Math(data=[r'\widetilde H', ' = ', latex(Derivative(Function('S')(*p[1:], *q[1:], t), t)), r' + c~H',
                              r'=', latex(diff(F, t) + c*H), r'=', latex(H_)], escape=False))
        doc.append(r'Уравнения Гамильтона-Якоби:')
        doc.append(Math(data=[latex(Derivative(S, t) +
                                    simplify(H_.subs([(p_[i], Derivative(S, q_[i])) for i in range(1, 3)]))), r'=0'], escape=False))
        PI = (p_[1]**2 - q_[1]**2 - a[1], q_[2]**2 - p_[2]**2 - a[2])
        doc.append(r'Отсюда первые интегралы:')
        with doc.create(Alignat(numbering=False, escape=False)) as agn:
            with agn.create(Cases()):
                for key, value in solve(PI, *a).items():
                    agn.append(latex(key) + r' = ' + latex(value))
                    agn.append(NoEscape(r'\\'))
        h = Symbol('h')
        doc.append(r'Тогда запишем полный интеграл:')
        p_n = [0] + [solve(PI, p_[i])[1][0] for i in range(1, 3)]
        S_n = -h*t
        for i in range(1, 3):
            S_n += Integral(p_n[i], q_[i])
        doc.append(Math(data=[r'S = ' + latex(S_n) + r' = ' + latex(S_n.doit())], escape=False))
        S_n = S_n.doit()
        doc.append(r'Страшно? Мне тоже. Но надо еще уравнения движения найти. К сожалению, я не смог это сделать. '
                   r'Может, найдется герой, у которого все получится?')
        b = (0, *symbols(r'\beta_1 \beta_2'))
        KE = [Derivative(S_n, a[i]) + b[i] for i in range(1, 3)]



if __name__ == '__main__':
    doc = Document('basic')
    fill_document(doc)
    fill_preambula(doc)
    doc.generate_pdf(task_number, clean_tex=False, compiler_args=['-f'])
