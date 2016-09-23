import numpy as np
import matplotlib.pyplot as plt
import sys
from operator import itemgetter

from common import *

def sorted_matrix(B):
    A = B.copy()
    return A[A[0,:].argsort()]

if __name__ == '__main__':
    n = 40
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    A, rho = make_matrix_noninteraction_case(n)
    R = np.eye(n)

    solve(A, R)

    eigvals = A[range(n), range(n)]
    eigvecs = [np.transpose(R)[i] for i in xrange(n)]
    eigs = [(eigval, eigvec, i) for i, (eigval, eigvec) in enumerate(zip(eigvals, eigvecs))]
    sorted_eigs = sorted(eigs, key=itemgetter(0))


    #k= 4
    #plt.plot(rho[1:], R[k][:])
    #plt.plot(rho[1:], R[:][k])
    #plt.plot(rho[1:], diff)
    #plt.show()

    """
    A2, rho = make_matrix_noninteraction_case(n)
    w, v = np.linalg.eig(A2)
    np_eigvec = sorted_matrix(v)
    our_eigvec = sorted_matrix(R)
    diff_eigvec = our_eigvec - np_eigvec
    max_diff_eigvec = abs(diff_eigvec).max(axis=(0,1))
    if max_diff_eigvec > 1E-8:
        #print "Numpy's eigvecs\n", v
        #print "Our eigvecs\n", R
        print "Max diff = %g" % max_diff_eigvec
    else:
        print "Numpy agrees with our eigenvectors (max diff = %g)" % max_diff_eigvec
    """

    #kk = 0
    #plt.plot(rho[1:], v[kk][:])
    #plt.plot(rho[1:], R[kk][:])
    #plt.legend(['r','c'])
    #plt.show()

    #"""
    legend = []
    for i in xrange(3):
        plt.plot(rho[1:], sorted_eigs[i][1]**2)
        legend.append("Eigval: %g" % sorted_eigs[i][0])
    plt.legend(legend)
    plt.xlabel('rho')
    plt.title('The three lowest energy levels.   n=%g' % n)
    plt.savefig('fig/plot_e.pdf')
    #"""

    #print eigvals
    #print eigvecs

    #eig_and_shit = sorted(A[range(n), range(n)])
    #print eig_and_shit#[4:40:8]
