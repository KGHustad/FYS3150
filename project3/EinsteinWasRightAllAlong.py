from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal
import math

mercurymass = 0.166e-6
mercuryspeed = 12.44
mercury_perihelion_distance = 0.3075

MySolarSystem = SolarSystem()
MySolarSystem.CreateCelestialObject(0, 0, 0, 0, 1)
MySolarSystem.CreateCelestialObject(mercury_perihelion_distance, 0, 0, mercuryspeed, mercurymass)

p_newton, v_newton = MySolarSystem.fill_array_c(10000000, 100, skip_saving=10)

p_einstein, v_einstein = MySolarSystem.fill_array_c(10000000, 100, acc_method=MySolarSystem.AccRelativistic, skip_saving=10)



local_min_indexes = scipy.signal.argrelextrema( np.sqrt((p_newton[:,1,0] - p_newton[:,0,0])**2 + (p_newton[:,1,1] - p_newton[:,0,1])**2), np.less )[0]
perihelion_points_newton = np.zeros(shape=(len(local_min_indexes),2))
perihelion_angle_newton = np.zeros(len(local_min_indexes))
for i in range(len(local_min_indexes)):
    perihelion_points_newton[i] = p_newton[local_min_indexes[i],1]
    perihelion_angle_newton[i] = np.arctan( p_newton[local_min_indexes[i],1,1] / p_newton[local_min_indexes[i],1,0] )
plt.plot(perihelion_angle_newton, "r-")

local_min_indexes = scipy.signal.argrelextrema(np.linalg.norm(p_newton[:,1],axis=1),np.less)[0]
perihelion_angle_einstein = np.zeros(len(local_min_indexes))
perihelion_points_einstein = np.zeros(shape=(len(local_min_indexes),2))
for i in range(len(local_min_indexes)):
    perihelion_points_einstein[i] = p_einstein[local_min_indexes[i],1]
    perihelion_angle_einstein[i] = np.arctan( p_einstein[local_min_indexes[i],1,1] / p_einstein[local_min_indexes[i],1,0] )
plt.plot(perihelion_angle_einstein, "b-")
plt.show()

plt.axes(aspect='equal')
plt.plot(0,0, "yo")
plt.plot(p_newton[::100,1,0], p_newton[::100,1,1], "r-")
plt.plot(p_einstein[::100,1,0], p_einstein[::100,1,1], "b-")
plt.plot(p_newton[-1,1,0], p_newton[-1,1,1], "ro")
plt.plot(p_einstein[-1,1,0], p_einstein[-1,1,1], "bo")
plt.plot(perihelion_points_einstein[:,0], perihelion_points_einstein[:,1], "ko")
plt.show()

print perihelion_points_newton[0]
print perihelion_points_newton[-1]
print perihelion_angle_newton[-1]
print perihelion_points_einstein[0]
print perihelion_points_einstein[-1]
print perihelion_angle_einstein[-1]
