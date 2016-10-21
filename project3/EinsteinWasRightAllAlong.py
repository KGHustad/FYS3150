from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np

mercurymass = 0.166e-6
mercuryspeed = 12.44
mercurydistance = 0.3075

MySolarSystem = SolarSystem()
MySolarSystem.CreateCelestialObject(0, 0, 0, 0, 1)
MySolarSystem.CreateCelestialObject(mercurydistance, 0, 0, mercuryspeed, mercurymass)

p_newton, v_newton = MySolarSystem.fill_array_c(100000, 100)

p_einstein, v_einstein = MySolarSystem.fill_array_c(100000, 100, acc_method=MySolarSystem.AccRelativistic)


plt.axes(aspect='equal')
plt.plot(p_newton[:,0,0], p_newton[:,0,1], "yo")
plt.plot(p_newton[99900:,1,0], p_newton[99900:,1,1], "r-")
plt.plot(p_einstein[99900:,1,0], p_einstein[99900:,1,1], "b-")
plt.plot(p_newton[-1,1,0], p_newton[-1,1,1], "ro")
plt.plot(p_einstein[-1,1,0], p_einstein[-1,1,1], "bo")
plt.show()
