import numpy as np
import matplotlib.pyplot as plt
import sys
from common import *

if __name__ == '__main__':
    def solve(n):
        return solve_LU(f_func, n)

    n_values = [10, 100, 1000]
    plot_solutions(n_values, solve)

    plt.savefig(get_fig_dir()+'/plot_e.pdf')

    if not '--dont_show' in sys.argv:
        plt.show()

    plt.clf()

    plot_errors(n_values, solve)
    plt.savefig(get_fig_dir()+'/plot_e_error.pdf')
    if not "--dont_show" in sys.argv:
        plt.show()
