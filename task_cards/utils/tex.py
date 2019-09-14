"""Contains helpful utility modules for latex.
"""
import typing
import io
import enum
import subprocess
import os


class TaskStyle(enum.IntEnum):
    """Describes the style for the latex"""
    Minimal = 1


def generate_doc_latex(
        fp: io.TextIOBase,
        required_imports: typing.Set[str],
        required_preamble: typing.Dict[str, str],
        pages: typing.List[str]
        ):
    """
    Creates the latex document that imports the specified documents, has the
    specified preambles (which have a unique key instead of necessarily a
    unique value), and the given ordered set of pages (which should act
    equivalent to having ended with newpage)

    Arguments:
        fp (io.TextIOBase): where to write the latex code
        required_imports (set[str]): the required imports, ex: 'amsmath'. This
            is only for imports which do not require arguments
        required_preamble (dict[str, str]): the keys are arbitrary identifiers,
            and the values are the latex code that will be included prior to
            beginning the document
        pages (list[str]): the latex code for each page
    """
    def my_print(*args, **kwargs):
        print(*args, **kwargs, file=fp)

    my_print('\\documentclass[landscape]{article}')
    my_print('\\usepackage{' + ','.join(required_imports) + '}')
    my_print()
    for iden, code in required_preamble.items():
        my_print(f'% Begin preamble: {iden}')
        my_print(code)
        my_print()

    my_print('\\begin{document}')
    for pg_num, pg in enumerate(pages):
        my_print(f'% Begin page {pg_num}')
        my_print(pg)
        my_print()
    my_print('\\end{document}')


def generate_task_minimal(fp: io.TextIOBase, problem_code: str, answer: str,
                          vspace: str = '2cm'):
    """Generates the code for a single task as a minipage given the code
    that displays the problem and the text answer to the problem. The answer
    is embedded in a QR code and should be fairly short.

    Arguments:
        fp (io.TextIOBase): where to write the task string
        problem_code (str): the latex code that displays the task
        answer (str): the answer to the problem
    """

    print(problem_code, file=fp, end='\n')
    print(color('.', 'white') + f'\\\\[{vspace}]', file=fp)
    print(f'\\begin{{center}}\\qrcode{{{answer}}}\\end{{center}}', file=fp)


def generate_task(fp: io.TextIOBase, problem_code: str, answer: str,
                  vspace: str = '2cm',
                  style: TaskStyle = TaskStyle.Minimal):
    """Generates a single task latex code according to the given style

    Arguments:
        fp (io.TextIOBase): where to write the task string
        problem_code (str): the latex code that displays the task
        answer (str): the answer to the problem
    """
    if style == TaskStyle.Minimal:
        generate_task_minimal(fp, problem_code, answer, vspace)
    else:
        raise NotImplementedError


def generate_task_page_minimal(
        fp: io.TextIOBase,
        tasks: typing.Iterable[str]
        ):
    """Generates one page for the task card, consisting of exactly 4 tasks.
    Minipages are less than 0.5 to make images fit without wrapping to new
    page.

    Arguments:
        fp (io.TextIOBase): where to write the problem string
        tasks (iterable[str]): the first string is the problem code and
            the second string is the answer
    """
    for i, task_code in enumerate(tasks):
        if i >= 4:
            raise ValueError(f'too many tasks for page!')
        print('\\begin{minipage}[t][0.48\\textheight]{0.5\\textwidth}',
              file=fp)
        print(task_code, file=fp)
        print('\\end{minipage}', file=fp)
        if (i % 2) == 0:
            pass
            # print('$\\hspace{0.05\\textwidth}$', file=fp)
        elif i == 1:
            print('\\\\[0\\textheight]', file=fp)
    print('\\newpage', file=fp)


def generate_task_page(
        fp: io.TextIOBase,
        tasks: typing.Iterable[str],
        style: TaskStyle = TaskStyle.Minimal
        ):
    """Generates the given task page according to the style.

    Arguments:
        fp (io.TextIOBase): where to write the problem string
        tasks (iterable[str]): the first string is the problem code and
            the second string is the answer
        style (TaskStyle): determine sthe style for the page
    """
    if style == TaskStyle.Minimal:
        generate_task_page_minimal(fp, tasks)
    else:
        raise NotImplementedError


def prompt_and_equation_minimal(prompt: str, equation: str,
                                vspace: str = '2em') -> str:
    """Generates the latex code for a problem of the sort

    ```
        Prompt

        equation
    ```

    Arguments:
        prompt (str): the prompt latex code
        equation (str): the equation latex code
    """
    return f'{prompt}\\\\[{vspace}]\n\n{equation}'


def scale_eqn(eqn: str, factor: str) -> str:
    """Wraps the given equation in center and scalebox"""
    return ('\\begin{center}\\scalebox{' + factor
            + '}{' + eqn + '}\\end{center}')


def prompt_and_equation(
        prompt: str,
        equation: str,
        style: TaskStyle = TaskStyle.Minimal,
        vspace: str = '2em'
        ) -> str:
    """
    Generates a prompt and equation with the given style

    Arguments:
        prompt (str): the prompt latex, which should NOT include formatting
            for size or padding. ex: 'Solve for $x$'
        equation (str): the equation latex, which should include equation
            delimiters and sizing/centering
                ex: '$$x^2 = 9$$
                ex: '\\begin{align}
                       % .. omitted ..
                     \\end{align}'
        style (TaskStyle): the style to mark with
    """
    if style == TaskStyle.Minimal:
        return prompt_and_equation_minimal(prompt, equation, vspace)
    raise NotImplementedError


def color(content: str, color: str):
    """Colors the specified content the given color in latex"""
    return f'\\textcolor{{{color}}}{{{content}}}'


def figure(fig: str, wid: str, hei: str):
    """Returns the latex code to insert the specified figure. The
    figure must be in the same directory as the tex file"""
    fig_wo_ext = os.path.splitext(os.path.basename(fig))[0]

    return (f'\\includegraphics[width={wid},height={hei},'
            + f'keepaspectratio]{{{fig_wo_ext}}}')


def figure_left_of_text(fig: str, text: str):
    return '\n'.join([
        '\\begin{minipage}{0.3\\textwidth}',
        figure(fig, '200px', '200px'),
        '\\end{minipage}',
        '\\hfill',
        '\\begin{minipage}{0.5\\textwidth}',
        text,
        '\\end{minipage}'
    ])


def enumer(items: typing.Iterable[str]):
    """Itemizes the sequence of items"""
    result = ['\\begin{enumerate}[label=(\\alph*)]']
    for it in items:
        result.append('\\item ' + it)
    result.append('\\end{enumerate}')
    return '\n'.join(result)


def pdflatex(latexfile: str, outdir: str):
    """Converts the given latex file to pdf"""
    subprocess.run([
        'pdflatex', latexfile, '-output-directory', outdir
    ])
