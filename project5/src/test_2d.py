from common_parallel import *
import matplotlib.pyplot as plt

iterations = int(1E4)

height = 20
width = 20
kappa = 1E-2

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

v = np.zeros((height, width), dtype=np.float64)
f = np.zeros((height, width), dtype=np.float64)

v[:,-1] = 1

diffusion_2d_parallel(v, f, iterations, kappa)
print v

def show_2d(v):
    plt.imshow(v, cmap=plt.cm.gray, interpolation='none')
    plt.show()

if rank == 0:
    show_2d(v)
