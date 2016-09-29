#import sys
#import numpy as np
import matplotlib.pyplot as plt
import argparse

from common import *

parser = argparse.ArgumentParser()
parser.add_argument('-N', '-n',
                    dest='n', metavar='N',
                    type=int, default=40)
parser.add_argument('-p', '--rho_max',
                    metavar='rho_max',
                    type=float, default=5)
parser.add_argument('-w', '--omega',
                    metavar='omega',
                    type=float, default=1)
parser.add_argument('--plot',
                    action='store_true', default=False)
parser.add_argument('--show',
                    action='store_true', default=False)
parser.add_argument('--interaction',
                    action='store_true', default=False)

args = parser.parse_args()
n = args.n
rho_max = args.rho_max
omega = args.omega
plot = args.plot
show = args.show
interaction = args.interaction
interaction_info = 'interacting' if interaction else 'non-interacting'

#print args

# setup input
if not interaction:
    A, rho = make_matrix_noninteracting_case(n, rho_max=rho_max)
else:
    A, rho = make_matrix_interacting_case(n, omega, rho_max)
R = np.eye(n)

# solve
iterations, time, tol = solve(A, R)
print "Solution with n=%d took %g seconds" % (n, time)

# extract eigenvalues and eigenvectors
sorted_eigs = extract_eigs(A, R)

# plot
if plot:
    legend = []
    levels=3
    for i in xrange(levels):
        plt.plot(rho[1:], sorted_eigs[i][1]**2)
        legend.append("$\\lambda$ = %g" % sorted_eigs[i][0])
    plt.legend(legend)
    plt.xlabel('$\\rho$')
    title = 'The %d lowest energy levels.\n' % levels
    if interaction:
        title += "$\\omega$=%g, " % omega
    title += 'n=%g,  %d it. (tol=%.0E)' % (n, iterations, tol)
    plt.title(title)
    info = interaction_info
    if interaction:
        # include omega value in filename
        info += "_omega=%g" % omega
    filename = 'fig/plot_%s_rho-max=%g_n=%03d.pdf' % (info, rho_max, n)
    print "Saving plot to %s" % filename
    plt.savefig(filename)
    if show:
        plt.show()
