from common import *
#Changing fontsize to make plots readable without microscope
plt.rc('font', **{'size' : 14})

seed = 0

L = 20
spin1 = homogeneous_spin_matrix(L)
spin2 = homogeneous_spin_matrix(L)
J = 1
T1 = 1.0
T2 = 2.4
save_every_nth = 1
reached_steady_state = int(1e4)

#show_spins(spin)

mc_cycles = int(1E5)
energies1, mean_magnetization1, accepted_configurations, time_spent = metropolis_c(spin1, J, T1, mc_cycles, save_every_nth=save_every_nth, seed=seed)
energies2, mean_magnetization2, accepted_configurations, time_spent = metropolis_c(spin2, J, T2, mc_cycles, save_every_nth=save_every_nth, seed=seed)
energies1 = energies1[reached_steady_state:]
energies2 = energies2[reached_steady_state:]

exact_mean_energy = analytical_mean_energy(J, T1)
exact_mean_abs_magnetization = analytical_mean_abs_magnetization(J, T1)

energy_frequency1 = scipy.stats.itemfreq(energies1)
plt.hist( energies1, bins = len(energy_frequency1[:,0]), normed = True, align = 'left' )
plt.xlabel("Energy")
plt.ylabel("P(E)")
plt.title("Probability of energy-states for T = 1")
plt.show()

plt.plot(energy_frequency1[:,0],energy_frequency1[:,1])
plt.show()

energy_frequency2 = scipy.stats.itemfreq(energies2)
plt.hist( energies2, bins = energy_frequency2[:,0], normed = True, align = 'left' )
plt.xlabel("Energy")
plt.ylabel("P(E)")
plt.title("Probability of energy-states for T = 2.4")
plt.show()

energy_variance1 = np.var(energies1)
energy_variance2 = np.var(energies2)

print "Variance of energy for T = 1.0: ", energy_variance1
print "Variance of energy for T = 2.4: ", energy_variance2
