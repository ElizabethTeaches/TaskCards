"""Returns a list of all the tasks. Assumes all python files in
task or subfolders of task include a Task file. Not the worlds
fastest solution, but seamless"""

import task_cards.tasks.task as task
import os
import typing
import importlib


def _find_tasks(prefix: str, folder: str) -> typing.Set[task.Task]:
    """Recursively search the tasks folder for tasks"""
    res = set()
    with os.scandir(folder) as it:
        for entry in it:
            entry: os.DirEntry
            if entry.is_file() and entry.name.endswith('.py'):
                if entry.name == 'all.py' or entry.name == 'task.py':
                    continue

                fname_wo_ext = os.path.splitext(entry.name)[0]
                try:
                    module = importlib.import_module(prefix + fname_wo_ext)

                    for nm, attr in module.__dict__.items():
                        if (isinstance(attr, type)
                                and issubclass(attr, task.Task)):
                            res.add(attr)
                except Exception as exc:
                    raise ImportError(
                        f'{prefix} in {folder} -> {entry.name}') from exc
            elif entry.is_dir():
                res = res.union(_find_tasks(f'{prefix}.{entry.name}',
                                            entry.path))

    return res


ALL_TASKS = _find_tasks('tasks.', 'tasks')

TASKS_BY_MODULE_AND_NAME = dict()
TASKS_BY_NAME = dict()  # duplicates chosen arbitrarily

for task_ in ALL_TASKS:
    module = task_.__module__
    name = task_.__name__
    TASKS_BY_MODULE_AND_NAME[f'{module}.{name}'] = task_
    TASKS_BY_NAME[name] = task_
