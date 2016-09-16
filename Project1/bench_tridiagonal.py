def CPU_time(n):
    import time
    from task_b import solve_general

    a = np.full(n+2, -1, dtype=np.float64)
    b = np.full(n+2, 2, dtype=np.float64)
    c = np.full(n+2, -1, dtype=np.float64)

    start_time = time.time()
    v,x = solve_general(f_func, n, a, b, c)
    print "General function run-time: %f seconds" % (time.time() - start_time)

    start_time = time.time()
    v,x = solve_specific(f_func, n)
    print "Specific function run-time: %f seconds" % (time.time() - start_time)

if __name__ == '__main__':
    CPU_time(int(1E6))
