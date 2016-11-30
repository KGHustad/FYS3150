from common import *
from mpi4py import MPI

"""The MPI code has been placed in a separate file so that one can run the
sequential program without MPI or mpi4py installed"""

def diffusion_2d_mpi(v, f, iterations, kappa):
    #libdiffuse = load_lib()
    libdiffuse = load_lib_alt()

    # type stuff
    from ctypes import c_double, c_int
    if MPI._sizeof(MPI.Comm) == ctypes.sizeof(ctypes.c_int):
        MPI_Comm = ctypes.c_int
        print "MPI_COMM is an int"
    else:
        MPI_Comm = ctypes.c_void_p
        print "MPI_COMM is a void pointer"
    print MPI_Comm

    float64_array_2d = np.ctypeslib.ndpointer(dtype=c_double, ndim=2,
                                          flags="contiguous")

    # MPI_Comm
    comm = MPI.COMM_WORLD
    comm_ptr = MPI._addressof(comm)
    comm_val = MPI_Comm.from_address(comm_ptr)
    print comm_val

    height, width = v.shape

    print np.ctypeslib.as_ctypes(v)
    print np.ctypeslib.as_ctypes(f)

    libdiffuse.solve_2d_mpi.restype = None
    libdiffuse.solve_2d_mpi.argtypes = [float64_array_2d,
                                        float64_array_2d,
                                        c_int,
                                        c_int,
                                        c_double,
                                        c_int,
                                        MPI_Comm]
    libdiffuse.solve_2d_mpi(#np.ctypeslib.as_ctypes(v),
                            #np.ctypeslib.as_ctypes(f),
                            v,
                            f,
                            c_int(height),
                            c_int(width),
                            c_double(kappa),
                            c_int(iterations),
                            comm_val
                            )
