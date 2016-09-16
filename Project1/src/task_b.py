# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import sys

from common import *

if __name__ == '__main__':
    def solve(n):
        a = np.full(n+2, -1, dtype=np.float64)
        b = np.full(n+2,  2, dtype=np.float64)
        c = np.full(n+2, -1, dtype=np.float64)
        x, v = solve_general(f_func, n, a, b, c)
        return x, v

    n_values = [10, 100, 1000, 10000]
    plot_solutions(n_values, solve)

    plt.savefig('fig/plot_b.pdf')
    if not "--dont_show" in sys.argv:
        plt.show()

    plt.clf()

    plot_errors(n_values, solve)
    plt.savefig('fig/plot_b_error.pdf')
    if not "--dont_show" in sys.argv:
        plt.show()
