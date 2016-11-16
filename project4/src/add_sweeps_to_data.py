import cPickle as pickle

filenames = ['data/task_e_dT=0.005_sweeps=1E+06_2016-11-15--00-20-15.dat',
             'data/task_e_dT=0.005_sweeps=2E+06_2016-11-15--00-30-32.dat']

sweep_array = [int(1E6), int(2E6)]

for filename, sweeps in zip(filenames, sweep_array):
    with open(filename, 'r') as f:
        data_dict = pickle.load(f)

    for key in sorted(data_dict.keys()):
        print data_dict[key]

    data_dict['sweeps'] = sweeps

    with open(filename, 'w') as f:
        pickle.dump(data_dict, f)
