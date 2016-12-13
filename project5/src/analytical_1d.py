from common import *
from plotting import *

def stable_dt(dx):
    #Returns a time interval for a given space interval that is stable with Forward Euler
    return 0.5*dx**2

def stable_N(n):
    #Returns a stable N from a given n for Forward Euler
    return 2*n**2


#Plots for the sinus initial conditions against analytical:
for T in [0.1,1]:
    for solver in SOLVERS_1D:
        for n in [10,100]:
            N = stable_N(n)
            dx = 1./n
            dt = T/float(N)
            kappa = dt/dx**2
            print "dx: %g  dt: %g  kappa: %g" % (dx, dt, kappa)
            x = np.linspace(0, 1, n+2)
            analytical_solution = analytical_u_1d(x,T)
            u = analytical_u_1d(x,0)

            v = u.copy()
            diffusion_1d(v, N, kappa, solver)
            print "Solver: %s" % solver
            print v
            print
            plt.plot(x, v, label=solver_abbreviation[solver] + " $\\Delta x=%.2f$" % (dx))

    plt.plot(x, analytical_solution, label="exact")
    # plt.rc('font', **{'size' : 14})
    # plt.tight_layout()
    plt.title("1D case simulated for T=%.2f" % (T))
    plt.xlabel("x")
    plt.ylabel("u(x,t)")
    plt.legend(loc='best')
    plt.savefig(get_fig_dir() + "/plot_T=%.2f.pdf" % (T))
    plt.show()
    plt.clf()


#Absolute error plots:
for n in [10,100]:
    for T in [0.1,1]:
        N = stable_N(n)
        dx = 1./n
        dt = T/float(N)
        kappa = dt/dx**2
        print "dx: %g  dt: %g  kappa: %g" % (dx, dt, kappa)
        x = np.linspace(0, 1, n+2)

        analytical_solution = analytical_u_1d(x,T)
        u = analytical_u_1d(x,0)

        for solver in SOLVERS_1D:
            v = u.copy()
            diffusion_1d(v, N, kappa, solver)
            print "Solver: %s" % solver
            print v
            print
            error = abs(analytical_solution - v)
            plt.plot(x, error, label=solver)


        # plt.rc('font', **{'size' : 14})
        # plt.tight_layout()
        plt.title("Absolute error after T=%.2f, with dx=%.2f and dt=%.5f" % (T,dx,dt))
        plt.xlabel("x")
        plt.ylabel("u(x,t)")
        plt.legend(loc='best')
        plt.savefig(get_fig_dir() + "/error_T=%.2fn=%d.pdf" % (T,n))
        plt.clf()
