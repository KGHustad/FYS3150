from common import SolarSystem
import matplotlib.pyplot as plt

MySolarSystem = SolarSystem()

MySolarSystem.CreateCelestialObject(0, 0, 0, 0, 1, 0.1)
MySolarSystem.CreateCelestialObject(1, 1, 0, 0, 0.001, 0.0001)

p = MySolarSystem.FillArray(10, 0.00001)

plt.plot(p[:,0], p[:,1], "ro")
plt.axis([-3,3,-3,3])
plt.show()
