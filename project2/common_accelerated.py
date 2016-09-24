from scipy import weave
import numpy as np
#from common import *

def find_max_nondiagonal(A):
    #print "Using accelerated function"
    """Finds the largest (in absolute value) non-diagonal element, a_kl, in an
    n x n matrix, A, and returns abs(a_kl) and its coordinates, k and l.

    >>> np.random.seed(3150)
    >>> n = 4
    >>> A = (np.random.rand(n,n)*-0.5 + np.eye(n))*10
    >>> A
    array([[ 8.9581678 , -0.44587921, -3.99281836, -2.34452466],
           [-2.74278801,  6.00382443, -2.05360951, -0.44483021],
           [-1.95052115, -3.32927787,  8.43516216, -4.84465403],
           [-0.07153444, -1.42596855, -0.13139105,  5.21781942]])
    >>> find_max_nondiagonal(A)
    (4.8446540255955943, 2, 3)
    """
    n = A.shape[0]
    code = """
    int max_k = 0;
    int max_l = 1;
    double maximum = fabs(A[max_k*n + max_l]);
    double current;
    int i, j;
    for (i=0; i < n; i++) {
        for (j=0; j < n; j++) {
            if (i != j) {
                current = fabs(A[i*n + j]);
                if (current > maximum) {
                    maximum = current;
                    max_k = i;
                    max_l = j;
                }
            }
        }
    }
    coor[0] = max_k;
    coor[1] = max_l;
    """
    coor = np.zeros(2, dtype=np.int32)

    weave.inline(code,
                 arg_names=['A', 'n', 'coor'],
                 headers=['<math.h>',   #for round
                          #'<stdio.h>',  #for printing
                          #'<string.h>', #for memcpy
                         ],
                 extra_compile_args=['-O3',             #optimize loops
                                     #'-w',              #surpress warnings
                                     '-march=native'    #optimize for processor
                                    ],
                )

    max_k = coor[0]
    max_l = coor[1]
    maximum = abs(A[max_k, max_l])
    return maximum, max_k, max_l
