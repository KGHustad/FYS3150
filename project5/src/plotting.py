import matplotlib.pyplot as plt
from common import ensure_fig_dir

def show_2d(v, title=None, save_to=None, show=True):
    plt.imshow(v, cmap=plt.cm.gray, vmin=0, vmax=1, interpolation='none')
    plt.xlabel('$i$')
    plt.ylabel('$j$')
    if title is not None:
        plt.title(title)
    if save_to is not None:
        plt.savefig(save_to)
    if show:
        plt.show()
    plt.clf()

ensure_fig_dir()
