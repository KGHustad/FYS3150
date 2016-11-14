from common import *
import multiprocessing

L = 20
seed = 3150*2

mc_cycles = int(1E6)
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
        argv = [spin, J, T, mc_cycles, save_every_nth, seed]
        results[(desc, T)] = pool.apply_async(metropolis_c, argv)

for original_spin, desc in spin_matrices:
    for T in T_values:
        energies, mean_magnetization, accepted_configurations, time_spent = results[(desc, T)].get()

        expectation_value_for_energy = expectation_values( energies, save_every_nth, mc_cycles )
        plt.plot(expectation_value_for_energy, 'r')
        plt.xlabel("Monte-Carlo cycles")
        plt.ylabel("Expectation value for energy")
        plt.title("Converge of expectation values\nfor %.1e Monte-Carlo cycles\nwith a %s spin matrix" % (mc_cycles, desc))
        plt.tight_layout()
        plt.savefig('plot_c_energy_%s_T=%g.pdf' % (desc, T))
        plt.show()

        expectation_value_for_magnetization = expectation_values( mean_magnetization, save_every_nth, mc_cycles )
        plt.plot(expectation_value_for_magnetization, 'r')
        plt.xlabel("Monte-Carlo cycles")
        plt.ylabel("Expectation value for magnetization")
        plt.title("Converge of expectation values\nfor %.1e Monte-Carlo cycles\nwith a %s spin matrix" % (mc_cycles, desc))
        plt.tight_layout()
        plt.savefig('plot_c_magnetization_%s_T=%g.pdf' % (desc, T))
        plt.show()
