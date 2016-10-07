import argparse

from common import *

parser = argparse.ArgumentParser()
parser.add_argument('-N', '-n',
                    dest='n', metavar='N',
                    type=int, default=40)
parser.add_argument('-p', '--rho_max',
                    type=float, default=5)
parser.add_argument('-w', '--omega',
                    type=float, default=1)
parser.add_argument('--solver',
                    choices=['python', 'c'], default='c',
                    help='choose solver')
parser.add_argument('--omegas',
                    nargs='+', type=float, default=None,
                    help='set of omega values')
parser.add_argument('--plot',
                    action='store_true', default=False,
                    help='make plot')
parser.add_argument('--show',
                    action='store_true', default=False,
                    help='show plot (only if plot is enabled)')
parser.add_argument('--interaction',
                    action='store_true', default=False,
                    help='enable interaction between electrons')

args = parser.parse_args()
n = args.n
rho_max = args.rho_max
omega = args.omega
omegas = args.omegas
solver = args.solver
plot = args.plot
show = args.show
interaction = args.interaction

if omegas:
    omega_values = omegas
else:
    omega_values = [omega]

interaction_info = 'interacting' if interaction else 'non-interacting'

if __name__ == '__main__':
    plot_lowest_energy_levels(n, interaction, omega, rho_max, solver=solver,
                              plot=plot, show=show)
