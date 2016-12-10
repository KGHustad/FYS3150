import sys
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle
from task_e import *

args = sys.argv[1:]

usage = "USAGE: python %s <output_data_file> <input data files>" % (sys.argv[0])

if len(args) < 2:
    print usage
    sys.exit(1)

outfilename = args[0]
infilenames = args[1:]

master_dict = {}
T_values = set()
L_values = None
sweeps = None
cutoff = None
for i, filename in enumerate(infilenames):
    print "joining '%s' ..." % filename
    with open(filename, 'r') as f:
        data_dict = pickle.load(f)

        T_values_part = set(data_dict['T_values'])
        L_values_part = data_dict['L_values']
        sweeps_part = data_dict['sweeps']
        cutoff_part = data_dict['cutoff']

        if T_values is None:
            T_values = T_values_part
        else:
            common_T_values = T_values.intersection(T_values_part)
            if len(common_T_values) > 0:
                print "Warning: %d values in common:" % len(common_T_values)
                print np.array(sorted(list(common_T_values)))

            T_values = T_values.union(T_values_part)
        if L_values is None:
            L_values = sorted(L_values_part)
        else:
            assert L_values == sorted(L_values_part)

        if sweeps is None:
            sweeps = sweeps_part
        else:
            msg = "# of sweeps is not the same (%d != %d)"
            assert sweeps == sweeps_part, msg

        if cutoff is None:
            cutoff = cutoff_part
        else:
            msg = "cutoff point is not the same! \n"
            msg += "Previous: %d  This: %d" % (cutoff, cutoff_part)
            assert cutoff == cutoff_part, msg

        del data_dict['T_values']
        del data_dict['L_values']

        master_dict.update(data_dict)

T_values = np.array(sorted(list(T_values)))
master_dict['T_values'] = T_values
master_dict['L_values'] = L_values

if outfilename in infilenames:
    print "Warning: Outfilename equal to a infilename. Skipping file write..."
    sys.exit(1)
else:
    with open(outfilename, 'w') as f:
        pickle.dump(master_dict, f)

print
print format_table(master_dict)
