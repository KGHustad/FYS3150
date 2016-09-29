import numpy as np
import matplotlib.pyplot as plt
import sys
from operator import itemgetter

from common import *
#from common_accelerated import *


if __name__ == '__main__':
    n = 40
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    A, rho = make_matrix_noninteracting_case(n)
    R = np.eye(n)

    iterations, time, tol = solve(A, R)
    print "Solution with n=%d took %g seconds" % (n, time)

    # extract eigenvalues and eigenvectors
    sorted_eigs = extract_eigs(A, R)

    # plot
    legend = []
    levels=3
    for i in xrange(levels):
        plt.plot(rho[1:], sorted_eigs[i][1]**2)
        legend.append("$\\lambda$ = %g" % sorted_eigs[i][0])
    plt.legend(legend)
    plt.xlabel('$\\rho$')
    title = 'The %d lowest energy levels.\n' % levels
    title += 'n=%g,  %d it. (tol=%.0E)' % (n, iterations, tol)
    plt.title(title)
    plt.savefig('fig/plot_e_n=%03d.pdf' % n)
