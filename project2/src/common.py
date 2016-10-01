import math
import numpy as np
import matplotlib.pyplot as plt
import time
import ctypes
import scipy.integrate as integrate
from scipy import weave
from operator import itemgetter

def find_max_nondiagonal_symmetrical_pure_python(A):
    """Finds the largest (in absolute value) non-diagonal element, a_kl, in an
    n x n matrix, A, and returns abs(a_kl) and its coordinates, k and l.

    >>> np.random.seed(3150)
    >>> n = 4
    >>> A = (np.random.rand(n,n)*-0.5 + np.eye(n))*10
    >>> A = A + np.transpose(A)
    >>> A
    array([[ 17.91633559,  -3.18866722,  -5.94333952,  -2.41605909],
           [ -3.18866722,  12.00764887,  -5.38288739,  -1.87079876],
           [ -5.94333952,  -5.38288739,  16.87032431,  -4.97604507],
           [ -2.41605909,  -1.87079876,  -4.97604507,  10.43563885]])
    >>> find_max_nondiagonal_symmetrical_pure_python(A)
    (5.9433395159259188, 0, 2)
    """
    n = A.shape[0]
    maximum = abs(A[0,1])
    max_k=0
    max_l=1
    for i in xrange(n):
        for j in xrange(i+1, n):
            if abs(A[i,j]) > maximum:
                maximum = abs(A[i,j])
                max_k = i
                max_l = j
    return maximum, max_k, max_l

def find_max_nondiagonal_symmetrical_weave(A):
    """Finds the largest (in absolute value) non-diagonal element, a_kl, in an
    n x n matrix, A, and returns abs(a_kl) and its coordinates, k and l.

    >>> np.random.seed(3150)
    >>> n = 4
    >>> A = (np.random.rand(n,n)*-0.5 + np.eye(n))*10
    >>> A = A + np.transpose(A)
    >>> A
    array([[ 17.91633559,  -3.18866722,  -5.94333952,  -2.41605909],
           [ -3.18866722,  12.00764887,  -5.38288739,  -1.87079876],
           [ -5.94333952,  -5.38288739,  16.87032431,  -4.97604507],
           [ -2.41605909,  -1.87079876,  -4.97604507,  10.43563885]])
    >>> find_max_nondiagonal_symmetrical_weave(A)
    (5.9433395159259188, 0, 2)
    """
    n = A.shape[0]
    code = """
    int max_k = 0;
    int max_l = 1;
    double maximum = fabs(A[max_k*n + max_l]);
    double current;
    int i, j;

    for (i=0; i < n; i++) {
        for (j=i+1; j < n; j++) {
            current = fabs(A[i*n + j]);
            if (current > maximum) {
                maximum = current;
                max_k = i;
                max_l = j;
            }
        }
    }
    coor[0] = max_k;
    coor[1] = max_l;
    """
    coor = np.zeros(2, dtype=np.int32)

    weave.inline(code,
                 arg_names=['A', 'n', 'coor'],
                 headers=['<math.h>',   #for fabs
                         ],
                 extra_compile_args=['-O2',             #optimize loops
                                     '-w',              #surpress warnings
                                     '-march=native'    #optimize for processor
                                    ],
                )

    max_k = coor[0]
    max_l = coor[1]
    maximum = abs(A[max_k, max_l])
    return maximum, max_k, max_l


# use weave
find_max_nondiagonal_symmetrical = find_max_nondiagonal_symmetrical_weave

def solve(A, R, tol=1E-8, silent=False):
    pre = time.clock()
    n = A.shape[0]

    iterations = 0
    maximum, k, l = find_max_nondiagonal_symmetrical(A)
    while maximum > tol:
        iterations += 1
        #print R[:][1].dot(R[:][0])
        rotate(A, R, k, l)
        maximum, k, l = find_max_nondiagonal_symmetrical(A)

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


def make_matrix_noninteracting_case(n, omega=1, rho_max=5):
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
    V = np.zeros(n+1)
    V[1:] = omega**2*rho[1:]**2
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

def plot_interactive(n, omega_values, rho_max, solver, show=False):
    # setup input
    legend = []
    for omega in omega_values:
        #print omega

        A, rho = make_matrix_interacting_case(n, omega, rho_max=rho_max)
        R = np.eye(n)


        # solve
        if solver == 'python':
            iterations, time, tol = solve(A, R)
        elif solver == 'c':
            iterations, time, tol = solve_c(A, R)
        print "Solution with n=%d took %g seconds" % (n, time)

        # extract eigenvalues and eigenvectors
        sorted_eigs = extract_eigs(A, R)

        # plot
        x = rho[1:]
        y = sorted_eigs[0][1]**2

        # ensure y is a valid probability density function
        y_pdf = y/integrate.simps(y, x)

        plt.plot(x, y_pdf)
        legend.append("$\\omega$ = %g" % omega)
    plt.legend(legend)
    plt.xlabel('$\\rho$')
    plt.ylabel('probability')
    title = 'Interactive case\n'
    title += 'n=%g,  %d it. (tol=%.0E)' % (n, iterations, tol)
    plt.title(title)
    info = 'interacting'

    # include omega value in filename
    omega_values_str = ",".join(["%g"% omega for omega in omega_values])
    info += "_omega=%s" % omega_values_str
    filename = 'fig/plot_%s_rho-max=%g_n=%03d.pdf' % (info, rho_max, n)
    print "Saving plot to %s" % filename
    plt.savefig(filename)
    if show:
        plt.show()
    plt.clf()

if __name__ == '__main__':
    test_solve()
