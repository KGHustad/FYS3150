import scipy.linalg as sci
import numpy as np
from common import u_func, f_func
import matplotlib.pyplot as plt

n = 10

def make_matrix(n):
    matrix = np.zeros(shape=(n,n))
    matrix[0,0] = 2
    matrix[0,1] = -1
    matrix[-1,-1] = 2
    matrix[-1,-2] = -1
    for i in range(1,n-1):
        array = np.zeros(n)
        array[i-1] = -1
        array[i] = 2
        array[i+1] = -1
        matrix[i] = array
    return matrix

def LU_solve(n):
    matrix = make_matrix(n)
    p,l,u = sci.lu(matrix)
    x = np.linspace(0, 1, n+2)
    h = x[1]-x[0]
    f = f_func(x)[1:-1]*h**2
    y = np.linalg.solve(l,f)
    v_inner = np.linalg.solve(u,y)
    v = np.zeros(n+2)
    v[1:-1] = v_inner[:]
    return x, v

if __name__ == '__main__':
    x = np.linspace(0,1,1002)
    plt.plot(x,u_func(x))
    x, y = LU_solve(10)
    plt.plot(x,y)
    x,y = LU_solve(100)
    plt.plot(x,y)
    x,y = LU_solve(10000)
    plt.plot(x,y)
    plt.show()
