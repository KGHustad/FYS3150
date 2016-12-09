from common import *
from plotting import *

def stable_dt(dx):
    #Returns a time interval for a given space interval that is stable with Forward Euler
    return 0.5*dx**2

def stable_N(n):
    #Returns a stable N from a given n for Forward Euler
    return 2*n**2

#Plots for the 0 initial conditions
for n in [10,100]:
    for T in [0.05,0.1,0.5]:
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

        # plt.rc('font', **{'size' : 14})
        # plt.tight_layout()
        plt.title("1D case after T=%.2f, with dx=%.2f and dt=%.5f" % (T,dx,dt))
        plt.xlabel("x")
        plt.ylabel("u(x,t)")
        plt.legend(loc='best')
        plt.savefig("fig/1D_linplot_T=%.2fdx=%.2f.pdf" % (T,dx))
        plt.clf()


#Plot showing the divergence of only the Crank-Nicolson scheme for different T values
for T in [0.01,0.03,0.1,0.3,1]:
    N = stable_N(n)
    dx = 1./n
    dt = T/float(N)
    kappa = dt/dx**2
    print "dx: %g  dt: %g  kappa: %g" % (dx, dt, kappa)
    u = np.zeros(n+2)
    u[-1] = 1

    v = u.copy()
    diffusion_1d(v, N, kappa, "crank_nicolson")


    x = np.linspace(0, 1, n+2)
    plt.plot(x, v, label = "T = %.2f" % T )

# plt.rc('font', **{'size' : 14})
# plt.tight_layout()
plt.title("Divergence of Crank-Nicolson over time")
plt.xlabel("x")
plt.ylabel("u(x,t)")
plt.legend(loc='best')
plt.savefig("fig/1D_linplot_Crank_nicolson.pdf")
plt.clf()
