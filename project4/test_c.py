import numpy as np
from common import *

L = 2
spin = np.ones(shape=(L, L), dtype=np.int8)
J = 1
T = 1

mc_cycles = int(2E7)
energy, mean_magnetization, accepted_configurations, time_spent = metropolis_c(spin, J, T, mc_cycles)
print "Energy: %g" % energy
print "Analytical Energy %g" % (analytical_energy(J, T))
print "Mean magnetization: %g" % mean_magnetization
print "Accepted configurations: %g" % accepted_configurations
#print spin

show_spins(spin)
