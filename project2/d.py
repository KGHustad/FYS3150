import numpy as np
import sys

from common import *

if __name__ == '__main__':
    n = 40
    if len(sys.argv) > 1:
        n = float(sys.argv[1])
    omega_values = [0.01, 0.5, 1, 5]
    for omega in omega_values:
        A, rho = make_matrix_interacting_case(n, omega)
        R = np.eye(n)
        solve(A, R)
        eig_and_shit = sorted(A[range(n), range(n)])
        print eig_and_shit#[4:40:8]
    #print R
