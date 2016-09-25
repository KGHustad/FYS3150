import numpy as np
import sys

from common import *

if __name__ == '__main__':
    n = 40
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    omega_values = [0.01, 0.5, 1, 5]
    for omega in omega_values:
        print "Omega = %g" % omega
        A, rho = make_matrix_interacting_case(n, omega)
        R = np.eye(n)
        solve(A, R)
        eig = extract_eigs_dict(A, R)
        print eig['val'][:3]
