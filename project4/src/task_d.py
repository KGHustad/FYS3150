from common import *
import multiprocessing
import os
import sys

proj_path = get_proj_path()


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
reached_steady_state = int(1e5)

show = True
if '--no_show' in sys.argv:
    show = False

#show_spins(spin)

pool = multiprocessing.Pool()

mc_cycles = int(1E6)

res1 = pool.apply_async(metropolis_c, [spin1, J, T1, mc_cycles, save_every_nth, seed])
res2 = pool.apply_async(metropolis_c, [spin2, J, T2, mc_cycles, save_every_nth, seed])

energies1, mean_magnetization1, accepted_configurations, time_spent = res1.get()
energies2, mean_magnetization2, accepted_configurations, time_spent = res2.get()

energies1 = energies1[reached_steady_state:]
energies2 = energies2[reached_steady_state:]

exact_mean_energy = analytical_mean_energy(J, T1)
exact_mean_abs_magnetization = analytical_mean_abs_magnetization(J, T1)

energy_frequency1 = scipy.stats.itemfreq(energies1)
plt.hist( energies1, bins = len(energy_frequency1[:,0]), normed = True, align = 'left' )
plt.xlabel("Energy")
plt.ylabel("P(E)")
plt.title("Probability of energy-states for T = 1")
plt.tight_layout()
filename = 'fig/plot_d_T=1.pdf'
plt.savefig(os.path.join(proj_path, filename))
if show:
    plt.show()
plt.clf()

plt.plot(energy_frequency1[:,0],energy_frequency1[:,1])
if show:
    plt.show()
plt.clf()

energy_frequency2 = scipy.stats.itemfreq(energies2)
plt.hist( energies2, bins = energy_frequency2[:,0], normed = True, align = 'left' )
plt.xlabel("Energy")
plt.ylabel("P(E)")
plt.title("Probability of energy-states for T = 2.4")
plt.tight_layout()
filename = 'fig/plot_d_T=2.4.pdf'
plt.savefig(os.path.join(proj_path, filename))
if show:
    plt.show()
plt.clf()

energy_variance1 = np.var(energies1)
energy_variance2 = np.var(energies2)

print "Variance of energy for T = 1.0: ", energy_variance1
print "Variance of energy for T = 2.4: ", energy_variance2
