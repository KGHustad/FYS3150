from common import *
from plotting import *


# Divergence of schemes for declining dt
n = 10
T = 1.0

# N_values = np.linspace(5,100,94)
N_values = np.linspace(200,1000,1000)
# N_values = np.array([5,6,7,8,9,10,15,20,25,30,40,50,60,70,80,90,100,200,300,400,500,1000,1500,2000])
N_values = np.array(N_values,dtype=int)

FE_error = np.zeros(len(N_values))
BE_error = np.zeros(len(N_values))
CN_error = np.zeros(len(N_values))

dt = T/N_values

x = np.linspace(0,1,n+2)
u = analytical_u_1d(x,0)
analytical = analytical_u_1d(x,T)
dx = 1./n

for solver, array in zip(SOLVERS_1D, (FE_error, BE_error, CN_error)):
    for i, N in enumerate(N_values):
        kappa = float(dt[i])/dx**2
        v = u.copy()
        diffusion_1d(v, N, kappa, solver, silent=True)
        difference = analytical - v
        max_error = np.max(np.abs(difference))
        array[i] = max_error

plt.plot(dt, FE_error)
plt.title("Max Error in Forward Euler as function of dt-length")
plt.xlabel("dt")
plt.ylabel("Absolute Error")
plt.show()

plt.plot(dt, BE_error)
plt.title("Max Error in Bacward Euler as function of dt-length")
plt.xlabel("dt")
plt.ylabel("Absolute Error")
plt.show()

plt.plot(dt, CN_error)
plt.title("Max Error in Crank-Nicolson as function of dt-length")
plt.xlabel("dt")
plt.ylabel("Absolute Error")
plt.show()
