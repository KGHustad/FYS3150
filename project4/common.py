import numpy as np

array = np.array( [ [-1,1], [1,-1] ] )

def EnergyConfig(J, A, L):
    Ei = 0
    for i in range(L-1):
        Ei += A[i,L-1]*A[i+1,L-1]
        Ei += A[i,L-1]*A[i, L-2]
        Ei += A[i,L-1]*A[i-1, L-1]
        Ei += A[i,L-1]*A[i, 0]
        print Ei
        Ei += A[L-1,i]*A[L-1, i+1]
        Ei += A[L-1,i]*A[L-2, i]
        Ei += A[L-1,i]*A[ L-1, i-1]
        Ei += A[L-1,i]*A[0, i]
        print Ei
        for j in range(L-1):
            Ei += A[i,j]*A[i+1,j]
            Ei += A[i,j]*A[i,j+1]
            Ei += A[i,j]*A[i-1,j]
            Ei += A[i,j]*A[i,j-1]
            print Ei
    Ei += A[-1,-1]*A[-2,-1]
    Ei += A[-1,-1]*A[-1,-2]
    Ei += A[-1,-1]*A[-1,0]
    Ei += A[-1,-1]*A[0,-1]
    return -J*Ei

print EnergyConfig(1, array, 2)
