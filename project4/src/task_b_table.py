from common import *
import sys
import tabulate

# disable terrible LaTeX escape behaviour in tabulate
tabulate.LATEX_ESCAPE_RULES = {}

seed = 3150

L = 2
spin = random_spin_matrix(L, seed=seed)
J = 1
T = 1
save_every_nth = 1

table_format = 'simple'
if '--latex' in sys.argv:
    table_format = 'latex'
elif '--markdown' in sys.argv:
    table_format = 'pipe'

silent = False
if '--silent' in sys.argv:
    silent = True

floatfmt = 'G'
if '--short' in sys.argv:
    floatfmt = '.1E'

sweeps_values = [10**4, 10**5, 10**6, 10**7]

# order of array:
# [mu_E, mu_E_sq, mu_abs_M, mu_M_sq, susceptibility, specific_heat]



exact = np.zeros(6, dtype=np.float64)
computed = np.zeros((len(sweeps_values), 6), dtype=np.float64)
error = np.zeros((len(sweeps_values), 6), dtype=np.float64)

exact[0] = analytical_mean_energy(J, T)
exact[1] = analytical_mean_energy_squared(J, T)
exact[2] = analytical_mean_abs_magnetization(J, T)
exact[3] = analytical_mean_magnetization_squared(J, T)
exact[4] = susceptibility(J, T)
exact[5] = heat_capacity(J, T)

for i, sweeps in enumerate(sweeps_values):
    energies, mean_magnetization, accepted_configurations, time_spent = metropolis_c(spin, J, T, sweeps, save_every_nth=save_every_nth, seed=seed, silent=silent)
    mu_E, mu_M, mu_abs_M, mu_E_sq, mu_M_sq = extract_expectation_values(energies, mean_magnetization)

    computed_susceptibility = (mu_M_sq - mu_abs_M**2)/T**2
    computed_specific_heat = (mu_E_sq - mu_E**2)/T**2

    computed[i,0] = mu_E
    computed[i,1] = mu_E_sq
    computed[i,2] = mu_abs_M
    computed[i,3] = mu_M_sq
    computed[i,4] = computed_susceptibility
    computed[i,5] = computed_specific_heat

    error[i] = (computed[i] - exact)/exact

#print error
data = np.zeros((len(sweeps_values), 7), dtype=np.float64)
data[:,1:] = error[:,:]
data[:,0] = np.asarray(sweeps_values)
#print data

headers = ['N', 'mu_E', 'mu_E_sq', 'mu_abs_M', 'mu_M_sq', 'susceptibility', 'specific_heat']
if table_format == 'latex':
    headers = ['$N$', '$\mu_E$', '$\mu_{E^2}$', '$\mu_{|M|}$', '$\mu_{M^2}$', '$\chi$', '$C_V$']

print tabulate.tabulate(data, headers, floatfmt=floatfmt, tablefmt=table_format)
