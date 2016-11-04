import numpy as np

def EnergyConfig(A, L, J):
    Ei = 0
    for i in range(L):
        for j in range(L):
            Ei += A[i,j] * A[i-1,j]
            Ei += A[i,j] * A[i,j-1]
    return -J*Ei

def deltaE(A, L, J, i, j):
    E_old_right = A[i,j] * A[(i+1)%L, j]
    E_old_left = A[i,j] * A[i-1, j]
    E_old_up = A[i,j] * A[i, (j+1)%L]
    E_old_down = A[i,j] * A[i, j-1]

    A[i,j] *= -1

    E_new_right = A[i,j] * A[(i+1)%L, j]
    E_new_left = A[i,j] * A[i-1, j]
    E_new_up = A[i,j] * A[i, (j+1)%L]
    E_new_down = A[i,j] * A[i, j-1]

    diff = -J*(E_new_right + E_new_left + E_new_up + E_new_down) - (E_old_right + E_old_left + E_old_up + E_old_down)
    return diff
