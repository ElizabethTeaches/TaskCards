"""Classify the exponential graph according to various things"""
import task_cards.tasks.task as task
import task_cards.utils.tex as tex
import random
import numpy as np
import utils.mpl as umpl
import uuid
import os
import io


class ExpoQualitativeTask(task.Task):
    def generate(self, style=tex.TaskStyle.Minimal):
        a_pos = random.random() < 0.5
        b_bigger_one = random.random() < 0.5

        a = random.randint(1, 5)
        if not a_pos:
            a *= -1

        b = random.randint(2, 5)
        if not b_bigger_one:
            b = 1 / b

        is_decay = a_pos and not b_bigger_one
        range_pos_y = a_pos

        is_growth = a_pos and b_bigger_one

        xs = np.linspace(-5, 5, 100)
        ys = a * (b ** xs)

        tmp_file = os.path.join('out', str(uuid.uuid4()) + '.png')
        umpl.create_graph(xs, ys, 6, 6, -6, tmp_file)

        problem_code = tex.prompt_and_equation(
            '\\Large{\\vspace{0.8em}Look at the graph of an '
            + 'exponential function that '
            + 'has the form $f(x)=ab^x$  where $b>0$. Which of the '
            + 'following statements about this function must be true? '
            + 'Select all that apply.}',

            tex.figure_left_of_text(
                tmp_file,
                tex.enumer([
                    '$a$ is positive',
                    '$0 < b < 1$',
                    'the function models growth',
                    'the function models decay',
                    'the range is $y > 0$',
                ])
            ),
            style,
            '-0.4cm'  # adjust space between main prompt and image
        )

        correct = []
        if a_pos:
            correct.append('A')
        if not b_bigger_one:
            correct.append('B')
        if is_growth:
            correct.append('C')
        if is_decay:
            correct.append('D')
        if range_pos_y:
            correct.append('E')

        if not correct:
            correct.append('None')

        answer = ', '.join(correct)

        writer = io.StringIO()
        tex.generate_task(writer, problem_code, answer, '-1.35cm', style)
        return writer.getvalue()

    @property
    def task_categories(self):
        return {task.TaskCategory.AlgebraI, task.TaskCategory.AlgebraII}

    @property
    def imports(self):
        return {'amsmath', 'wrapfig', 'enumitem'}
