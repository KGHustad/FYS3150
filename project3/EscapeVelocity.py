from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np

for i in range(4):
    MySolarSystem = SolarSystem()
    MySolarSystem.CreateCelestialObject(0,0, 0,0, 1) #Sun
    MySolarSystem.CreateCelestialObject(1,0, 0,(2.65+0.05*i)*np.pi, 3.003e-6)
    p, v = MySolarSystem.fill_array_c(int(1e6), 20)
    plt.axis([-25,10,-15,20])
    plt.axes(aspect='equal')
    plt.plot(p[:,1,0], p[:,1,1], "-")
plt.title("Testing velocities in Earth Sun system")
plt.xlabel("AU")
plt.ylabel("AU")
plt.plot(p[:,0,0], p[:,0,1], "yo")
plt.legend(["Planet1, v = 2.6","Planet2, v = 2.65","Planet3 v = 2.7", "Planet4, v = 2.75","Sun"])
plt.show()
