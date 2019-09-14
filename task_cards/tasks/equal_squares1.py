""" Solve for the solution of a squared binomial
    equal to a perfect square.
"""
import task_cards.utils.tex as tex
import task_cards.tasks.task as task
import random
import io

MIN_SQRT = 2
MAX_SQRT = 12


class SolveQuadByEqualSquares1Task(task.Task):
    def generate(self, style=tex.TaskStyle.Minimal):
        sqrt = random.randint(MIN_SQRT, MAX_SQRT)
        square = sqrt * sqrt
        plus_what = random.randint(-10, 10)
        if plus_what < 0:
            sign = '-'
            number = abs(plus_what)
        else:
            sign = '+'
            number = plus_what

        problem_code = tex.prompt_and_equation(
            tex.scale_eqn('Solve for $x$', '2') + tex.color('.', 'white'),
            tex.scale_eqn(f'$(x {sign} {number})^2 = {square}$', '3'),
            style
        )
        sol1 = sqrt - plus_what
        sol2 = - sqrt - plus_what
        answer = f'{sol1} or {sol2}'

        writer = io.StringIO()
        print(tex.color('.', 'white'), file=writer)
        print('\\\\', file=writer)  # fix issue created making images work
        tex.generate_task(writer, problem_code, answer, '2cm', style)
        return writer.getvalue()

    @property
    def task_categories(self):
        return {task.TaskCategory.AlgebraI, task.TaskCategory.AlgebraII}
