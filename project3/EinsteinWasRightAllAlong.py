from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np

mercurymass = 0.166e-6
mercuryspeed = 47.4*0.210805
mercurydistance = 0.39

MySolarSystem = SolarSystem()
MySolarSystem.CreateCelestialObject(0, 0, 0, 0, 1, 1)
MySolarSystem.CreateCelestialObject(mercurydistance, 0, 0, mercuryspeed, mercurymass, 1)

p, v = MySolarSystem.FillArray(20000, 100)

plt.axes(aspect='equal')
plt.plot(p[:,0,0], p[:,0,1], "yo")
plt.plot(p[:,1,0], p[:,1,1], "r-")
plt.show()
