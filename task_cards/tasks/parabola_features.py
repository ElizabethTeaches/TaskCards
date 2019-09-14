"""Identify features of parabolas from graphs"""
import task_cards.tasks.task as task
import task_cards.utils.tex as tex
import random
import numpy as np
import utils.mpl as umpl
import uuid
import os
import io
import enum


class Feature(enum.Enum):
    Yint = 1
    Xint = 2
    Vertex = 3
    Symmetry = 4
    Apos = 5


FEATURE_TO_QN = {
    Feature.Yint: 'What is the y-intercept?',
    Feature.Xint: 'What are the zeros?',
    Feature.Vertex: 'What is the vertex?',
    Feature.Symmetry: 'What is the axis of symmetry?',
    Feature.Apos: 'Is the leading coefficient positive or negative?'
}


class ParabolaFeaturesTask(task.Task):
    def generate(self, style=tex.TaskStyle.Minimal):
        a_pos = random.random() < 0.5
        a_bigger_one = random.random() < 0.5
        which_feature = random.choice(list(Feature))

        a = random.randint(1, 3)
        if not a_pos:
            a *= -1

        if not a_bigger_one:
            a = 1 / a

        xs = np.linspace(-5, 5, 100)
        if (which_feature == Feature.Vertex
                or which_feature == Feature.Symmetry
                or which_feature == Feature.Apos):
            h = random.randint(-4, 4)
            k = random.randint(0, 4)
            if not a_pos:
                k = -k
            ys = a * ((xs - h) ** 2) + k
            if which_feature == Feature.Vertex:
                answer = f'The vertex is at ({h}, {k}).'
            elif which_feature == Feature.Symmetry:
                answer = f'The axis of symmetry is x = {h}.'
            else:  # which_feature == Apos
                if a_pos:
                    answer = 'The leading coefficient is positive.'
                else:
                    answer = 'The leading coefficient is negative.'

        elif which_feature == Feature.Xint:
            xint1 = random.randint(-4, 4)
            xint2 = random.randint(-4, 4)
            ys = a * (xs + xint1) * (xs + xint2)
            answer = f'The zeros are {xint1} and {xint2}.'

        else:  # which_feature == Yint
            c = random.randint(0, 5)
            b = random.randint(-5, 5)
            if not a_pos:
                c = -c
            ys = (a * xs**2) + (b * xs) + c
            answer = f'The y-intercept is {c}.'

        tmp_file = os.path.join('out', str(uuid.uuid4()) + '.png')
        umpl.create_graph(xs, ys, 6, 6, -6, tmp_file)

        problem_code = tex.prompt_and_equation(
            '\\Large{\\vspace{0.8em}Look at this graph of a '
            + 'quadratic function and answer the question. }',

            tex.figure_left_of_text(
                tmp_file,
                FEATURE_TO_QN[which_feature]
            ),
            style,
            '0.2cm'   # adjusts space between main prompt and image
        )

        writer = io.StringIO()
        tex.generate_task(writer, problem_code, answer, '-1.5cm', style)
        return writer.getvalue()

    @property
    def task_categories(self):
        return {task.TaskCategory.AlgebraI, task.TaskCategory.AlgebraII}

    @property
    def imports(self):
        return {'amsmath', 'wrapfig', 'enumitem'}
