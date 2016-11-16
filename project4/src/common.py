import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import random
import time
import ctypes
import math
import os

def get_lib_name():
    return 'libising.so'

def get_lib_path():
    this_file_dir = os.path.dirname(__file__)
    relative_lib_path = os.path.join(this_file_dir, 'c')
    return relative_lib_path

def homogeneous_spin_matrix(L, value=1):
    if not (value == 1 or value == -1):
        print "Spins must be -1 or 1"
        return None
    return np.full((L, L), value, dtype=np.int8)

def random_spin_matrix(L, seed=None):
    if seed != None:
        np.random.seed(seed)
    a = np.random.randint(0, 2, size=(L, L), dtype=np.int8)
    return np.ones(shape=(L, L), dtype=np.int8) - 2*a

def random_spin_matrix_c(L, seed=None):
    if seed == None:
        seed = 0
    spin = np.empty(shape=(L, L), dtype=np.int8)

    from ctypes import c_int8, c_int, c_ulong
    int8_array = np.ctypeslib.ndpointer(dtype=c_int8, ndim=1,
                                        flags="contiguous")
    libising = np.ctypeslib.load_library(get_lib_name(), get_lib_path())
    libising.fill_random.argstypes = [int8_array, c_int, c_ulong]
    libising.fill_random(np.ctypeslib.as_ctypes(spin),
                         c_int(L),
                         c_ulong(seed))
    return spin

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

def metropolis_c(spin, J, T, sweeps, save_every_nth=1, seed=0, silent=False):
    if not spin.dtype == np.int8:
        print "Wrong usage! Spin array must be of dtype np.int8"
        return

    L = spin.shape[0]

    saved_states = sweeps/save_every_nth + 1

    energies = np.empty(saved_states, dtype=np.float64)
    tot_magnetization = np.empty(saved_states, dtype=np.int64)

    # import and create the needed types
    from ctypes import c_int8, c_int, c_long, c_ulong, c_double
    c_long_ptr = ctypes.POINTER(c_long)
    c_double_ptr = ctypes.POINTER(c_double)
    int8_array = np.ctypeslib.ndpointer(dtype=c_int8, ndim=1,
                                        flags="contiguous")
    int64_array = np.ctypeslib.ndpointer(dtype=c_long, ndim=1,
                                        flags="contiguous")
    float64_array = np.ctypeslib.ndpointer(dtype=c_double, ndim=1,
                                        flags="contiguous")

    # load library
    libising = np.ctypeslib.load_library(get_lib_name(), get_lib_path())
    libising.python_interface.argstypes = [int8_array,
                                           c_int,
                                           c_int,
                                           c_double,
                                           c_double,
                                           c_double_ptr,
                                           c_long_ptr,
                                           c_long_ptr,
                                           c_long,
                                           c_ulong]

    # make c primitives to pass by reference
    accepted_configurations = c_long(0)


    # call library interface function
    pre = time.clock()
    libising.python_interface(np.ctypeslib.as_ctypes(spin),
                              c_int(L),
                              c_long(sweeps),
                              c_double(J),
                              c_double(T),
                              np.ctypeslib.as_ctypes(energies),
                              np.ctypeslib.as_ctypes(tot_magnetization),
                              ctypes.byref(accepted_configurations),
                              c_long(save_every_nth),
                              c_ulong(seed)
                              )
    post = time.clock()
    time_spent = post - pre

    if not silent:
        print "Time spent (C): %g" % time_spent

    mean_magnetization = abs(tot_magnetization)
    return energies, mean_magnetization, accepted_configurations.value, time_spent

def extract_expectation_values(energies, mean_magnetization):
    mu_E = np.mean(energies)
    mu_M = np.mean(mean_magnetization)
    mu_abs_M = np.mean(abs(mean_magnetization))
    mu_E_sq = np.mean(energies**2)
    mu_M_sq = np.mean(mean_magnetization**2)
    return mu_E, mu_M, mu_abs_M, mu_E_sq, mu_M_sq

def Magnetization(A):
    return abs(np.sum(A))

def show_spins(spin):
    plt.imshow(spin, cmap=plt.cm.gray, vmin=-1, vmax=1, interpolation='none')
    plt.show()

def expectation_values(values_array, mc_cycles):
    denom = np.arange(1, (mc_cycles+1), dtype=np.float64)
    return np.cumsum(values_array) / denom


#Analytical expressions for expectations values of 2x2 lattice.

def analytical_mean_energy(J, T):
    beta = 1./T
    Z = 2*np.exp(-8*beta*J) + 2*np.exp(8*beta*J) + 12.0
    return -(-16*J*np.exp(-8*J*beta) + 16*J*np.exp(8*beta*J)) / Z

def analytical_mean_energy_squared(J, T):
    beta = 1./T
    Z = 2*np.exp(-8*beta*J) + 2*np.exp(8*beta*J) + 12.0
    return (128*J**2*np.exp(-8*beta*J) + 128*J**2*np.exp(8*beta*J)) / Z

def analytical_mean_abs_magnetization(J, T):
    beta = 1./T
    Z = 2*np.exp(-8*beta*J) + 2*np.exp(8*beta*J) + 12.0
    return (16 + 8*np.exp(8*beta)) / Z

def analytical_mean_magnetization_squared(J, T):
    beta = 1./T
    Z = 2*np.exp(-8*beta*J) + 2*np.exp(8*beta*J) + 12.0
    return (32 + 32*np.exp(8*beta*J)) / Z

def heat_capacity(J, T):
    beta = 1./T
    return ( analytical_mean_energy_squared(J, T) - analytical_mean_energy(J, T)**2 ) / ( T**2 )

def susceptibility(J, T):
    beta = 1./T
    return ( analytical_mean_magnetization_squared(J, T) - analytical_mean_abs_magnetization(J, T)**2 ) / ( T**2 )