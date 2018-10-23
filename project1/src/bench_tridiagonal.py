import time
from common import *

def CPU_time(n):
    a = np.full(n+2, -1, dtype=np.float64)
    b = np.full(n+2, 2, dtype=np.float64)
    c = np.full(n+2, -1, dtype=np.float64)

    start_time = time.time()
    v,x = solve_general(f_func, n, a, b, c)
    end_time = time.time()
    print("General function run-time: %f seconds" % (end_time - start_time))

    start_time = time.time()
    v,x = solve_specific(f_func, n)
    end_time = time.time()
    print("Specific function run-time: %f seconds" % (end_time - start_time))

if __name__ == '__main__':
    CPU_time(int(1E6))
