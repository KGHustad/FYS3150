import time
from common import *

def bench(n_values):
    time_data = np.zeros((3, len(n_values)))
    header = "%8s  |  %8s  %8s  %8s" % ('N', 'Gen.', 'Spec.', 'LU')
    print(header)
    print("-"*len(header))
    for i, n in enumerate(n_values):
        a = np.full(n+2, -1, dtype=np.float64)
        b = np.full(n+2, 2, dtype=np.float64)
        c = np.full(n+2, -1, dtype=np.float64)

        start_time = time.time()
        v,x = solve_general(f_func, n, a, b, c)
        end_time = time.time()
        time_data[0,i] = end_time - start_time

        start_time = time.time()
        v,x = solve_specific(f_func, n)
        end_time = time.time()
        time_data[1,i] = end_time - start_time

        start_time = time.time()
        v,x = solve_LU(f_func, n)
        end_time = time.time()
        time_data[2,i] = end_time - start_time

        print("%8d  |  %8.1e  %8.1e  %8.1e" % (n, time_data[0,i],
                                                  time_data[1,i],
                                                  time_data[2,i]))

if __name__ == '__main__':
    n_values = [1*10**pow for pow in range(1, 5)]
    bench(n_values)
