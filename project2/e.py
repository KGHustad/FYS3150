import numpy as np
import matplotlib.pyplot as plt
import sys
from operator import itemgetter

from common import *

if __name__ == '__main__':
    n = 40
    if len(sys.argv) > 1:
        n = float(sys.argv[1])
    A, rho = make_matrix_noninteraction_case(n)
    R = np.eye(n)

    solve(A, R)


    eigvals = A[range(n), range(n)]
    print eigvals
    eigvecs = [R[:][i]**2 for i in xrange(n)]
    eigs = [(eigval, eigvec) for eigval, eigvec in zip(eigvals, eigvecs)]
    sorted_eigs = sorted(eigs, key=itemgetter(0))
    print sorted(eigvals)


    #print R
    plt.plot(rho[1:], R[4][:])
    plt.plot(rho[1:], R[:][4])
    #plt.plot(rho[1:], diff)
    plt.show()

    A2, rho = make_matrix_noninteraction_case(n)
    w, v = np.linalg.eig(A2)


    kk = 0
    plt.plot(rho[1:], v[kk][:])
    plt.plot(rho[1:], R[kk][:])
    plt.legend(['r','c'])
    plt.show()

    #"""
    for i in xrange(1):
        plt.plot(rho[1:], sorted_eigs[i][1])
    plt.show()
    #"""

    #print eigvals
    #print eigvecs

    #eig_and_shit = sorted(A[range(n), range(n)])
    #print eig_and_shit#[4:40:8]
