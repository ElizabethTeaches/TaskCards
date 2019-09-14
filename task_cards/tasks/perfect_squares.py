"""Find the square root of perfect squares
"""
import task_cards.utils.tex as tex
import task_cards.tasks.task as task
import random
import io

MIN_SQRT = 2
MAX_SQRT = 20


class PerfectSquaresTask(task.Task):
    def generate(self, style=tex.TaskStyle.Minimal):
        sqrt = random.randint(MIN_SQRT, MAX_SQRT)
        square = sqrt * sqrt

        problem_code = tex.prompt_and_equation(
            tex.scale_eqn('Solve for $x$', '2') + tex.color('.', 'white'),
            tex.scale_eqn(f'$x^2 = {square}$', '3'),
            style
        )
        answer = f'{sqrt} or -{sqrt}'

        writer = io.StringIO()
        print(tex.color('.', 'white'), file=writer)
        print('\\\\', file=writer)  # fix issue created making images work
        tex.generate_task(writer, problem_code, answer, '2cm', style)
        return writer.getvalue()

    @property
    def task_categories(self):
        return {task.TaskCategory.AlgebraI, task.TaskCategory.AlgebraII}
