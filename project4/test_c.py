import numpy as np
from common import *

seed = 3150

L = 2
spin = np.ones(shape=(L, L), dtype=np.int8)
spin = random_spin_matrix(L, seed=seed)
J = 1
T = 1
save_every_nth = 1

#show_spins(spin)

mc_cycles = int(1E7)
energies, mean_magnetization, accepted_configurations, time_spent = metropolis_c(spin, J, T, mc_cycles, save_every_nth=save_every_nth, seed=seed)
mu_E, mu_M, mu_abs_M, mu_E_sq, mu_M_sq = extract_expectation_values(energies, mean_magnetization)

print mu_E, mu_M, mu_abs_M, mu_E_sq, mu_M_sq


exact_mean_energy = analytical_mean_energy(J, T)
exact_mean_energy_sq = analytical_mean_energy_squared(J, T)
exact_mean_abs_magnetization = analytical_mean_abs_magnetization(J, T)
exact_mean_magnetization_sq = analytical_mean_magnetization_squared(J, T)

print "Mean energy:             %8g" % mu_E
print "Analytical mean energy:  %8g" % exact_mean_energy
print "Error in mean energy:    %8g" % ((mu_E - exact_mean_energy)
                                        /exact_mean_energy)
print
print "Mean energy squared:         %8g" % mu_E_sq
print "Analytical mean energy sq.:  %8g" % exact_mean_energy_sq
print "Error in mean energy sq.:    %8g" % ((mu_E_sq - exact_mean_energy_sq)
                                            /exact_mean_energy_sq)
print
print "Mean abs. magnetization: %8g" % mu_abs_M
print "Analytical mean mag.:    %8g" % exact_mean_abs_magnetization
print "Error in mean mag..:     %8g" % ((mu_abs_M - exact_mean_abs_magnetization)
                                        /exact_mean_abs_magnetization)
print
print "Mean magnetization sq.:      %8g" % mu_M_sq
print "Analytical mean mag. sq.:    %8g" % exact_mean_magnetization_sq
print "Error in mean mag. sq.:      %8g" % ((mu_M_sq - exact_mean_magnetization_sq)
                                            /exact_mean_magnetization_sq)

print
print "Mean magnetization: %8g" % mu_M

print
print "Accepted configurations: %8g" % accepted_configurations
#print spin

show_spins(spin)

expectation_value_for_energy = np.cumsum(energies[1:]) / np.arange(1, (mc_cycles/save_every_nth+1))
plt.plot(expectation_value_for_energy)
#plt.ylim(-8.1, -7.9)
plt.show()
