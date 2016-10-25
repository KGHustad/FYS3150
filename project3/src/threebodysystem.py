from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np

MySolarSystem = SolarSystem()
MySolarSystem.CreateCelestialObject(0, 0, 0, 0, 1) #Sun
MySolarSystem.CreateCelestialObject(1, 0, 0, 29.8*0.210805, 3.003e-6, adjust_sun=False) #Earth
MySolarSystem.CreateCelestialObject(5.20, 0, 0, 13.1*0.210805, 954.7e-6*1000, adjust_sun=False) #Jupiter

p, v = MySolarSystem.fill_array_c(int(1e6), 3)

plt.axes(aspect='equal')
plt.plot(p[:,0,0], p[:,0,1], "y-")
plt.plot(p[:,1,0], p[:,1,1], "b-")
plt.plot(p[:,2,0], p[:,2,1], "r-")
plt.plot(p[0,0,0], p[0,0,1], "yx")
plt.plot(p[-1,0,0], p[-1,0,1], "yo")
plt.plot(p[0,2,0], p[0,2,1], "rx")
plt.plot(p[-1,2,0], p[-1,2,1], "ro")
plt.plot(p[0,1,0], p[0,1,1], "bx")
plt.plot(p[-1,1,0], p[-1,1,1], "bo")
plt.axis([-2,7,-2,7])
plt.title("Sun-Earth-Jupiter system over 3 years")
plt.legend(["Sun", "Earth", "Jupiter"])
plt.show()

MySolarSystem = SolarSystem()
MySolarSystem.CreateCelestialObject(0, 0, 0, 0, 1) #Sun
MySolarSystem.CreateCelestialObject(1, 0, 0, 29.8*0.210805, 3.003e-6, adjust_sun=False) #Earth
MySolarSystem.CreateCelestialObject(5.20, 0, 0, 13.1*0.210805, 954.7e-6*10, adjust_sun=False) #Jupiter

p, v = MySolarSystem.fill_array_c(int(1e6), 3)

plt.axes(aspect='equal')
plt.plot(p[:,0,0], p[:,0,1], "y-")
plt.plot(p[:,1,0], p[:,1,1], "b-")
plt.plot(p[:,2,0], p[:,2,1], "r-")
plt.plot(p[0,0,0], p[0,0,1], "yx")
plt.plot(p[-1,0,0], p[-1,0,1], "yo")
plt.plot(p[0,2,0], p[0,2,1], "rx")
plt.plot(p[-1,2,0], p[-1,2,1], "ro")
plt.plot(p[0,1,0], p[0,1,1], "bx")
plt.plot(p[-1,1,0], p[-1,1,1], "bo")
plt.axis([-2,7,-2,7])
plt.title("Sun-Earth-Jupiter system over 3 years")
plt.legend(["Sun", "Earth", "Jupiter"])
plt.show()
