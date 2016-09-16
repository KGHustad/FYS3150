# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import sys

from common import *

if __name__ == '__main__':
    n_values = [10,100,1000]
    def solve(n):
        a = np.full(n+2, 2, dtype=np.float64)
        b = np.full(n+2, -1, dtype=np.float64)
        c = np.full(n+2, -1, dtype=np.float64)
        x, v = solve_specific(f_func, n)
        return x, v

    n_values = [10, 100, 1000]
    plot_magic(n_values, solve)

    plt.savefig('fig/plot_c.pdf')

    if not '--dont_show' in sys.argv:
        plt.show()
