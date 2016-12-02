# *-* coding: utf-8 *-*

import numpy as np
from scipy.linalg import lu

def COL_LU(A):
    n = A.shape[0]
    for k in xrange(n):         # column
        for j in xrange(k+1, n):  # row
            # eliminerer U langs kolonnen for å finne L-
            A[j, k] /= A[k, k]
        print "L-column done"
        print A

        for j in xrange(k+1, n):        # column
            for i in xrange(k+1, n):    # row
                # fjerner L-leddet
                A[i, j] -= A[i, k] * A[k, j]
        print "Col #%d of L and row #%d of U is done" % (k, k)
        print A
        print

#A = np.zeros((3, 3))
A = np.array([ [1, 2, 4], [3, 8, 14], [2, 6, 13] ], dtype=np.float64)
print "INPUT:"
print A
print "\n"

p, l, u = lu(A)

COL_LU(A)
print "\nOUTPUT:"
print A

print
n=3 
L = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float64)
U = np.zeros((n,n))#np.array([[1, 2, 4], [0, 1, -8], [0, 0, 1]], dtype=np.float64)
U = A.copy()

for i in xrange(1, n):
    for j in xrange(i):
        L[i, j] = A[i, j]
        U[i, j] = 0

print "\nL:"
print L
print "\nU:"
print U
print "\n\n"


def MAT_MULT(A, B):
    n = A.shape[0]
    C = np.zeros((n,n), dtype=np.float64)
    for row in xrange(n):
        for col in xrange(n):
            for k in xrange(n):
                C[row, col] += A[row, k] * B[k, col]
    return C

C = MAT_MULT(L, U)
print "L*U"
print C

"""
print "\nScipy\n"
print p
print
print l
print
print u
print
print np.dot(l, u)
"""