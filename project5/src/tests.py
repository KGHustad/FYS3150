from common import *


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
    >>> v_old = v.copy()
    >>> t = diffusion_1d(v, iterations, alpha, solver, silent=silent)
    >>> v
    array([ 0.        ,  0.45454545,  0.36363636,  0.63636364,  0.54545455,  1.        ])

    Now, it is easy to use the formula in reverse to see that we get the
    original values, which we stored in `v_old`

    >>> approx_old = -alpha*v[:-2] + (2*alpha + 1)*v[1:-1] - alpha*v[2:]
    >>> diff = approx_old - v_old[1:-1]
    >>> diff
    array([  0.00000000e+00,  -1.11022302e-16,   0.00000000e+00,
            -1.11022302e-16])


    U(1) = 1
    --------
    First a single step
    >>> v = np.zeros(n+2)
    >>> v[-1] = 1
    >>> t = diffusion_1d(v, iterations, alpha, solver, silent=silent)
    >>> v
    array([ 0.        ,  0.01818182,  0.05454545,  0.14545455,  0.38181818,  1.        ])
    >>> v_1_step = v.copy()

    Then a second step
    >>> t = diffusion_1d(v, iterations, alpha, solver, silent=silent)
    >>> v
    array([ 0.        ,  0.04793388,  0.12561983,  0.27438017,  0.55206612,  1.        ])

    Check that running two steps in one call gives same result
    >>> iterations = 2
    >>> v = np.zeros(n+2)
    >>> v[-1] = 1
    >>> t = diffusion_1d(v, iterations, alpha, solver, silent=silent)
    >>> v
    array([ 0.        ,  0.04793388,  0.12561983,  0.27438017,  0.55206612,  1.        ])

    Check that we get `v_step_1` by reversing one step
    >>> approx_old = -alpha*v[:-2] + (2*alpha + 1)*v[1:-1] - alpha*v[2:]
    >>> diff = approx_old - v_1_step[1:-1]
    >>> diff
    array([  6.93889390e-18,   7.63278329e-17,  -5.55111512e-17,
             0.00000000e+00])

    """
    pass

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
