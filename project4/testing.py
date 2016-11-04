import numpy as np
from common import EnergyConfig, deltaE

array = np.array( [ [-1,1], [1,-1] ] )

print "Energy of array:", EnergyConfig(array, 2, -1)

print "Delta E for flipping one spin:", deltaE(array, 2, -1, 0, 0)

print "New energy of array:", EnergyConfig(np.array([[1,1],[1,-1]]), 2, -1)
