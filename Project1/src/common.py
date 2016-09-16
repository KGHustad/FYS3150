import numpy as np
import matplotlib.pyplot as plt

# MATHEMATICAL FUNCTIONS
def u_func(x):
    """The analytical solution"""
    return 1-(1-np.exp(-10))*x-np.exp(-10*x)

def f_func(x):
    """The source term"""
    return 100*np.exp(-10*x)

# SOLVERS
def solve_general(f_func, n, a, b, c):
    x = np.linspace(0, 1, n+2)
    h = x[1] - x[0]
    s = f_func(x)*h**2
    v = np.zeros(n+2)

    # Forward Substitution
    for i in range(2, n+1):
        row_factor = a[i]/b[i-1]      # 1 FLOP
        b[i] -= c[i-1]*row_factor     # 2 FLOPS
        s[i] -= s[i-1]*row_factor     # 2 FLOPS

    #Backward Substitution
    v[n] = s[n]/b[n]

    for i in range(n-1,0,-1):
        v[i] = (s[i] - c[i]*v[i+1]) / b[i]  # 3 FLOPS

    return x, v

def solve_specific(f_func, n):
    x = np.linspace(0, 1, n+2)
    h = x[1] - x[0]
    s = f_func(x)*h**2
    v = np.zeros(n+2)
    b_func = lambda i: (i+1)/i
    b = np.zeros(n+2, dtype=np.float64)
    i = np.arange(0, n+2, dtype=np.float64)
    b[1:-1] = b_func(i[1:-1])
    for i in range(2,n+1):
        s[i] = s[i] + s[i-1]/b[i-1] # 2 FLOPS

    v[n] = s[n]/b[n]

    for i in range(n-1,0,-1):
        v[i] = (s[i]+v[i+1])/b[i]   # 2 FLOPS

    return x, v

# PLOTTING
def plot_magic(n_values, solve):
    for n in n_values:
        x, v = solve(n)
        plt.plot(x, v)
    legend = ["N = %d" % n for n in n_values]

    # plot analytical solution
    x = np.linspace(0, 1, 1000)
    plt.plot(x, u_func(x))
    legend.append('Analytical sol.')

    # make plot look great
    plt.legend(legend)
    plt.xlabel('x')
    plt.ylabel('u')
