import numpy as np
from common import *

L = 2
spin = np.ones(shape=(L, L), dtype=np.int8)
spin = random_spin_matrix(L)
J = 1
T = 1
save_every_nth = 1

show_spins(spin)

mc_cycles = int(1E5)
energies, mean_magnetization, accepted_configurations, time_spent = metropolis_c(spin, J, T, mc_cycles, save_every_nth=save_every_nth)
mu_E, mu_M, mu_abs_M, mu_E_sq, mu_M_sq = extract_expectation_values(energies, mean_magnetization)

print mu_E, mu_M, mu_abs_M, mu_E_sq, mu_M_sq

print len(energies)

print energies
print mean_magnetization

exact_energy = analytical_energy(J, T)

print "Mean energy:         %8g" % mu_E
print "Analytical Energy:   %8g" % exact_energy
print "Energy error:        %8g" % ((mu_E - exact_energy)/exact_energy)
print "Mean magnetization:  %8g" % mu_M
print "Accepted configurations: %g" % accepted_configurations
#print spin

show_spins(spin)

expectation_value_for_energy = np.cumsum(energies[1:]) / np.arange(1, (mc_cycles/save_every_nth+1))
plt.plot(expectation_value_for_energy)
#plt.ylim(-8.1, -7.9)
plt.show()
