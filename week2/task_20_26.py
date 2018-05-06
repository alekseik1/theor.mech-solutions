from task import *

task_number = '20.26'


def fill_document(doc: Document):
    """
    Fill document with solution
    @param doc: Document to be filled
    @return:
    """

    t, i, n = symbols('t i n')
    q_1, p_1, q_i, p_i = symbols('q_1 p_1 q_i p_i')
    F = Function('F')(p_i(t), t)
    H = (p_1**2+ q_1**2)*F
    # Условие задачи
    with doc.create(Problem(task_number)):
        doc.append(r'Для системы с гамильтонианом: ')
        doc.append(Math(escape=False, data=['H = ', latex(H), r'\\'], inline=True))
        doc.append(r' проинтегрировать уравнения движения.')

    # Решение задачи
    with doc.create(Solution(task_number)):
        doc.append(Math(escape=False, data=[r'\dot{q_i} = ', r'\cfrac{\partial H}{\partial \dot{p_i}}']))
        doc.append(Math(escape=False, data=[r'\dot{p_i} = ', r'- \cfrac{\partial H}{\partial \dot{q_i}}']))
        doc.append(Math(escape=False, data=[r'\dot{q_1} = ', r'\cfrac{\partial H}{\partial p_1} = ',
                                            '2\,p_1\,F (p_2, \dots, p_n, t)']))


if __name__ == '__main__':
    doc = Document('basic')
    fill_document(doc)
    fill_preambula(doc)
    doc.generate_pdf(task_number, clean_tex=False)
