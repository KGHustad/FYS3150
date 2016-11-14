from common import *

seed = 3150

J = 1
T = 1
save_every_nth = 1

L = [40, 60, 100, 140]
spin = homogeneous_spin_matrix(L[0])


#show_spins(spin)

mc_cycles = int(1E7)
energies, mean_magnetization, accepted_configurations, time_spent = metropolis_c(spin, J, T, mc_cycles, save_every_nth=save_every_nth, seed=seed)
mu_E, mu_M, mu_abs_M, mu_E_sq, mu_M_sq = extract_expectation_values(energies, mean_magnetization)

print mu_E, mu_M, mu_abs_M, mu_E_sq, mu_M_sq
