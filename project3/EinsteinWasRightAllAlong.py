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

p_newton, v_newton = MySolarSystem.fill_array_c(100000, 100)

p_einstein, v_einstein = MySolarSystem.fill_array_c(100000, 100, acc_method=MySolarSystem.AccRelativistic)



local_min_indexes = scipy.signal.argrelextrema(np.linalg.norm(p_newton[:,1],axis=1),np.less)[0]
perihelion_angle = np.zeros(len(local_min_indexes))
for i in range(len(local_min_indexes)):
    perihelion_angle[i] = np.arctan( p_newton[local_min_indexes[i],1,1] / p_newton[local_min_indexes[i],1,0] )
plt.plot(perihelion_angle)

local_min_indexes = scipy.signal.argrelextrema(np.linalg.norm(p_newton[:,1],axis=1),np.less)[0]
perihelion_angle = np.zeros(len(local_min_indexes))
for i in range(len(local_min_indexes)):
    perihelion_angle[i] = np.arctan( p_einstein[local_min_indexes[i],1,1] / p_einstein[local_min_indexes[i],1,0] )
plt.plot(perihelion_angle)
plt.show()


plt.axes(aspect='equal')
plt.plot(p_newton[:,0,0], p_newton[:,0,1], "yo")
plt.plot(p_newton[99800:,1,0], p_newton[99800:,1,1], "r-")
plt.plot(p_einstein[99800:,1,0], p_einstein[99800:,1,1], "b-")
plt.plot(p_newton[-1,1,0], p_newton[-1,1,1], "ro")
plt.plot(p_einstein[-1,1,0], p_einstein[-1,1,1], "bo")
plt.plot()
plt.show()
