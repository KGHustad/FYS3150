import numpy as np
import sys

from common import *

if __name__ == '__main__':
    n = 4
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    omega_values = [0.01, 0.5, 1, 5]
    for omega in omega_values:
        print "Omega = %g" % omega
        A, rho = make_matrix_interacting_case(n, omega)
        A_np = A.copy()
        R = np.eye(n)

        solve(A, R)
        eig = extract_eigs_dict(A, R)
        print eig['val'][:3]

        eigvals_np, eigvecs_np, w, v = solve_np(A_np)
        diff = R - v
        print diff
        print abs(diff).max(axis=(0,1))
