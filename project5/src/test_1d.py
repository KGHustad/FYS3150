from common import *
from plotting import *

n = int(4)
N = int(1000)
T = 1

dx = 1./n
dt = T/float(N)

kappa = dt/dx**2

print "dx: %g  dt: %g  kappa: %g" % (dx, dt, kappa)

u = np.zeros(n+2)
u[-1] = 1



print u

for solver in SOLVERS_1D:
    v = u.copy()
    diffusion_1d(v, N, kappa, solver)
    print "Solver: %s" % solver
    print v
    print

    x = np.linspace(0, 1, n+2)
    plt.plot(x, v, label=solver)

plt.legend(loc='best')
plt.show()
