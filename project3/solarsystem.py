from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np

KGtoSM = 5.02785431e-31
KMtoAU = 6.68459e-9


MySolarSystem = SolarSystem()
"""
MySolarSystem.CreateCelestialObject(0, 0, 0, 0, 1, 1)
MySolarSystem.CreateCelestialObject(1, 0, 0, 2.8*np.pi, 0.0000001, 1)
MySolarSystem.CreateCelestialObject(0, 4, np.pi, 0, 1898.13*KGtoAU, 1) #Jupiter
p, v = MySolarSystem.FillArray(20000, 200)

plt.axes(aspect='equal')
plt.plot(p[:,0,0], p[:,0,1], "yo")
plt.plot(p[:,1,0], p[:,1,1], "r-")
plt.plot(p[:,2,0], p[:,2,1], "b-")
#plt.axis([-2,2,-2,2])
plt.show()
"""
MySolarSystem.EnergyConservation_test()

MySolarSystem.TimeStep_test()
