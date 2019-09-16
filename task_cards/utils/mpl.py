"""Utility functions related to matplotlib"""
import matplotlib.pyplot as plt


def create_graph(x, y, width, height, ymin, filename,
                 **savefig_kwargs):
    """Creates and saves a plot with the given x and y coordinates
    and saves it to the given file. If the file is a file-like
    object instead of a string, it saves it there.

    Arguments:
        x (np.ndarray[samples]): the x-coordinates
        y (np.ndarray[samples]): the y-coordinates
        width (float): the left and right edges of the plot
        height (float): the maximum y of the plot
        ymin (float): the minimum y of the plot
        filename (file or str): where to save the plot to
    """
    fig, axes = plt.subplots(figsize=(15, 15))

    axes.plot(x, y, 'b', linewidth=8)
    # axes.text(0.15, height - 0.5, 'y')
    # axes.text(-width + 0.2, 1, 'x')
    axes.axis([-width, width, ymin, height])
    axes.tick_params(
        which='both',
        width=4,
        length=8
    )
    axes.set_xticks([i for i in range(-width + 1, width) if i != 0])
    axes.set_yticks([i for i in range(ymin + 1, height) if i != 0])
    axes.spines['bottom'].set_position('zero')
    axes.spines['left'].set_position('zero')
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    for item in (
            [axes.title, axes.xaxis.label, axes.yaxis.label] +
            axes.get_xticklabels() + axes.get_yticklabels()):
        item.set_fontsize(32)
    for spine in axes.spines.values():
        spine.set_linewidth(6)
    if 'dpi' not in savefig_kwargs:
        savefig_kwargs['dpi'] = 300
    plt.savefig(filename, **savefig_kwargs)
