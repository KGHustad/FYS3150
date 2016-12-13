from common import *
from plotting import *


# Divergence of schemes for declining dx
N = 20000
T = 1.0

# N_values = np.linspace(5,100,94)
n_values = np.linspace(10,100,91)
# N_values = np.array([5,6,7,8,9,10,15,20,25,30,40,50,60,70,80,90,100,200,300,400,500,1000,1500,2000])

FE_error = np.zeros(len(n_values))
BE_error = np.zeros(len(n_values))
CN_error = np.zeros(len(n_values))

dt = T/N

x = np.linspace(0,1,len(n_values)+2)
u = analytical_u_1d(x,0)
analytical = analytical_u_1d(x,T)
dx = 1./n_values

for solver, array in zip(SOLVERS_1D, (FE_error, BE_error, CN_error)):
    for i, n in enumerate(n_values):
        kappa = float(dt)/dx[i]**2
        v = u.copy()
        diffusion_1d(v, N, kappa, solver, silent=True)
        difference = analytical - v
        max_error = np.max(np.abs(difference))
        array[i] = max_error

plt.plot(dx, FE_error)
plt.title("Max Error in Forward Euler as function of dx-length")
plt.xlabel("dx")
plt.ylabel("Absolute Error")
plt.show()

plt.plot(dx, BE_error)
plt.title("Max Error in Bacward Euler as function of dx-length")
plt.xlabel("dx")
plt.ylabel("Absolute Error")
plt.show()

plt.plot(dx, CN_error)
plt.title("Max Error in Crank-Nicolson as function of dx-length")
plt.xlabel("dx")
plt.ylabel("Absolute Error")
plt.show()
