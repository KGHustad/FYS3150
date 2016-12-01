import numpy as np
import os
import ctypes
import time

# utility functions for smart path handling
def get_lib_name():
    return 'libdiffuse.so'

def get_lib_path():
    this_file_dir = os.path.dirname(__file__)
    relative_lib_path = os.path.join(this_file_dir, 'c')
    return relative_lib_path

def get_proj_path():
    this_file_dir = os.path.dirname(__file__)
    proj_path = os.path.abspath(os.path.join(this_file_dir, '..'))
    return proj_path

def load_lib():
    return np.ctypeslib.load_library(get_lib_name(), get_lib_path())

def load_lib_alt():
    return ctypes.CDLL(os.path.join(get_lib_path(), get_lib_name()))

def diffusion_2d(v, f, iterations, kappa, bc_left=0, bc_right=0,
                 bc_top=0, bc_bottom=0, omp=False, silent=False):
    #libdiffuse = load_lib()
    libdiffuse = load_lib_alt()

    # type stuff
    from ctypes import c_double, c_int
    c_double_ptr = ctypes.POINTER(c_double)
    float64_array_2d = np.ctypeslib.ndpointer(dtype=c_double, ndim=2,
                                          flags="contiguous")

    height, width = v.shape

    time_spent = c_double(0)

    solver_func = libdiffuse.solve_2d_omp if omp else libdiffuse.solve_2d

    solver_func.restype = None
    solver_func.argtypes = [float64_array_2d,
                            float64_array_2d,
                            c_int,
                            c_int,
                            c_double,
                            c_int,
                            c_int,
                            c_int,
                            c_int,
                            c_int,
                            c_double_ptr
                            ]
    solver_func(v,
                f,
                c_int(height),
                c_int(width),
                c_double(kappa),
                c_int(iterations),
                c_int(bc_left),
                c_int(bc_right),
                c_int(bc_top),
                c_int(bc_bottom),
                ctypes.byref(time_spent)
                )

    if not silent:
        print "Time spent (C): %g" % time_spent.value

    return time_spent.value
