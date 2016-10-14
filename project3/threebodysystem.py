from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np

MySolarSystem = SolarSystem()
MySolarSystem.CreateCelestialObject(0, 0, 0, 0, 1) #Sun
MySolarSystem.CreateCelestialObject(1, 0, 0, 29.8*0.210805, 3.003e-6) #Earth
MySolarSystem.CreateCelestialObject(5.20, 0, 0, 13.1*0.210805, 954.7e-6) #Jupiter

p, v = MySolarSystem.FillArray(20000, 10)

plt.axes(aspect='equal')
plt.plot(p[:,0,0], p[:,0,1], "yo")
plt.plot(p[:,1,0], p[:,1,1], "r-")
plt.plot(p[:,2,0], p[:,2,1], "b-")
plt.show()
