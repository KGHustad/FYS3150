from common import *


#def solve_1d_forwa

def doctest_solve_2d_serial():
    """
    >>> silent = True
    >>> n = 4
    >>> iterations = 1
    >>> alpha = 0.1

    >>> v = np.fromfunction((lambda x, y: (x+y)%2), (n+2, n+2))
    >>> v
    array([[ 0.,  1.,  0.,  1.,  0.,  1.],
           [ 1.,  0.,  1.,  0.,  1.,  0.],
           [ 0.,  1.,  0.,  1.,  0.,  1.],
           [ 1.,  0.,  1.,  0.,  1.,  0.],
           [ 0.,  1.,  0.,  1.,  0.,  1.],
           [ 1.,  0.,  1.,  0.,  1.,  0.]])
    >>> t = diffusion_2d(v, iterations, alpha, bc_left=0, bc_right=0, bc_top=0, bc_bottom=0, omp=False, silent=silent)
    >>> v
    array([[ 0. ,  1. ,  0. ,  1. ,  0. ,  1. ],
           [ 1. ,  0.4,  0.6,  0.4,  0.6,  0. ],
           [ 0. ,  0.6,  0.4,  0.6,  0.4,  1. ],
           [ 1. ,  0.4,  0.6,  0.4,  0.6,  0. ],
           [ 0. ,  0.6,  0.4,  0.6,  0.4,  1. ],
           [ 1. ,  0. ,  1. ,  0. ,  1. ,  0. ]])
    """
    pass

def doctest_solve_2d_omp():
    """
    >>> silent = True
    >>> n = 4
    >>> iterations = 1
    >>> alpha = 0.1

    >>> v = np.fromfunction((lambda x, y: (x+y)%2), (n+2, n+2))
    >>> v
    array([[ 0.,  1.,  0.,  1.,  0.,  1.],
           [ 1.,  0.,  1.,  0.,  1.,  0.],
           [ 0.,  1.,  0.,  1.,  0.,  1.],
           [ 1.,  0.,  1.,  0.,  1.,  0.],
           [ 0.,  1.,  0.,  1.,  0.,  1.],
           [ 1.,  0.,  1.,  0.,  1.,  0.]])
    >>> t = diffusion_2d(v, iterations, alpha, bc_left=0, bc_right=0, bc_top=0, bc_bottom=0, omp=True, silent=silent)
    >>> v
    array([[ 0. ,  1. ,  0. ,  1. ,  0. ,  1. ],
           [ 1. ,  0.4,  0.6,  0.4,  0.6,  0. ],
           [ 0. ,  0.6,  0.4,  0.6,  0.4,  1. ],
           [ 1. ,  0.4,  0.6,  0.4,  0.6,  0. ],
           [ 0. ,  0.6,  0.4,  0.6,  0.4,  1. ],
           [ 1. ,  0. ,  1. ,  0. ,  1. ,  0. ]])
    """
    pass
