import numpy as np
from common import EnergyConfig, deltaE

J = 1

array = np.array( [ [1,-1], [-1,1] ] )

print "Energy of array:", EnergyConfig(array, J)

print "Delta E for flipping one spin:", deltaE(array, J, 0, 0)

array[0,0] *= -1
print "New energy of array:", EnergyConfig(np.array([[1,1],[1,-1]]), J)
