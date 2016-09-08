import numpy as np

def u_func(x):
    """The analytical solution"""
    return 1-(1-np.exp(-10))*x-np.exp(-10*x)

def f_func(x):
    """The source term"""
    return 100*np.exp(-10*x)
