"""Generates a specified number of pages from a given list of tasks
by selecting from them uniformly at random for each card.
"""
import argparse
import task_cards.utils.tex as tex
import task_cards.tasks.all as tasks_all
import task_cards.utils.borders as borders
import random
import io
import shutil
import os
import time


def main():
    parser = argparse.ArgumentParser(
        description='Generates task cards from the list')
    parser.add_argument('--pages', type=int, default=1,
                        help='the number of pages that you want to generate')
    parser.add_argument('--tasks', type=str, nargs='+',
                        default=['PerfectSquaresTask'],
                        help='The tasks that you want to include')
    args = parser.parse_args()
    run_(args)


def run_(args):
    if os.path.exists('out'):
        shutil.rmtree('out')
        time.sleep(1)
    os.makedirs('out')

    tasks_ = []
    for task_id in args.tasks:
        if task_id in tasks_all.TASKS_BY_MODULE_AND_NAME:
            tasks_.append(tasks_all.TASKS_BY_MODULE_AND_NAME[task_id])
        else:
            tasks_.append(tasks_all.TASKS_BY_NAME[task_id])

    pages = []
    imports = {'qrcode', 'graphicx'}
    preambles = {
        'margin': '\\usepackage[margin=0in]{geometry}',
        'parindent': '\\setlength\\parindent{0pt}'
    }
    for _ in range(args.pages):
        page_task_codes = []
        for _ in range(4):
            tsk = random.choice(tasks_)()
            page_task_codes.append(tsk.generate())
            imports = imports.union(tsk.imports)
            preambles.update(tsk.preambles)
        writer = io.StringIO()
        tex.generate_task_page(writer, page_task_codes)
        pages.append(writer.getvalue())

    with open('out/out.tex', 'w') as outfile:
        tex.generate_doc_latex(outfile, imports, preambles, pages)
    tex.pdflatex('out/out.tex', 'out')
    borders.add_borders('out/out.pdf', 'out/bordered.pdf', args.pages)


if __name__ == '__main__':
    main()
