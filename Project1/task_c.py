# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import sys

from common import *
from task_b import solve_general

def solve_specific(f_func, n):
    x = np.linspace(0, 1, n+2)
    h = x[1] - x[0]
    s = f_func(x)*h**2
    v = np.zeros(n+2)
    b_func = lambda i: (i+1)/i
    b = np.zeros(n+2, dtype=np.float64)
    i = np.arange(0, n+2, dtype=np.float64)
    b[1:-1] = b_func(i[1:-1])
    for i in range(2,n+1):
        s[i] = s[i] + s[i-1]/b[i-1] # 2 FLOPS

    v[n] = s[n]/b[n]

    for i in range(n-1,0,-1):
        v[i] = (s[i]+v[i+1])/b[i]   # 2 FLOPS

    return x, v


def CPU_time(n):
    import time
    from task_b import solve_general

    a = np.full(n+2, -1, dtype=np.float64)
    b = np.full(n+2, 2, dtype=np.float64)
    c = np.full(n+2, -1, dtype=np.float64)

    start_time = time.time()
    v,x = solve_general(f_func, n, a, b, c)
    print "General function run-time: %f seconds" % (time.time() - start_time)

    start_time = time.time()
    v,x = solve_specific(f_func, n)
    print "Specific function run-time: %f seconds" % (time.time() - start_time)

#CPU_time(10**6)

def error_solver(i):
    for n in (i):
        v, x = solve_specific(f_func, n)
        u = u_func(x)
        eps_i = np.log10(abs(np.divide((v[1:-1]-u[1:-1]),u[1:-1]))) #The first and last arguments are the boundery conditions in 0 and n+1, which are outside the matrix, and we don't want them.
        eps = np.max(eps_i)
        print "Logaritmic relative error for n = %e: %f" % (n, eps)


if __name__ == '__main__':
    n_values = [10,100,1000]
    for n in n_values:
        a = np.full(n+2, 2, dtype=np.float64)
        b = np.full(n+2, -1, dtype=np.float64)
        c = np.full(n+2, -1, dtype=np.float64)
        x, v = solve_specific(f_func, n)
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

    plt.savefig('fig/plot_c.pdf')

    if not '--dont_show' in sys.argv:
        plt.show()

    error_solver([10,10**2,10**3,10**4,10**5,10**6])
