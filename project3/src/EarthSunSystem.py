from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np

MySolarSystem = SolarSystem()
MySolarSystem.CreateCelestialObject(0,0, 0,0, 1) #Sun
MySolarSystem.CreateCelestialObject(1,0, 0,2*np.pi, 3.003e-6) #Earth

p, v = MySolarSystem.fill_array_c(int(1e6), 5.5)
plt.axes(aspect="equal")
plt.plot(p[:,0,0], p[:,0,1], "yo")
plt.plot(p[:,1,0], p[:,1,1], "b-")
plt.plot(p[0,1,0], p[0,1,1], "bx")
plt.plot(p[-1,1,0], p[-1,1,1], "bo")
plt.axis([-1.2,1.2,-1.2,1.2])
plt.title("Earth Sun system over 5.5 years")
plt.legend(["Sun","Earth"])
plt.xlabel("AU")
plt.ylabel("AU")
plt.show()
