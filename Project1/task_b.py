# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from common import *

def solve_general(f_func, n, a, b, c):
    x = np.linspace(0, 1, n+2)
    h = x[1] - x[0]
    s = f_func(x)*h**2
    v = np.zeros(n+2)

    # Forward Substitution
    for i in range(2, n+1):
        row_factor = c[i]/a[i-1]      # 1 FLOP
        a[i] -= b[i-1]*row_factor     # 2 FLOPS
        s[i] -= s[i-1]*row_factor     # 2 FLOPS

    #Backward Substitution
    v[n] = s[n]/a[n]

    for i in range(n-1,0,-1):
        v[i] = (s[i] - b[i]*v[i+1]) / a[i]  # 3 FLOPS

    return x, v

def plot_func(f_func, n, a, b, c, legend=None):
    x, v = solve_general(f_func, n, a, b, c)
    plt.plot(x, v)

if __name__ == '__main__':
    # find and plot numerical approximations
    n_values = [10, 100, 1000]
    for n in n_values:
        a = np.full(n+2, 2, dtype=np.float64)
        b = np.full(n+2, -1, dtype=np.float64)
        c = np.full(n+2, -1, dtype=np.float64)
        plot_func(f_func, n, a, b, c)
    legend = ["N = %d" % n for n in n_values]

    # plot analytical solution
    x = np.linspace(0, 1, 1000)
    plt.plot(x, u_func(x))
    legend.append('Analytical sol.')

    plt.legend(legend)
    plt.savefig('fig/plot_b.png')
    plt.savefig('fig/plot_b.pdf')
    plt.show()
