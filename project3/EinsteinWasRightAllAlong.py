from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
import math

def find_perihelion(pos_star, pos_celbody):
    dist = np.linalg.norm(pos_star - pos_celbody, axis=1)
    local_minima_indices = scipy.signal.argrelmin(dist)
    pos_minima = pos_celbody[local_minima_indices]
    angles = np.arctan(pos_minima[:,1] /  pos_minima[:,0])
    return pos_minima, angles, local_minima_indices

mercurymass = 0.166e-6
mercuryspeed = 12.44
mercury_perihelion_distance = 0.3075

MySolarSystem = SolarSystem()
MySolarSystem.CreateCelestialObject(0, 0, 0, 0, 1)
MySolarSystem.CreateCelestialObject(mercury_perihelion_distance, 0, 0, mercuryspeed, mercurymass)

N = int(1e8)    # total time steps stored
years = 100
time_steps = np.linspace(0, years, N+1)


# newton
p_newton, v_newton = MySolarSystem.fill_array_c(N, years, skip_saving=1
)
v_newton = None # allow for garbage collection
res_newton = find_perihelion(p_newton[:,0,:], p_newton[:,1,:])
points_newton, angles_newton, indices_newton = res_newton


# einstein
p_einstein, v_einstein = MySolarSystem.fill_array_c(N, years, acc_method=MySolarSystem.AccRelativistic, skip_saving=1
)
v_einstein = None # allow for garbage collection
res_einstein = find_perihelion(p_einstein[:,0,:], p_einstein[:,1,:])
points_einstein, angles_einstein, indices_einstein = res_einstein


plt.plot(time_steps[indices_newton], angles_newton)
plt.plot(time_steps[indices_einstein], angles_einstein)


plt.title("Change in perihelion angle over a century")
plt.legend(["Classical Mechanics case", "Relativistic case"])
plt.xlabel("time in years")
plt.ylabel("angle in radians")
plt.show()

plt.axes(aspect='equal')
plt.plot(0,0, "yo")
plt.plot(p_newton[::100,1,0], p_newton[::100,1,1], "r-")
plt.plot(p_einstein[::100,1,0], p_einstein[::100,1,1], "b-")
plt.plot(p_newton[-1,1,0], p_newton[-1,1,1], "ro")
plt.plot(p_einstein[-1,1,0], p_einstein[-1,1,1], "bo")
plt.plot(points_einstein[:,0], points_einstein[:,1], "ko")
plt.show()

print points_newton[0]
print points_newton[-1]
print angles_newton[-1]
print points_einstein[0]
print points_einstein[-1]
print angles_einstein[-1]
