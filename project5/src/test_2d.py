from common import *
from plotting import *

iterations = int(1E4)

height = 20
width = 20
kappa = 1E-2

v = np.zeros((height, width), dtype=np.float64)
f = np.zeros((height, width), dtype=np.float64)

v[:,-1] = 1

diffusion_2d(v, f, iterations, kappa, bc_left=1, bc_top=1, bc_bottom=1)
#print v

show_2d(v)
