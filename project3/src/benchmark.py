from common import SolarSystem
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter

masses = { 'mercury' : 0.166e-6, 'venus' : 2.081e-6, 'earth' : 3.003e-6, 'mars' : 0.323e-6, 'jupiter' : 954.7e-6, 'saturn' : 285.8e-6, 'uranus' : 43.6e-6, 'neptune' : 51.5e-6}

distances = { 'mercury' : 0.39, 'venus' : 0.72, 'earth' : 1, 'mars' : 1.52, 'jupiter' : 5.20, 'saturn' : 9.58, 'uranus' : 19.23, 'neptune' : 30.10}

speeds_kms = { 'mercury' : 47.4, 'venus' : 35.0, 'earth' : 29.8, 'mars' : 24.1, 'jupiter' : 13.1, 'saturn' : 9.7, 'uranus' : 6.8, 'neptune' : 5.4}

speeds = {key: speeds_kms[key]*0.210805 for key in speeds_kms}

ss = SolarSystem()
ss.CreateCelestialObject(0, 0, 0, 0, 1)
bodies = ['sun']

# sort planets after distance
body_dist = [(key, distances[key]) for key in distances]
sorted_bodies = [item[0] for item in sorted(body_dist, key=itemgetter(1))]

for key in sorted_bodies:
    ss.CreateCelestialObject(distances[key], 0, 0, speeds[key], masses[key])
    bodies.append(key)


for int_alg, int_str in [(ss.ForwardEuler, "Forward Euler"),
                          (ss.VelocityVerlet, "Velocity Verlet")]:
    for acc_alg, acc_str in [(ss.Acc, "Classical acc."),
                             (ss.AccRelativistic, "Relativistic acc.")]:

        p, v, time_spent = ss.fill_array_c(int(1E6), 100,
                                           int_method = int_alg,
                                           acc_method = acc_alg,
                                           silent=True, benchmark=True)
        print("%8g s with  %15s  AND  %20s" % (time_spent, int_str, acc_str))
