import sys
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle
from task_e import plot

filenames = sys.argv[1:]

for filename in filenames:
    with open(filename, 'r') as f:
        data_dict = pickle.load(f)
    plot(data_dict, show=True)
