from common import *

def _test_solve_1d(solver, LHS_formula, RHS_formula):
    np.random.seed(3150)

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
    np.random.seed(3150)

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
