# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import sys

from common import *

def solve_general(f_func, n, a, b, c):
    x = np.linspace(0, 1, n+2)
    h = x[1] - x[0]
    s = f_func(x)*h**2
    v = np.zeros(n+2)

    # Forward Substitution
    for i in range(2, n+1):
        row_factor = a[i]/b[i-1]      # 1 FLOP
        b[i] -= c[i-1]*row_factor     # 2 FLOPS
        s[i] -= s[i-1]*row_factor     # 2 FLOPS

    #Backward Substitution
    v[n] = s[n]/b[n]

    for i in range(n-1,0,-1):
        v[i] = (s[i] - c[i]*v[i+1]) / b[i]  # 3 FLOPS

    return x, v


if __name__ == '__main__':
    # find and plot numerical approximations
    n_values = [10, 100, 1000]
    for n in n_values:
        a = np.full(n+2, -1, dtype=np.float64)
        b = np.full(n+2,  2, dtype=np.float64)
        c = np.full(n+2, -1, dtype=np.float64)
        x, v = solve_general(f_func, n, a, b, c)
        plt.plot(x, v)
    legend = ["N = %d" % n for n in n_values]

    # plot analytical solution
    x = np.linspace(0, 1, 1000)
    plt.plot(x, u_func(x))
    legend.append('Analytical sol.')

    # make plot look great
    plt.legend(legend)
    plt.xlabel('x')
    plt.ylabel('u')

    plt.savefig('fig/plot_b.pdf')
    if not "--dont_show" in sys.argv:
        plt.show()
