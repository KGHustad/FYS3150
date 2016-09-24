import numpy as np
import time
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


def solve(A, R, tol=1E-8, silent=False):
    pre = time.clock()
    n = A.shape[0]

    iterations = 0
    maximum, k, l = find_max_nondiagonal(A)
    while maximum > tol:
        iterations += 1
        #print R[:][1].dot(R[:][0])
        single_step(A, R, k, l)
        maximum, k, l = find_max_nondiagonal(A)

    post = time.clock()
    time_spent = post - pre
    if not silent:
        print "Solved in %g iterations" % iterations
    return iterations, time_spent

def single_step(A, R, k, l):
    n = A.shape[0]
    tau = (A[l,l] - A[k,k])/(2*A[k,l])
    if tau > 0:
        t = 1./(tau + np.sqrt(1 + tau*tau))
    else:
        t = 1./(tau - np.sqrt(1 + tau*tau))
    c = 1 / np.sqrt(1+t**2)
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

def extract_eigs(A, R):
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
    eigvecs = [R[:,i] for i in xrange(n)]
    eigs = [(eigval, eigvec, i) for i, (eigval, eigvec) in enumerate(zip(eigvals, eigvecs))]
    sorted_eigs = sorted(eigs, key=itemgetter(0))
    return sorted_eigs
