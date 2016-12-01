import matplotlib.pyplot as plt
from common import ensure_fig_dir

def show_2d(v):
    plt.imshow(v, cmap=plt.cm.gray, vmin=0, vmax=1, interpolation='none')
    plt.show()

ensure_fig_dir()
