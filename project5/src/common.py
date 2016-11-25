import numpy as np
import os
import ctypes

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
