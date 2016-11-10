import numpy as np
import matplotlib.pyplot as plt
import random
import time
import ctypes

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

def metropolis_c(spin, J, T, mc_cycles, silent=False):
    if not spin.dtype == np.int8:
        print "Wrong usage! Spin array must be of dtype np.int8"
        return

    L = spin.shape[0]

    # fill in ctypes magic
    # import and create the needed types
    from ctypes import c_int8, c_int, c_long, c_double
    c_long_ptr = ctypes.POINTER(c_long)
    c_double_ptr = ctypes.POINTER(c_double)
    int8_array = np.ctypeslib.ndpointer(dtype=c_int8, ndim=1,
                                        flags="contiguous")

    # load library
    libising = np.ctypeslib.load_library("libising.so", "src/c")
    libising.python_interface.argstypes = [int8_array,
                                           c_int,
                                           c_int,
                                           c_double,
                                           c_double,
                                           c_double_ptr,
                                           c_long_ptr,
                                           c_long_ptr]

    # make c primitives to pass by reference
    energy = c_double(0)
    mean_magnetization = c_long(0)
    accepted_configurations = c_long(0)


    # call library interface function
    pre = time.clock()
    libising.python_interface(np.ctypeslib.as_ctypes(spin),
                              c_int(L),
                              c_long(mc_cycles),
                              c_double(J),
                              c_double(T),
                              ctypes.byref(energy),
                              ctypes.byref(mean_magnetization),
                              ctypes.byref(accepted_configurations)
                              )
    post = time.clock()
    time_spent = post - pre

    if not silent:
        print "Time spent (C): %g" % time_spent

    return energy.value, mean_magnetization.value, accepted_configurations.value, time_spent

def Magnetization(A):
    return abs(np.sum(A))

def show_spins(spin):
    plt.imshow(spin, cmap=plt.cm.gray, vmin=-1, vmax=1, interpolation='none')
    plt.show()