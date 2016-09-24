import numpy as np
import matplotlib.pyplot as plt
import sys
from operator import itemgetter

from common import *
from common_accelerated import *


if __name__ == '__main__':
    n = 40
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    A, rho = make_matrix_noninteracting_case(n)
    R = np.eye(n)

    iterations, time = solve(A, R)
    print "Solution with n=%d took %g seconds" % (n, time)

    # extract eigenvalues and eigenvectors
    sorted_eigs = extract_eigs(A, R)

    # plot
    legend = []
    for i in xrange(3):
        plt.plot(rho[1:], sorted_eigs[i][1]**2)
        legend.append("Eigval: %g" % sorted_eigs[i][0])
    plt.legend(legend)
    plt.xlabel('rho')
    plt.title('The three lowest energy levels.   n=%g' % n)
    plt.savefig('fig/plot_e_n=%03d.pdf' % n)
