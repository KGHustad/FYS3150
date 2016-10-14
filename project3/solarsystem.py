from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np

KGtoSM = 5.02785431e-31
KMtoAU = 6.68459e-9

jupiterdistance = np.sqrt(5.429091121847574**2 + 0.446412185703396**2 + 0.1232706724471818**2)
jupiterspeed = np.sqrt( (5.310921442239308e-4*365.2422)**2 + (7.163232763813381e-3*365.2422)**2 + (1.792277878205211e-5*365.2422)**2 )

earthmass = 5.97219*10**24*KGtoSM

MySolarSystem = SolarSystem()

MySolarSystem.CreateCelestialObject(0, 0, 0, 0, 1, 1)
MySolarSystem.CreateCelestialObject(1, 0, 0, 2*np.pi, earthmass, 1)
MySolarSystem.CreateCelestialObject(jupiterdistance, 0, 0, jupiterspeed, 1898.13*KGtoSM, 1) #Jupiter
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
"""
