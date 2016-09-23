import numpy as np
import sys

def solve(A, R, tol=1E-8):
    # find max
    def find_max(A):
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

    iterations = 0
    maximum, k, l = find_max(A)
    while maximum > tol:
        iterations += 1
        single_step(A, R, k, l)
        maximum, k, l = find_max(A)

    print "Solved in %g iterations" % iterations

def single_step(A, R, k, l):
    tau = (A[l,l] - A[k,k])/(2*A[k,l])
    #t_1 = -tau + np.sqrt(1 + tau**2)
    #t_2 = -tau - np.sqrt(1 + tau**2)
    #t = min(abs(t_1), abs(t_2))
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
        R[i,l] = c*r_il - s*r_ik

def make_input_random(n):
    A = np.random.rand(n,n)*10-5
    #for i in xrange(n)

def make_matrix(n, rho_max=5):
    """Creates A"""
    A = np.zeros(shape=(n,n))

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
    return A

if __name__ == '__main__':
    n = 40
    if len(sys.argv) > 1:
        n = float(sys.argv[1])
    A = make_matrix(n)
    R = np.eye(n)
    solve(A, R)
    eig_and_shit = sorted(A[range(n), range(n)])
    print eig_and_shit#[4:40:8]
    #print R
