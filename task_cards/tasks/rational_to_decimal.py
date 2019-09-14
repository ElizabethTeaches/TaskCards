"""Find the decimal form for the rational number. State
whether it repeats or terminates.
"""
import task_cards.utils.tex as tex
import task_cards.tasks.task as task
import random
import io
import numpy as np
from fractions import Fraction

MIN_NUM = 1
MAX_NUM = 150

NOISE_PRIMES = [3, 7, 9, 11, 13, 17, 19]

class RationalToDecimalTask(task.Task):
    def generate(self, style=tex.TaskStyle.Minimal):
        should_terminate = random.random() < .5
        is_positive = random.random() < .5

        if should_terminate:
            denom = 0
            while denom < MIN_NUM or denom > MAX_NUM:
                de_pows_2 = random.randint(0, 5)
                de_pows_5 = random.randint(0, 2)

                denom = 1
                denom *= 2 ** de_pows_2
                denom *= 5 ** de_pows_5

            num = random.randint(MIN_NUM, MAX_NUM)
        else:
            denom = 0

            while denom < MIN_NUM or denom > MAX_NUM:
                denom = 1
                non_noise = int(np.random.choice(
                    [0, 1, 2], size=(1,), replace=True,
                    p=[0.5, 0.35, 0.15]
                ))

                if non_noise > 0:
                    non_noise_ps = np.random.choice(
                        [2, 5], size=(non_noise,), replace=True)
                    for p in non_noise_ps:
                        denom *= int(p)

                num_noise_ps = random.randint(1, 3)
                noise_ps = np.random.choice(NOISE_PRIMES, size=(num_noise_ps,))
                for p in noise_ps:
                    denom *= int(p)

            num = random.randint(MIN_NUM, MAX_NUM)

        eqn = '-' if not is_positive else ''
        eqn += '\\frac{%s}{%s}' % (num, denom)
        problem_code = tex.prompt_and_equation(
            '\\begin{center}\nFind the decimal form for the rational \\\\\n'
            + 'number. State whether it repeats or terminates.\n\\end{center}'
            + tex.color('.', 'white'),
            tex.scale_eqn(f'${eqn}$', '2'),
            style
        )
        answer = f'{num/denom}, ' + ('terminates' if should_terminate else 'repeats')

        writer = io.StringIO()
        print(tex.color('.', 'white'), file=writer)
        print('\\\\', file=writer)  # fix issue created making images work
        tex.generate_task(writer, problem_code, answer, '2cm', style)
        return writer.getvalue()

    @property
    def task_categories(self):
        return {task.TaskCategory.AlgebraI}
