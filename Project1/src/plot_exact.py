import numpy as np
import matplotlib.pyplot as plt
import sys

from common import u_func

if __name__ == '__main__':
    n = 10000
    x = np.linspace(0, 1, n)
    u = u_func(x)
    plt.plot(x, u)
    plt.xlabel('x')
    plt.ylabel('u(x)')
    plt.savefig('fig/plot_exact.pdf')
    if not "--dont_show" in sys.argv:
        plt.show()
