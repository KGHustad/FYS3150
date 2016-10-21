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

p_newton, v_newton = MySolarSystem.fill_array_c(30000000, 100)

p_einstein, v_einstein = MySolarSystem.fill_array_c(30000000, 100, acc_method=MySolarSystem.AccRelativistic)



local_min_indexes = scipy.signal.argrelextrema( np.sqrt((p_newton[:,1,0] - p_newton[:,0,0])**2 + (p_newton[:,1,1] - p_newton[:,0,1])**2), np.less )[0]
perihelion_points = np.zeros(shape=(len(local_min_indexes),2))
perihelion_angle = np.zeros(len(local_min_indexes))
for i in range(len(local_min_indexes)):
    perihelion_points[i] = p_newton[local_min_indexes[i],1]
    perihelion_angle[i] = np.arctan( p_newton[local_min_indexes[i],1,1] / p_newton[local_min_indexes[i],1,0] )
plt.plot(perihelion_angle, "r-")

local_min_indexes = scipy.signal.argrelextrema(np.linalg.norm(p_newton[:,1],axis=1),np.less)[0]
perihelion_angle = np.zeros(shape=(len(local_min_indexes),2))
for i in range(len(local_min_indexes)):
    perihelion_points[i] = p_einstein[local_min_indexes[i],1]
    perihelion_angle[i] = np.arctan( p_einstein[local_min_indexes[i],1,1] / p_einstein[local_min_indexes[i],1,0] )
plt.plot(perihelion_angle, "b-")
plt.show()


plt.axes(aspect='equal')
plt.plot(0,0, "yo")
plt.plot(p_newton[::100,1,0], p_newton[::100,1,1], "r-")
plt.plot(p_einstein[::100,1,0], p_einstein[::100,1,1], "b-")
plt.plot(p_newton[-1,1,0], p_newton[-1,1,1], "ro")
plt.plot(p_einstein[-1,1,0], p_einstein[-1,1,1], "bo")
plt.plot(p_newton[local_min_indexes[-1],1,0], p_newton[local_min_indexes[-1],1,1], "ko")
# plt.plot(perihelion_points[::100,0], perihelion_points[::100,1], "ko")
plt.show()
