from common import *
import multiprocessing
import tabulate # on ImportError, run 'pip install tabulate'
import cPickle as pickle
import time

def format_table(data_dict):
    L_values = data_dict['L_values']
    T_values = data_dict['T_values']
    table_rows = len(L_values) * len(T_values)
    table_data = np.zeros((table_rows, 6), dtype=np.float64)
    i = 0
    for L in L_values:
        for T in T_values:
            entry = data_dict[(L, T)]
            table_data[i][0] = L
            table_data[i][1] = T
            table_data[i][2] = entry['mu_E']
            table_data[i][3] = entry['mu_abs_M']
            table_data[i][4] = entry['susceptibility']
            table_data[i][5] = entry['specific_heat']
            i += 1

    headers = ['L', 'T', 'mu_E', 'mu_abs_M', 'susceptibility', 'specific_heat']
    return tabulate.tabulate(table_data, headers, tablefmt='simple')


time_suffix = True
if time_suffix:
     out_data_file = 'task_e_%s.dat' % time.strftime('%Y-%m-%d--%H-%M-%S')
else:
     out_data_file = 'task_e.dat'

seed = 3150

J = 1
T = 1
save_every_nth = 1

pool = multiprocessing.Pool()

#L_values = [20, 40]
L_values = [40, 60, 100, 140]
L_values = np.asarray(L_values)
spin_matrices = {L: homogeneous_spin_matrix(L, 1) for L in L_values}

dt = 0.02
T_values = np.linspace(2, 2.3, int(round(0.3/dt))+1)

sweeps = int(1E4)

results = {}
out_data = {}

out_data['L_values'] = L_values
out_data['T_values'] = T_values

print "L values:"
print L_values

print "T values:"
print T_values

print

for L in reversed(L_values):
    for T in T_values:
            spin = spin_matrices[L].copy()
            argv = [spin, J, T, sweeps, save_every_nth, seed]
            results[(L, T)] = pool.apply_async(metropolis_c, argv)

for L in reversed(L_values):
    for T in T_values:
        energies, mean_magnetization, accepted_configurations, time_spent = results[(L, T)].get()

        mu_E, mu_M, mu_abs_M, mu_E_sq, mu_M_sq = extract_expectation_values(energies, mean_magnetization)

        susceptibility = (mu_M_sq - mu_abs_M**2)/T**2
        specific_heat = (mu_E_sq - mu_E**2)/T**2

        entry = {}
        #print "L=%g  T=%g   mu_E=%g" % (L, T, mu_E)
        entry['mu_E'] = mu_E
        entry['mu_abs_M'] = mu_abs_M
        entry['susceptibility'] = susceptibility
        entry['specific_heat'] = specific_heat
        out_data[(L, T)] = entry

with open(out_data_file, 'w') as f:
    pickle.dump(out_data, f)

#print out_data
print format_table(out_data)
