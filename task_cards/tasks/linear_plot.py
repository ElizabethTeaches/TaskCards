"""Plot the following function where x varies from -3 to 3:

y = 2x + 1
"""
import task_cards.utils.tex as tex
import task_cards.tasks.task as task
import task_cards.utils.mpl as mpl
from task_cards.utils.upload import upload
import random
import io
import numpy as np


MIN_M = -2
MAX_M = 2
MIN_B = -2
MAX_B = 2

class LinearPlotTask(task.Task):
    def generate(self, style=tex.TaskStyle.Minimal):
        m = random.randint(MIN_M, MAX_M)
        b = random.randint(MIN_B, MAX_B)

        xs = (-3, 3)
        ys = (-3 * m + b, 3 * m + b)

        img_bytes = io.BytesIO()
        mpl.create_graph(
            xs, ys, 5, 5, -5, img_bytes,
            format='png'
        )
        answer = upload(img_bytes)

        if b > 0:
            signed_b = '+' + str(b)
        elif b < 0:
            signed_b = str(b)
        else:
            signed_b = ''

        if m == 1:
            str_m = ''
        elif m == -1:
            str_m = '-'
        else:
            str_m = str(m)

        problem_code = tex.prompt_and_equation(
            tex.scale_eqn('Plot the function on $-3 < x < 3$', '1.25') + tex.color('.', 'white'),
            tex.scale_eqn(f'$y = {str_m}x {signed_b}$', '2'),
            style
        )

        writer = io.StringIO()
        print(tex.color('.', 'white'), file=writer)
        print('\\\\', file=writer)  # fix issue created making images work
        tex.generate_task(writer, problem_code, answer, '2cm', style)
        return writer.getvalue()

    @property
    def task_categories(self):
        return {task.TaskCategory.AlgebraI}
