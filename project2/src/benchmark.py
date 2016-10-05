import sys
import numpy as np

from common import *
import tabulate   # on ImportError, run 'pip install tabulate'

# disable terrible LaTeX escape behaviour in tabulate
tabulate.LATEX_ESCAPE_RULES = {}

if __name__ == '__main__':
    only_table = '--only_table' in sys.argv
    latex_table_format = '--latex' in sys.argv
    silent = only_table

    # since the algorithm runs in n^4 time, we increase n by 2^(1/4) at each
    # which should result in a doubling of the runtime
    n_start = 50
    n_end = 200
    steps_per_doubling = 4
    doublings = np.log2(n_end / n_start)
    n_points = int(doublings * steps_per_doubling + 1)

    n_values = np.logspace(np.log2(n_start), np.log2(n_end), n_points, base=2)
    n_values = np.array(np.round(n_values), dtype=np.int64)
    omega = 1
    rho_max = 6
    interaction_info = 'non-interacting'

    table_col_count = 1 + 3 + 1 + 1 + 1
    # N + 3 eigs + iterations + it/elem + time
    data = np.zeros(shape=(n_points, table_col_count), dtype=np.float64)

    for i, n in enumerate(n_values):
        data[i,0] = n
        if not only_table:
            print "N = %4d" % n
        A, rho = make_matrix_noninteracting_case(n, rho_max=rho_max)
        R = np.eye(n)
        iterations, time_spent, tol = solve_c(A, R, silent=silent)
        eig = extract_eigs_dict(A, R)
        data[i, 1:4] = eig['val'][:3]
        data[i, 4] = iterations
        data[i, 5] = iterations / float(n**2)
        data[i, 6] = time_spent
        if not only_table:
            print "Solution for %s case with omega=%6g, n=%d took %g seconds" \
                  % (interaction_info, omega, n, time_spent)
            print eig['val'][:3]
            print

    headers = ["N", u"\u03BB_1", u"\u03BB_2", u"\u03BB_3", "iterations",
               "it./N**2", "time"]
    if latex_table_format:
        headers = ["$N$", "$\lambda_1$", "$\lambda_2$", "$\lambda_3$",
                   "iterations", "$\\frac{iterations}{N^2}$", "time"]
        print tabulate.tabulate(data, headers, tablefmt='latex')
    else:
        """
        headers = ["N", "lambda_1", "lambda_2", "lambda_3",
                   "iterations", "time"]
        """
        print tabulate.tabulate(data, headers, tablefmt='simple')
