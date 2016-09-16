import numpy as np
from common import *

def error_solver(n_values):
    for n in n_values:
        v, x = solve_specific(f_func, n)
        u = u_func(x)
        eps_i = np.log10(abs(np.divide((v[1:-1]-u[1:-1]),u[1:-1]))) #The first and last arguments are the boundery conditions in 0 and n+1, which are outside the matrix, and we don't want them.
        eps = np.max(eps_i)
        print "Logaritmic relative error for n = %e: %f" % (n, eps)


if __name__ == '__main__':
    error_solver([10**pow for pow in range(1, 7)])
