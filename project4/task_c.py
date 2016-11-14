from common import *
import multiprocessing

L = 20
seed = 3150*2

convergence_reached = int(2E5)

sweeps = int(1E6)
J = 1
save_every_nth = 1

spin_homogeneous = homogeneous_spin_matrix(L, 1)
spin_random = random_spin_matrix(L, seed=seed)
spin_matrices = [(spin_homogeneous, 'homogeneous'), (spin_random, 'random')]

pool = multiprocessing.Pool()

T_values = [1, 2.4]
results = {}
for original_spin, desc in spin_matrices:
    for T in T_values:
        spin = original_spin.copy()
        argv = [spin, J, T, sweeps, save_every_nth, seed]
        results[(desc, T)] = pool.apply_async(metropolis_c, argv)

for original_spin, desc in spin_matrices:
    for T in T_values:
        energies, mean_magnetization, accepted_configurations, time_spent = results[(desc, T)].get()

        # discard noise in the start
        energies = energies[convergence_reached:]
        mean_magnetization = mean_magnetization[convergence_reached:]
        length = len(energies)
        sweep_array= np.arange(convergence_reached, sweeps+1)


        expectation_value_for_energy = expectation_values(energies, length)
        expectation_value_for_magnetization = expectation_values(mean_magnetization, length)

        plt.plot(sweep_array, expectation_value_for_energy, 'r')
        plt.xlabel("Monte-Carlo cycles")
        plt.ylabel("Expectation value for energy")
        plt.title("Converge of expectation values\nfor %.0E sweeps\nwith a %s spin matrix with L=%d" % (sweeps, desc, L))
        plt.tight_layout()
        plt.savefig('fig/plot_c_energy_%s_T=%g_sweeps=%.0E.pdf' % (
                    desc, T, sweeps))
        plt.show()

        plt.plot(sweep_array, expectation_value_for_magnetization, 'r')
        plt.xlabel("Monte-Carlo cycles")
        plt.ylabel("Expectation value for magnetization")
        plt.title("Converge of expectation values\nfor %.0E Monte-Carlo cycles\nwith a %s spin matrix with L=%d" % (sweeps, desc, L))
        plt.tight_layout()
        plt.savefig('fig/plot_c_magnetization_%s_T=%g_sweeps=%.0E.pdf' % (
                    desc, T, sweeps))
        plt.show()
