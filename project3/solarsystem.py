from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter

masses = { 'mercury' : 0.166e-6, 'venus' : 2.081e-6, 'earth' : 3.003e-6, 'mars' : 0.323e-6, 'jupiter' : 954.7e-6, 'saturn' : 285.8e-6, 'uranus' : 43.6e-6, 'neptune' : 51.5e-6}

distances = { 'mercury' : 0.39, 'venus' : 0.72, 'earth' : 1, 'mars' : 1.52, 'jupiter' : 5.20, 'saturn' : 9.58, 'uranus' : 19.23, 'neptune' : 30.10}

speeds_kms = { 'mercury' : 47.4, 'venus' : 35.0, 'earth' : 29.8, 'mars' : 24.1, 'jupiter' : 13.1, 'saturn' : 9.7, 'uranus' : 6.8, 'neptune' : 5.4}

speeds = {key: speeds_kms[key]*0.210805 for key in speeds_kms}

MySolarSystem = SolarSystem()
MySolarSystem.CreateCelestialObject(0, 0, 0, 0, 1)
bodies = ['sun']

# sort planets after distance
body_dist = [(key, distances[key]) for key in distances]
sorted_bodies = [item[0] for item in sorted(body_dist, key=itemgetter(1))]

for key in sorted_bodies:
    MySolarSystem.CreateCelestialObject(distances[key], 0, 0, speeds[key], masses[key])
    bodies.append(key)

#p, v = MySolarSystem.FillArray(10000, 100, int_method = MySolarSystem.ForwardEuler, acc_method = MySolarSystem.AccRelativistic)

#p, v = MySolarSystem.FillArray(4, 1E-2, int_method = MySolarSystem.ForwardEuler, acc_method = MySolarSystem.Acc)
#p, v = MySolarSystem.FillArray(20000, 100, int_method = MySolarSystem.VelocityVerlet, acc_method = MySolarSystem.Acc)
p, v = MySolarSystem.fill_array_c(20000, 100, int_method = MySolarSystem.VelocityVerlet, acc_method = MySolarSystem.Acc)

"""
print "\nInitial values:"
print p[0]
print v[0]

print "\nAfter first step:"
print p[1]
print v[1]

print "\nAfter second step:"
print p[2]
print v[2]
"""

print "\nSun development:"
print p[:,0]
print v[:,0]

#"""
plt.axes(aspect='equal')
for i in range(len(masses)+1):
    plt.plot(p[:,i,0], p[:,i,1])
#plt.axis([-10,10,-10,10])
plt.legend(bodies)
plt.show()
#"""
