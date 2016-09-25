import sys
import numpy as np

from common import *

if __name__ == '__main__':
    n = 40
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    A, rho = make_matrix_noninteracting_case(n)
    R = np.eye(n)
    solve(A, R)
    eig = extract_eigs_dict(A, R)
    print eig['val'][:3]
