from common import *
from plotting import *

n = 100

T = 0.01
x = np.linspace(0, 1, n+2)
analytical = analytical_u_1d(x,T)

alpha_values = np.linspace(0.1, 1.0, 10)

FE_error = np.zeros(len(alpha_values))
BE_error = np.zeros(len(alpha_values))
CN_error = np.zeros(len(alpha_values))


dx = x[1] - x[0]
for solver, array in zip(SOLVERS_1D, (FE_error, BE_error, CN_error)):
    for i, alpha in enumerate(alpha_values):
        x = np.linspace(0, 1, n+2)
        v = analytical_u_1d(x, 0)
        dt = alpha * dx**2
        iterations = int(T / dt)
        print iterations
        diffusion_1d(v, iterations, alpha, solver)
        difference = analytical - v
        max_error = np.max(np.abs(difference))
        array[i] = max_error

print FE_error

plt.semilogy(alpha_values, FE_error, label='FE')
plt.semilogy(alpha_values, BE_error, label='BE')
plt.semilogy(alpha_values, CN_error, label='CN')
plt.legend(loc='best')
plt.xlabel('$\\alpha$')
plt.ylabel('error')
plt.savefig(get_fig_dir()+'/plot_stability_1d.pdf'
)
plt.show()
