import sys
import matplotlib.pyplot as plt
import numpy as np
import os
import cPickle as pickle
from common import *
from plotting import *

if len(sys.argv) < 2:
    print "USAGE: python %s <data file>" % (sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

with open(filename, 'r') as f:
    data_dict = pickle.load(f)

L_values = data_dict['L_values']
T_values = data_dict['T_values']
T_values = np.array(filter((lambda T: T <= 2.3), T_values))

L_count = len(L_values)
T_count = len(T_values)

data = np.zeros((L_count, T_count))

colours = ('b', 'g', 'r', 'c')

for i, L in enumerate(L_values):
    for j, T in enumerate(T_values):
        data[i, j] = data_dict[(L, T)]['specific_heat']/L**2

for i, L in enumerate(L_values):
    plt.plot(T_values, data[i], label='L=%3d' % L)
#plt.legend(loc='best')
#plt.show()

for i, L in enumerate(L_values):
    diffusion_1d(data[i], 20, 0.1, 'crank_nicolson', silent=True)
    plt.plot(T_values, data[i], '%s--'% colours[i], label='L=%3d (smoothed)' % L)
plt.legend(loc='best')
plt.xlabel('$T$')
plt.ylabel('$C_V$')
plt.savefig(get_fig_dir()+'/project4_smoothed_%s.pdf' % os.path.basename(filename)[:-4])
plt.show()
