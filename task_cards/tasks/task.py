"""Describes a generic task"""
import typing
import enum
import task_cards.utils.tex as tex


class TaskCategory(enum.IntEnum):
    """Task categories"""
    AlgebraI = 1,
    Geometry = 2,
    AlgebraII = 3


class Task:
    """Generates the problem and answer, potentially also specifying required
    imports and preamble
    """
    def generate(self, style: tex.TaskStyle = tex.TaskStyle.Minimal) -> str:
        """Generates the task card with the given style

        Arguments:
            style (TaskStyle, optional): the style for the card.
                Default TaskStyle.Minimal
        Returns:
            The task card latex
        """
        raise NotImplementedError

    @property
    def task_categories(self) -> typing.Set[TaskCategory]:
        """Returns the categories that this task belongs too"""
        raise NotImplementedError

    @property
    def imports(self) -> typing.Set[str]:
        """Returns the imports which do not require any arguments that
        are required for this task
        """
        return {'amsmath'}

    @property
    def preambles(self) -> typing.Dict[str, str]:
        """Returns the preambles that are required for this task. Uses a
        unique identifier for each preamble to avoid repeating preambles
        with other tasks that share them.
        """
        return dict()
