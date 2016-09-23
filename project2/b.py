import sys
import numpy as np

from common import *

if __name__ == '__main__':
    n = 40
    if len(sys.argv) > 1:
        n = float(sys.argv[1])
    A = make_matrix_noninteraction_case(n)
    R = np.eye(n)
    solve(A, R)
    eig_and_shit = sorted(A[range(n), range(n)])
    print eig_and_shit#[4:40:8]
    #print R
