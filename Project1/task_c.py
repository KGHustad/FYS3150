# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from common import *
from task_b import solve_general

def solve_specific(f_func, n):
    x = np.linspace(0, 1, n+2)
    h = x[1] - x[0]
    f = f_func(x)*h**2
    v = np.zeros(n+2)
    a_func = lambda i: (i+1)/i
    a = a_func(np.arange(0,n+1, dtype=np.float64))
    a[0] = 0 #fysiker loesning
    for i in range(2,n+1):
        f[i] = f[i] + f[i-1]/a[i-1] # 2 FLOP

    v[n] = f[n]/float(a[n])

    for i in range(n-1,0,-1):
        v[i] = (f[i]+v[i+1])/a[i]   # 2 FLOP

    return x, v

def plot_func(f_func, n):
    x, v = solve_specific(f_func, n)
    plt.plot(x, v, x, u_func(x))

"""
for n in ([10,100,1000]):
    a = np.full(n+2, 2, dtype=np.float64)
    b = np.full(n+2, -1, dtype=np.float64)
    c = np.full(n+2, -1, dtype=np.float64)
    plot_func(f_func, n)
plt.show()
"""


def CPU_time(n):
    import time
    from task_b import solve_general

    a = np.full(n+2, 2, dtype=np.float64)
    b = np.full(n+2, -1, dtype=np.float64)
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


error_solver([10,10**2,10**3,10**4,10**5,10**6])
