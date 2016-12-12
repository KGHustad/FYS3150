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


def _test_solve_1d(solver, LHS_formula, RHS_formula):
    silent = True
    n = 4
    alpha = 0.1
    atol = 0
    rtol = 1e-15

    v_original = np.random.random(n+2)

    # check that LHS == RHS
    v = v_original.copy()
    v_new = v_original.copy()
    diffusion_1d(v_new, 1, alpha, solver=solver, silent=silent)

    LHS = LHS_formula(v_new, alpha)
    RHS = RHS_formula(v, alpha)
    msg = "Arrays are not almost equal! Difference:\n" + str(LHS - RHS)
    assert np.allclose(LHS, RHS, atol=0, rtol=rtol), msg

    # check that 2 iterations equal 1 + 1 iterations
    v_a = v_original.copy()
    v_b = v_original.copy()
    diffusion_1d(v_a, 1, alpha, solver=solver, silent=silent)
    diffusion_1d(v_a, 1, alpha, solver=solver, silent=silent)
    diffusion_1d(v_b, 2, alpha, solver=solver, silent=silent)
    msg = "Arrays are not equal! Difference:\n" + str(LHS - RHS)
    assert np.array_equal(v_a, v_b), msg

def test_solve_1d_forward_euler():
    LHS = lambda v, n: v[1:-1]
    RHS = lambda v, alpha: (alpha*v[:-2]
                               + (1 - 2*alpha)*v[1:-1]
                               + alpha*v[2:])
    _test_solve_1d('forward_euler', LHS, RHS)

def test_solve_1d_backward_euler():
    LHS = lambda v, alpha: (-alpha*v[:-2]
                               + (2*alpha + 1)*v[1:-1]
                               - alpha*v[2:])
    RHS = lambda v, alpha: v[1:-1]
    _test_solve_1d('backward_euler', LHS, RHS)

def test_solve_1d_crank_nicolson():
    LHS = lambda v, alpha: (-alpha*v[:-2]
                               + (2 + 2*alpha)*v[1:-1]
                               - alpha*v[2:])
    RHS = lambda v, alpha: (alpha*v[:-2]
                               + (2 - 2*alpha)*v[1:-1]
                               + alpha*v[2:])
    _test_solve_1d('crank_nicolson', LHS, RHS)

def _test_solve_2d(solver, omp):
    silent = True
    n = 4
    alpha = 0.1
    atol = 0
    rtol = 1e-15

    v_original = np.random.random((n+2, n+2))

    # check that LHS == RHS
    v = v_original.copy()
    v_new = v_original.copy()
    solver(v_new, 1, alpha, omp=omp, silent=silent)

    LHS = v_new[1:-1, 1:-1]
    RHS = v[1:-1,1:-1] \
          + alpha*(                     v[0:-2, 1:-1]
                  + v[1:-1, 0:-2]   - 4*v[1:-1, 1:-1]    + v[1:-1, 2:]
                                    +   v[2:,   1:-1])
    assert np.allclose(LHS, RHS, atol=0, rtol=rtol)

    # check that 2 iterations equal 1 + 1 iterations
    v_a = v_original.copy()
    v_b = v_original.copy()
    solver(v_a, 1, alpha, omp=omp, silent=silent)
    solver(v_a, 1, alpha, omp=omp, silent=silent)
    solver(v_b, 2, alpha, omp=omp, silent=silent)
    assert np.array_equal(v_a, v_b)

def test_solve_2d_serial():
    _test_solve_2d(diffusion_2d, omp=False)

def test_solve_2d_omp():
    _test_solve_2d(diffusion_2d, omp=True)
