#import sys
#import numpy as np
import argparse

from common import *

parser = argparse.ArgumentParser()
parser.add_argument('-N', '--points',
                    dest='N', metavar='N',
                    type=int, default=40)
parser.add_argument('-p', '--rho_max',
                    metavar='rho_max',
                    type=float, default=5)
parser.add_argument('--plot',
                    action='store_true', default=False)
parser.add_argument('--interaction',
                    choices=['non-interacting', 'interacting'],
                    default='non-interacting')

args = parser.parse_args()
N = args.N
rho_max = args.rho_max
plot = args.plot

print args
