from common import *
np.set_printoptions(linewidth=100)
try:
    np.set_printoptions(legacy="1.13")
except:
    pass

def doctest_solve_1d_forward_euler():
    """
    >>> silent = True
    >>> n = 4
    >>> iterations = 1
    >>> alpha = 0.1

    Every other 0 and 1
    -------------------
    >>> v = np.fromfunction(lambda x: x%2, (n+2,))
    >>> v
    array([ 0.,  1.,  0.,  1.,  0.,  1.])
    >>> t = diffusion_1d(v, iterations, alpha, 'forward_euler', silent=silent)
    >>> v
    array([ 0. ,  0.8,  0.2,  0.8,  0.2,  1. ])

    U(1) = 1
    --------
    First a single step
    >>> v = np.zeros(n+2)
    >>> v[-1] = 1
    >>> t = diffusion_1d(v, iterations, alpha, 'forward_euler', silent=silent)
    >>> v
    array([ 0. ,  0. ,  0. ,  0. ,  0.1,  1. ])

    Then a second step
    >>> t = diffusion_1d(v, iterations, alpha, 'forward_euler', silent=silent)
    >>> v
    array([ 0.  ,  0.  ,  0.  ,  0.01,  0.18,  1.  ])

    Check that running two steps in one call gives same result
    >>> iterations = 2
    >>> v = np.zeros(n+2)
    >>> v[-1] = 1
    >>> t = diffusion_1d(v, iterations, alpha, 'forward_euler', silent=silent)
    >>> v
    array([ 0.  ,  0.  ,  0.  ,  0.01,  0.18,  1.  ])
    """
    pass

def doctest_solve_1d_backward_euler():
    """
    >>> solver = 'backward_euler'
    >>> silent = True
    >>> n = 4
    >>> iterations = 1
    >>> alpha = 1

    Every other 0 and 1
    -------------------
    >>> v = np.fromfunction(lambda x: x%2, (n+2,))
    >>> v
    array([ 0.,  1.,  0.,  1.,  0.,  1.])
    >>> t = diffusion_1d(v, iterations, alpha, solver, silent=silent)
    >>> v
    array([ 0.        ,  0.45454545,  0.36363636,  0.63636364,  0.54545455,  1.        ])

    U(1) = 1
    --------
    >>> v = np.zeros(n+2)
    >>> v[-1] = 1
    >>> t = diffusion_1d(v, 1, alpha, solver, silent=silent)
    >>> v
    array([ 0.        ,  0.01818182,  0.05454545,  0.14545455,  0.38181818,  1.        ])
    >>> t = diffusion_1d(v, 99, alpha, solver, silent=silent)
    >>> v
    array([ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ])
    """
    pass

def doctest_solve_1d_crank_nicolson():
    """
    >>> solver = 'crank_nicolson'
    >>> silent = True
    >>> n = 4
    >>> iterations = 1
    >>> alpha = 1

    Every other 0 and 1
    -------------------
    >>> v = np.fromfunction(lambda x: x%2, (n+2,))
    >>> v
    array([ 0.,  1.,  0.,  1.,  0.,  1.])
    >>> t = diffusion_1d(v, iterations, alpha, solver, silent=silent)
    >>> v
    array([ 0.        ,  0.15789474,  0.63157895,  0.36842105,  0.84210526,  1.        ])

    U(1) = 1
    --------
    >>> v = np.zeros(n+2)
    >>> v[-1] = 1
    >>> t = diffusion_1d(v, 1, alpha, solver, silent=silent)
    >>> v
    array([ 0.        ,  0.00956938,  0.03827751,  0.14354067,  0.53588517,  1.        ])
    >>> t = diffusion_1d(v, 99, alpha, solver, silent=silent)
    >>> v
    array([ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ])
    """
    pass

def doctest_solve_2d_serial():
    """
    >>> omp = False
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
    >>> t = diffusion_2d(v, iterations, alpha, bc_left=0, bc_right=0, bc_top=0, bc_bottom=0, omp=omp, silent=silent)
    >>> v
    array([[ 0. ,  1. ,  0. ,  1. ,  0. ,  1. ],
           [ 1. ,  0.4,  0.6,  0.4,  0.6,  0. ],
           [ 0. ,  0.6,  0.4,  0.6,  0.4,  1. ],
           [ 1. ,  0.4,  0.6,  0.4,  0.6,  0. ],
           [ 0. ,  0.6,  0.4,  0.6,  0.4,  1. ],
           [ 1. ,  0. ,  1. ,  0. ,  1. ,  0. ]])

    Isolating all sides, we should get a homogenous array
    >>> t = diffusion_2d(v, 200, alpha, bc_left=1, bc_right=1, bc_top=1, bc_bottom=1, omp=omp, silent=silent)
    >>> v
    array([[ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
           [ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
           [ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
           [ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
           [ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
           [ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5]])


    Top and bottom isolated, i.e. du/dy=0 (Neumann condition)
    and left and right constantly 0 and 1, respectively (Dirichlet
    condition)
    This should be similar to the linear case
    >>> v = np.zeros((n+2, n+2))
    >>> v[:,-1] = 1
    >>> t = diffusion_2d(v, 500, alpha, bc_left=0, bc_right=0, bc_top=1, bc_bottom=1, omp=omp, silent=silent)
    >>> v
    array([[ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ],
           [ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ],
           [ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ],
           [ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ],
           [ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ],
           [ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ]])
    """
    pass

def doctest_solve_2d_omp():
    """
    >>> omp = True
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
    >>> t = diffusion_2d(v, iterations, alpha, bc_left=0, bc_right=0, bc_top=0, bc_bottom=0, omp=omp, silent=silent)
    >>> v
    array([[ 0. ,  1. ,  0. ,  1. ,  0. ,  1. ],
           [ 1. ,  0.4,  0.6,  0.4,  0.6,  0. ],
           [ 0. ,  0.6,  0.4,  0.6,  0.4,  1. ],
           [ 1. ,  0.4,  0.6,  0.4,  0.6,  0. ],
           [ 0. ,  0.6,  0.4,  0.6,  0.4,  1. ],
           [ 1. ,  0. ,  1. ,  0. ,  1. ,  0. ]])

    Isolating all sides, we should get a homogenous array
    >>> t = diffusion_2d(v, 200, alpha, bc_left=1, bc_right=1, bc_top=1, bc_bottom=1, omp=omp, silent=silent)
    >>> v
    array([[ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
           [ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
           [ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
           [ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
           [ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5],
           [ 0.5,  0.5,  0.5,  0.5,  0.5,  0.5]])


    Top and bottom isolated, i.e. du/dy=0 (Neumann condition)
    and left and right constantly 0 and 1, respectively (Dirichlet
    condition)
    This should be similar to the linear case
    >>> v = np.zeros((n+2, n+2))
    >>> v[:,-1] = 1
    >>> t = diffusion_2d(v, 500, alpha, bc_left=0, bc_right=0, bc_top=1, bc_bottom=1, omp=omp, silent=silent)
    >>> v
    array([[ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ],
           [ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ],
           [ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ],
           [ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ],
           [ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ],
           [ 0. ,  0.2,  0.4,  0.6,  0.8,  1. ]])

    """
    pass
