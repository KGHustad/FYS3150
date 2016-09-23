import numpy as np
import matplotlib.pyplot as plt
import sys
from operator import itemgetter

from common import *


if __name__ == '__main__':
    n = 40
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    A, rho = make_matrix_noninteraction_case(n)
    R = np.eye(n)

    solve(A, R)

    # extract eigenvalues and eigenvectors
    eigvals = A[range(n), range(n)]
    eigvecs = [np.transpose(R)[i] for i in xrange(n)]
    eigs = [(eigval, eigvec, i) for i, (eigval, eigvec) in enumerate(zip(eigvals, eigvecs))]
    sorted_eigs = sorted(eigs, key=itemgetter(0))

    # plot
    legend = []
    for i in xrange(3):
        plt.plot(rho[1:], sorted_eigs[i][1]**2)
        legend.append("Eigval: %g" % sorted_eigs[i][0])
    plt.legend(legend)
    plt.xlabel('rho')
    plt.title('The three lowest energy levels.   n=%g' % n)
    plt.savefig('fig/plot_e.pdf')
