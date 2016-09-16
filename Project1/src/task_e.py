import scipy.linalg as sci
import numpy as np
import matplotlib.pyplot as plt
import sys
from common import *

n = 10

def make_matrix(n):
    matrix = np.zeros(shape=(n,n))
    matrix[0,0] = 2
    matrix[0,1] = -1
    matrix[-1,-1] = 2
    matrix[-1,-2] = -1
    for i in xrange(1,n-1):
        matrix[i,i-1] = -1
        matrix[i,i] = 2
        matrix[i,i+1] = -1
    return matrix

def LU_solve(n):
    matrix = make_matrix(n)
    p,l,u = sci.lu(matrix, overwrite_a=True)
    x = np.linspace(0, 1, n+2)
    h = x[1]-x[0]
    f = f_func(x)[1:-1]*h**2
    y = np.linalg.solve(l,f)
    v_inner = np.linalg.solve(u,y)
    v = np.zeros(n+2)
    v[1:-1] = v_inner[:]
    return x, v

if __name__ == '__main__':
    n_values = [10, 100, 1000, 4000]
    plot_solutions(n_values, LU_solve)

    plt.savefig('fig/plot_e.pdf')

    if not '--dont_show' in sys.argv:
        plt.show()
