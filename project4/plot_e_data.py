import sys
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle
from task_e import plot

filenames = sys.argv[1:]

if len(filenames) == 0:
    print "USAGE: python %s <data file> [more data files]" % (sys.argv[0])
    sys.exit(1)

for filename in filenames:
    with open(filename, 'r') as f:
        data_dict = pickle.load(f)
    plot(data_dict, #show=True
    )
