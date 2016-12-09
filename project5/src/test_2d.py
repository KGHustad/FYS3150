from common import *
from plotting import *

iterations = int(1E4)

height = 400
width = 400
kappa = 1E-2

v = np.zeros((height, width), dtype=np.float64)

v[:,-1] = 1

diffusion_2d(v, iterations, kappa, bc_left=1, bc_top=1, bc_bottom=1)
#print v

show_2d(v)



# uniform spread
v = np.zeros((height, width), dtype=np.float64)

uniform = np.linspace(0, 1, width)
v[:] = uniform[:]
diffusion_2d(v, iterations, kappa, bc_left=1, bc_top=1, bc_bottom=1, bc_right=1)
show_2d(v)
