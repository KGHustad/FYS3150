import numpy as np
from common import *

def error_solver(n_values, latex_table=None):
    print("Maximal logaritmic relative error")
    if latex_table:
        f = open(latex_table, 'w')
    print("%8s  %8s" % ('N', 'err'))
    f.write("%8s & %8s \\\\ \\hline\n" % ('$N$', '$\\epsilon$'))
    for n in n_values:
        x, v = solve_specific(f_func, n)
        u = u_func(x)
        eps_i = np.log10(abs((v[1:-1]-u[1:-1])/u[1:-1])) #The first and last arguments are the boundery conditions in 0 and n+1, which are outside the matrix, and we don't want them.
        eps = np.max(eps_i)
        print("%8.1e  %8.2f" % (n, eps))
        f.write("%8.1e & %8.2f \\\\ \n" % (n, eps))

    f.close()

if __name__ == '__main__':
    n_values = [10**pow for pow in range(1, 7)]
    error_solver(n_values, latex_table='table_errors.dat')
