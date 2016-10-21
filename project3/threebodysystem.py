from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np

MySolarSystem = SolarSystem()
MySolarSystem.CreateCelestialObject(0, 0, 0, 0, 1) #Sun
MySolarSystem.CreateCelestialObject(1, 0, 0, 29.8*0.210805, 3.003e-6) #Earth
MySolarSystem.CreateCelestialObject(5.20, 0, 0, 13.1*0.210805, 954.7e-6*1000) #Jupiter

p, v = MySolarSystem.fill_array_c(40000000, 3.5)

#plt.axes(aspect='equal')
plt.plot(p[:,0,0], p[:,0,1], "y-")
plt.plot(p[:,1,0], p[:,1,1], "r-")
plt.plot(p[:,2,0], p[:,2,1], "b-")
#plt.axis([-10,15,-10,30])
plt.show()
