from common import *
from main import *

if __name__ == '__main__':
    solver = 'c'
    n = 100
    for interaction in [False, True]:
        rho_max = 5
        plot_varying_omega(n, interaction, [0.5, 1, 5], rho_max, show=show)
        rho_max = 70
        plot_varying_omega(n, interaction, [0.5E-2, 1E-2, 5E-2], rho_max, show=show)
