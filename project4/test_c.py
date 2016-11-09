import numpy as np
from common import *

L = 20
spin = np.ones(shape=(L, L), dtype=np.int8)
J = 1
T = 1

mc_cycles = int(2E7)
energy, mean_magnetization, accepted_configurations, time_spent = metropolis_c(spin, J, T, mc_cycles)
print "Energy: %g" % energy
print "Mean magnetization: %g" % mean_magnetization
print "Accepted configurations: %g" % accepted_configurations
#print spin

show_spins(spin)
