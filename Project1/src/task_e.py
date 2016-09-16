import numpy as np
import matplotlib.pyplot as plt
import sys
from common import *

if __name__ == '__main__':
    n_values = [10, 100, 1000, 4000]
    plot_solutions(n_values, solve_LU)

    plt.savefig('fig/plot_e.pdf')

    if not '--dont_show' in sys.argv:
        plt.show()
