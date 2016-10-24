from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np

for i in range(4):
    MySolarSystem = SolarSystem()
    MySolarSystem.CreateCelestialObject(0,0, 0,0, 1) #Sun
    MySolarSystem.CreateCelestialObject(1,0, 0,(2.7+0.05*i)*np.pi, 3.003e-6)
    p, v = MySolarSystem.fill_array_c(int(1e3), 100, skip_saving=1000)
    plt.axis([-60,20,-20,40])
    plt.axes(aspect='equal')
    plt.plot(p[:,1,0], p[:,1,1], "-")
plt.title("Testing velocities in Earth Sun system")
plt.xlabel("AU")
plt.ylabel("AU")
plt.plot(p[:,0,0], p[:,0,1], "yo")
plt.legend(["Planet1, v = 2.7$\pi$","Planet2, v = 2.75$\pi$","Planet3 v = 2.80$\pi$", "Planet4, v = 2.85$\pi$","Sun"])
plt.savefig("fig/escape_velocity.pdf")
plt.show()
