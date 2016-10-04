from common import *
from main import *

if __name__ == '__main__':
    solver = 'c'
    n = 200
    rho_max = 5
    for interaction in [False, True]:
        plot_lowest_energy_levels(n, interaction, omega, rho_max, solver=solver,
                                  plot=True, show=show, silent=True)
    rho_max = 10
    interaction = False
    plot_lowest_energy_levels(n, interaction, omega, rho_max, solver=solver,
                              plot=True, show=show, silent=True)
