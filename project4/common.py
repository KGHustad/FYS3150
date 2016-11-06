import numpy as np
import random

def EnergyConfig(A, J):
    L = A.shape[0]
    Ei = 0
    for i in range(L):
        for j in range(L):
            Ei += A[i,j] * A[i-1,j]
            Ei += A[i,j] * A[i,j-1]
    return -J*Ei

def deltaE(A, J, i, j):
    L = A.shape[0]
    E_old_right = A[i,j] * A[(i+1)%L, j]
    E_old_left = A[i,j] * A[i-1, j]
    E_old_up = A[i,j] * A[i, (j+1)%L]
    E_old_down = A[i,j] * A[i, j-1]
    E_old = (E_old_right + E_old_left + E_old_up + E_old_down)

    diff = J*2*E_old
    return diff

def Metropolis(A, J, steps):
    L = A.shape[0]
    Energy = np.zeros(steps+1)
    Energy[0] = EnergyConfig(A, J)
    for k in range(steps):
        i = random.randint(0,L-1)
        j = random.randint(0,L-1)
        dE = deltaE(A, J, i, j)
        if dE <= 0:
            A[i,j] *= -1
            Energy[k+1] = dE
        Energy[k+1] += Energy[k]
    return A, Energy

def Magnetization(A):
    return abs(np.sum(A))
