from common import *
from plotting import *
import sys

show = True
if '--no_show' in sys.argv:
    show = False

iterations = int(1E5)

width = 100
height = width
kappa = 1E-2

dx = 1./width
dt = kappa*dx**2
T = dt*iterations

figdir = get_fig_dir()

v = np.zeros((height, width), dtype=np.float64)

v[:,-1] = 1

diffusion_2d(v, iterations, kappa)
#print v
title ="$T = %g$,  $\\Delta t=%f$" % (T, dt)
print title
show_2d(v, title=title,
        save_to=figdir+"/plot_2d_all_dirichlet.pdf", show=show)



# linear, isolated top and bottom
v = np.zeros((height, width), dtype=np.float64)
v[:,-1] = 1
diffusion_2d(v, iterations, kappa, bc_left=0, bc_top=1, bc_bottom=1, bc_right=0)
show_2d(v, save_to=figdir+"/plot_2d_dirichlet_x_and_neumann_y.pdf", show=show)
