from common import *
from plotting import *

def stable_dt(dx):
    #Returns a time interval for a given space interval that is stable with Forward Euler
    return 0.5*dx**2

def stable_N(n):
    #Returns a stable N from a given n for Forward Euler
    return 2*n**2

for n in [10,100]:
    for T in [0.05,0.5]:
        N = stable_N(n)
        dx = 1./n
        dt = T/float(N)
        kappa = dt/dx**2
        print "dx: %g  dt: %g  kappa: %g" % (dx, dt, kappa)
        u = np.zeros(n+2)
        u[-1] = 1

        for solver in SOLVERS_1D:
            v = u.copy()
            diffusion_1d(v, N, kappa, solver)
            print "Solver: %s" % solver
            print v
            print

            x = np.linspace(0, 1, n+2)
            plt.plot(x, v, label=solver)

        plt.plot(x, analytical_solution)
        plt.rc('font', **{'size' : 14})
        plt.tight_layout()
        plt.title("1D case after T=%.2f, with dx=%.2f and dt=%.5f" % (T,dx,dt))
        plt.xlabel("x")
        plt.ylabel("u(x,t)")
        plt.legend(loc='best')
        plt.show()
