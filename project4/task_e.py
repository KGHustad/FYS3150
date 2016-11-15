from common import *
import multiprocessing
import tabulate # on ImportError, run 'pip install tabulate'
import cPickle as pickle
import time
import argparse

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

def plot(data_dict, show=False):
    L_values = data_dict['L_values']
    T_values = data_dict['T_values']
    sweeps = data_dict['sweeps']
    dT = T_values[1] - T_values[0]

    length = len(T_values)
    mu_E = np.zeros(length)
    mu_abs_M = np.zeros(length)
    susceptibility = np.zeros(length)
    specific_heat = np.zeros(length)

    plots = [(mu_E, 'mean_energy', '$\mu_E$'),
             (mu_abs_M, 'mean_abs_magnetization', '$\mu_{|M|}$'),
             (susceptibility, 'susceptibility', '$\chi$'),
             (specific_heat, 'specific_heat', '$C_V$')]
    plt.clf()
    for L in L_values:
        print L
        for i, T in enumerate(T_values):
            entry = data_dict[(L, T)]
            mu_E[i] = entry['mu_E']
            mu_abs_M[i] = entry['mu_abs_M']
            susceptibility[i] = entry['susceptibility']
            specific_heat[i] = entry['specific_heat']
        for data_array, desc, ylabel in plots:
            plt.plot(T_values, data_array)
            plt.xlabel('$T$')
            plt.ylabel(ylabel)
            plt.savefig('fig/plot_e_L=%03d_dT=%g_sweeps=%.0E_%s.pdf' % (
                        L, dT, sweeps, desc))
            if show:
                plt.show()
            plt.clf()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-S', '--sweeps', dest='sweeps', type=float, default=int(1E4))
    parser.add_argument('-dT', '--temp_step', dest='dT', type=float, default=0.1)
    parser.add_argument('--seed', dest='seed', type=int, default=3150)
    parser.add_argument('--T_start', dest='T_start', type=float, default=2.0)
    parser.add_argument('--T_stop', dest='T_stop', type=float, default=2.3)
    parser.add_argument('--cutoff', dest='cutoff', type=float, default=0)
    args = parser.parse_args()

    dT = args.dT
    sweeps = int(args.sweeps)
    seed = args.seed
    T_start = args.T_start
    T_stop = args.T_stop
    cutoff = int(args.cutoff)

    n = int(round((T_stop - T_start)/dT))+1

    T_values = np.linspace(T_start, T_stop, n)

    J = 1
    save_every_nth = 1

    pool = multiprocessing.Pool()

    #L_values = [20, 40]
    L_values = [40, 60, 100, 140]
    L_values = np.asarray(L_values)
    spin_matrices = {L: homogeneous_spin_matrix(L, 1) for L in L_values}




    out_data_file_basename = 'task_e_dT=%g_sweeps=%.0E' % (dT, sweeps)
    time_suffix = True
    if time_suffix:
         out_data_file = '%s_%s.dat' % (out_data_file_basename, time.strftime('%Y-%m-%d--%H-%M-%S'))
    else:
         out_data_file = '%s.dat' % out_data_file_basename


    results = {}
    out_data = {}

    out_data['L_values'] = L_values
    out_data['T_values'] = T_values
    out_data['sweeps'] = sweeps
    out_data['cutoff'] = cutoff

    print "L values:"
    print L_values
    print

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

            mu_E, mu_M, mu_abs_M, mu_E_sq, mu_M_sq = extract_expectation_values(energies[cutoff:], mean_magnetization[cutoff:])

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
