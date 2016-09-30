import math
import numpy as np
import time
import ctypes
from operator import itemgetter

def find_max_nondiagonal(A):
    """Finds the largest (in absolute value) non-diagonal element, a_kl, in an
    n x n matrix, A, and returns abs(a_kl) and its coordinates, k and l.

    >>> np.random.seed(3150)
    >>> n = 4
    >>> A = (np.random.rand(n,n)*-0.5 + np.eye(n))*10
    >>> A
    array([[ 8.9581678 , -0.44587921, -3.99281836, -2.34452466],
           [-2.74278801,  6.00382443, -2.05360951, -0.44483021],
           [-1.95052115, -3.32927787,  8.43516216, -4.84465403],
           [-0.07153444, -1.42596855, -0.13139105,  5.21781942]])
    >>> find_max_nondiagonal(A)
    (4.8446540255955943, 2, 3)
    """
    n = A.shape[0]
    maximum = abs(A[0,1])
    max_k=0
    max_l=1
    for i in xrange(n):
        for j in xrange(n):
            if i != j:
                if abs(A[i,j]) > maximum:
                    maximum = abs(A[i,j])
                    max_k = i
                    max_l = j
    return maximum, max_k, max_l

from common_accelerated import find_max_nondiagonal

def solve(A, R, tol=1E-8, silent=False):
    pre = time.clock()
    n = A.shape[0]

    iterations = 0
    maximum, k, l = find_max_nondiagonal(A)
    while maximum > tol:
        iterations += 1
        #print R[:][1].dot(R[:][0])
        rotate(A, R, k, l)
        maximum, k, l = find_max_nondiagonal(A)

    post = time.clock()
    time_spent = post - pre
    if not silent:
        print "Reached tolerance (%.0E) in %g iterations" % (tol, iterations),
        print "(%.2f iterations/element)" % (iterations/float(n**2))
    return iterations, time_spent, tol

def rotate(A, R, k, l):
    n = A.shape[0]
    tau = (A[l,l] - A[k,k])/(2*A[k,l])
    if tau > 0:
        t = 1./(tau + math.sqrt(1 + tau**2))
    else:
        t = 1./(tau - math.sqrt(1 + tau**2))
    c = 1 / math.sqrt(1+t**2)
    s = c*t

    # we need to store some values for later use
    a_kk = A[k,k]
    a_ll = A[l,l]

    A[k,k] = c**2*a_kk - 2*c*s*A[k,l] + s**2*a_ll
    A[l,l] = s**2*a_kk + 2*c*s*A[k,l] + c**2*a_ll
    A[k,l] = 0
    A[l,k] = 0

    for i in xrange(n):
        if i != k and i != l:
            a_ik = A[i,k]
            a_il = A[i,l]
            A[i,k] = c*a_ik - s*a_il
            A[k,i] = A[i,k]
            A[i,l] = c*a_il + s*a_ik
            A[l,i] = A[i,l]

        r_ik = R[i,k]
        r_il = R[i,l]
        R[i,k] = c*r_ik - s*r_il
        R[i,l] = c*r_il + s*r_ik


def make_matrix_noninteracting_case(n, rho_max=5):
    """Creates A for the non-interacting case

    >>> A, rho = make_matrix_noninteracting_case(5, rho_max=5)
    >>> A
    array([[  3.,  -1.,   0.,   0.,   0.],
           [ -1.,   6.,  -1.,   0.,   0.],
           [  0.,  -1.,  11.,  -1.,   0.],
           [  0.,   0.,  -1.,  18.,  -1.],
           [  0.,   0.,   0.,  -1.,  27.]])
    >>> rho
    array([ 0.,  1.,  2.,  3.,  4.,  5.])
    """
    A = np.zeros(shape=(n,n), dtype=np.float64)

    rho_0 = 0
    rho_n = rho_max
    rho = np.linspace(rho_0, rho_n, n+1)
    h = rho[1]-rho[0]
    V = rho**2
    d = 2/h**2 + V
    e = -1/h**2

    A[range(n), range(n)] = d[1:]
    A[range(1, n), range(n-1)] = e
    A[range(n-1), range(1, n)] = e
    return A, rho

def make_matrix_interacting_case(n, omega, rho_max=5):
    """Creates A for the interacting case

    >>> n = 4
    >>> omega = 2
    >>> A, rho = make_matrix_interacting_case(n, omega, rho_max=4)
    >>> A
    array([[  7.        ,  -1.        ,   0.        ,   0.        ],
           [ -1.        ,  18.5       ,  -1.        ,   0.        ],
           [  0.        ,  -1.        ,  38.33333333,  -1.        ],
           [  0.        ,   0.        ,  -1.        ,  66.25      ]])
    >>> rho
    array([ 0.,  1.,  2.,  3.,  4.])
    """
    A = np.zeros(shape=(n,n), dtype=np.float64)

    rho_0 = 0
    rho_n = rho_max
    rho = np.linspace(rho_0, rho_n, n+1)
    h = rho[1]-rho[0]
    V = np.zeros(n+1)
    V[1:] = omega**2*rho[1:]**2 + 1/rho[1:]
    d = 2/h**2 + V
    e = -1/h**2

    A[range(n), range(n)] = d[1:]
    A[range(1, n), range(n-1)] = e
    A[range(n-1), range(1, n)] = e
    return A, rho

def normalize_eigenvectors(eigenvectors):
    """Ensure the 1-norm of all eigenvectors is non-negative
    (the 2-norm is assumed to be 1)

    >>> np.random.seed(3150)
    >>> n = 4
    >>> a = np.random.randint(-5, 5, (n,n))
    >>> a
    array([[ 1, -4,  2, -5],
           [-2, -1, -1, -4],
           [ 0, -1, -3, -3],
           [-3,  0,  4, -4]])
    >>> eigenvectors = [a[:,i] for i in xrange(n)]
    >>> eigenvectors[0]
    array([ 1, -2,  0, -3])
    >>> eigenvectors[1]
    array([-4, -1, -1,  0])
    >>> eigenvectors[2]
    array([ 2, -1, -3,  4])
    >>> eigenvectors[3]
    array([-5, -4, -3, -4])
    >>> normalized_eigenvectors = normalize_eigenvectors(eigenvectors)
    >>> normalized_eigenvectors[0]
    array([-1,  2,  0,  3])
    >>> normalized_eigenvectors[1]
    array([4, 1, 1, 0])
    >>> normalized_eigenvectors[2]
    array([ 2, -1, -3,  4])
    >>> normalized_eigenvectors[3]
    array([5, 4, 3, 4])
    """
    for i in xrange(len(eigenvectors)):
        if sum(eigenvectors[i]) < 0:
            eigenvectors[i] = -eigenvectors[i]
    return eigenvectors

def extract_eigs(A, R, sort_R=True):
    """
    >>> np.random.seed(3150)
    >>> n = 3
    >>> A = np.random.rand(n,n)
    >>> R = np.random.rand(n,n)
    >>> A
    array([[ 0.20836644,  0.08917584,  0.79856367],
           [ 0.46890493,  0.5485576 ,  0.79923511],
           [ 0.4107219 ,  0.08896604,  0.39010423]])
    >>> R
    array([[ 0.66585557,  0.31296757,  0.96893081],
           [ 0.01430689,  0.28519371,  0.02627821],
           [ 0.95643612,  0.20162405,  0.29535341]])
    >>> eigs = extract_eigs(A, R)
    >>> eigs[0]
    (0.2083664405073874, array([ 0.66585557,  0.01430689,  0.95643612]), 0)
    >>> eigs[1]
    (0.39010423044182929, array([ 0.96893081,  0.02627821,  0.29535341]), 2)
    >>> eigs[2]
    (0.54855760104321716, array([ 0.31296757,  0.28519371,  0.20162405]), 1)
    """
    n = A.shape[0]
    eigvals = A[range(n), range(n)]
    eigvecs = normalize_eigenvectors([R[:,i].copy() for i in xrange(n)])
    eigs = [(eigval, eigvec, i) for i, (eigval, eigvec) in enumerate(zip(eigvals, eigvecs))]
    sorted_eigs = sorted(eigs, key=itemgetter(0))
    if sort_R:
        for i in xrange(n):
            R[:,i] = sorted_eigs[i][1]
    return sorted_eigs

def extract_eigs_dict(A, R):
    eigs = extract_eigs(A, R)
    eigs_dict = {}
    eigenvalues = np.array([eig[0] for eig in eigs])
    eigenvectors = [eig[1] for eig in eigs]
    original_columns = np.array([eig[2] for eig in eigs])
    eigs_dict['val'] = eigenvalues
    eigs_dict['vec'] = eigenvectors
    eigs_dict['org_col'] = original_columns
    return eigs_dict



def solve_np(A):
    n = A.shape[0]
    w, v = np.linalg.eigh(A)
    # w (N) holds eigenvalues, v (N,N) holds eigenvectors
    eigvals = w
    #print v
    eigvecs = [v[:,i].copy() for i in xrange(n)]
    eigvecs = normalize_eigenvectors(eigvecs)
    for i in xrange(n):
        v[:,i] = eigvecs[i][:]
    return eigvals, eigvecs, w, v

def solver_tester(solve):
    n = 10
    np.set_printoptions(linewidth=200)
    # set up input
    A, rho = make_matrix_noninteracting_case(n)
    R = np.eye(n)
    # make copy of A
    A_np = A.copy()

    # solve with our implementation of Jacobi's method
    solve(A, R)
    eig = extract_eigs_dict(A, R)

    # solve with NumPy (LAPACK)
    eigvals_np, eigvecs_np, w, v = solve_np(A_np)

    # compare
    msg = "Eigvals differ! Diff: " + str(eig['val'] - eigvals_np)
    assert np.allclose(eig['val'], eigvals_np), msg
    for i in xrange(n):
        eigvec_jacobi = eig['vec'][i]
        eigvec_np = eigvecs_np[i]
        msg = "Eigvec #%d: " % i + str(eigvec_jacobi - eigvec_np)
        assert np.allclose(eigvec_jacobi, eigvec_np), msg

def test_solve():
    solver_tester(solve)

def solve_c(A, R, tol=1E-8, silent=False):
    pre = time.clock()
    n = A.shape[0]

    #
    libjacobi = np.ctypeslib.load_library("jacobi.so", "src/c")

    float64_array = np.ctypeslib.ndpointer(dtype=ctypes.c_double, ndim=1, flags="contiguous")
    libjacobi.jacobi.argstypes = [float64_array, float64_array,
                                  ctypes.c_int, ctypes.c_double]

    iterations = libjacobi.jacobi(np.ctypeslib.as_ctypes(A),
                                  np.ctypeslib.as_ctypes(R),
                                  ctypes.c_int(n),
                                  ctypes.c_double(tol))

    post = time.clock()
    time_spent = post - pre
    if not silent:
        print "Reached tolerance (%.0E) in %g iterations" % (tol, iterations),
        print "(%.2f iterations/element)" % (iterations/float(n**2))
    return iterations, time_spent, tol

def test_solve_c():
    solver_tester(solve_c)

if __name__ == '__main__':
    test_solve()
