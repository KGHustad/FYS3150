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
    p,l,u = sci.lu(make_matrix(n))
    x = np.linspace(0, 1, n)
    h = x[1]-x[0]
    f = f_func(x)*h**2
    y = np.linalg.solve(l,f)
    return np.linalg.solve(u,y)

print LU_solve(10)
